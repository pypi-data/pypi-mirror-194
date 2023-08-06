#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Union, List, Iterable, Dict, Callable, Set, Any, Tuple, cast
from memoization import cached
import os.path
import re
import math

from nomad import utils
from nomad.units import ureg
from nomad.datamodel import EntryArchive, EntryData, ArchiveSection
from nomad.datamodel.context import Context
from nomad.metainfo import Section, Quantity, Package, Reference, SectionProxy, MSection, Property
from nomad.metainfo.metainfo import MetainfoError, SubSection
from nomad.parsing.parser import MatchingParser
from nomad.datamodel.metainfo.annotations import TabularMode, TabularAnnotation, TabularParserAnnotation
from nomad.metainfo.util import MSubSectionList

# We define a simple base schema for tabular data. The parser will then generate more
# specialized sections based on the table headers. These specialized definitions will use
# this as base section definition.
# TODO maybe this should be moved to nomad.datamodel.metainfo
m_package = Package()


def traverse_to_target_data_file(section, path_list: List[str]):
    if len(path_list) == 0 and isinstance(section, str):
        return section
    else:
        try:
            temp = path_list.pop(0)
            return traverse_to_target_data_file(getattr(section, temp), path_list)
        except AttributeError:
            raise MetainfoError(f'The path {temp} in path_to_data_file does not exist')


def to_camel_case(snake_str: str):
    '''Take as input a snake case variable and return a camel case one'''

    components = snake_str.split('_')

    return ''.join(f'{x[0].upper()}{x[1:].lower()}' for x in components)


def extract_tabular_parser_annotation(archive):
    for quantity_def in archive.m_def.all_quantities.values():
        annotation = quantity_def.m_get_annotations('tabular_parser')
        if not annotation:
            pass
        else:
            return annotation, quantity_def
    return None, None


class TableRow(EntryData):
    ''' Represents the data in one row of a table. '''
    table_ref = Quantity(
        type=Reference(SectionProxy('Table')),
        description='A reference to the table that this row is contained in.')


class Table(EntryData):
    ''' Represents a table with many rows. '''
    row_refs = Quantity(
        type=Reference(TableRow.m_def), shape=['*'],
        description='References that connect to each row. Each row is stored in it individual entry.')


class TableData(ArchiveSection):

    fill_archive_from_datafile = Quantity(
        type=bool,
        a_eln=dict(component='BoolEditQuantity'),
        description='''While checked, it allows the parser to fill all the Quantities from the data file.
        Be cautious though! as checking this box will cause overwriting your fields with data parsed from the data file
        ''',
        default=True)

    def normalize(self, archive, logger):
        super(TableData, self).normalize(archive, logger)

        if self.fill_archive_from_datafile:
            annotation, quantity_def = extract_tabular_parser_annotation(self)
            if annotation:
                if isinstance(annotation, list):
                    annotation = annotation[0]
                self.tabular_parser(quantity_def, archive, logger, annotation)

    def tabular_parser(self, quantity_def: Quantity, archive, logger, annotation: TabularParserAnnotation):
        if logger is None:
            logger = utils.get_logger(__name__)

        if not quantity_def.is_scalar:
            raise NotImplementedError('CSV parser is only implemented for single files.')

        if annotation.path_to_data_file:
            self.m_set(
                quantity_def,
                traverse_to_target_data_file(
                    archive,
                    annotation.path_to_data_file.split('#')[1].split('/')
                )
            )

        data_file = self.m_get(quantity_def)
        if not data_file:
            return

        with archive.m_context.raw_file(data_file) as f:
            data = read_table_data(data_file, f, **annotation.dict(include={'sep', 'comment', 'skiprows'}))

        tabular_parser_mode = annotation.mode
        if tabular_parser_mode == TabularMode.column:
            parse_columns(data, self)

        elif tabular_parser_mode == TabularMode.row:
            # Getting list of all repeating sections where new instances are going to be read from excel/csv file
            # and appended.
            section_names: List[str] = annotation.target_sub_section

            # A list to track if the top-most level section has ever been visited
            list_of_visited_sections: List[str] = []

            for section_name in section_names:
                section_name_list = section_name.split('/')
                section_name_str = section_name_list[0]
                section_def = getattr(self, to_camel_case(section_name_str)).m_def

                if not list_of_visited_sections.count(section_name_str):
                    list_of_visited_sections.append(section_name_str)

                    # The (sub)section needs to be cleared first
                    if isinstance(getattr(self, section_name_str), MSubSectionList):
                        getattr(self, section_name_str).clear()
                    else:
                        setattr(self, section_name_str, section_def.section_cls())

                sections = parse_table(data, section_def, logger=logger)
                for section in sections:
                    self.append_section_to_subsection(section_name, section)

        else:
            raise MetainfoError(f'The provided mode {tabular_parser_mode.value} should be either "column" or "row".')

        # If the `fill_archive_from_datafile` checkbox is set to be hidden for this specific section, parser's logic
        # also needs to be modified to 'Always run the parser if it's been called'.
        eln_annotation = self.m_def.m_get_annotations('eln', None)
        try:
            self.fill_archive_from_datafile = 'fill_archive_from_datafile' in eln_annotation.hide
        except AttributeError:
            self.fill_archive_from_datafile = False

    def append_section_to_subsection(self, section_name: str, section: MSection):
        section_name_list = section_name.split('/')
        top_level_section = section_name_list[0]
        self_updated = getattr(self, top_level_section)
        section_updated = section
        section_name_list.pop(0)
        for section_path in section_name_list:
            self_updated = self_updated[section_path]
            section_updated = section_updated[section_path]
        if len(section_name_list) == 0:
            self_updated.append(section_updated)
        else:
            self_updated.append(section_updated[0])


m_package.__init_metainfo__()


@cached(max_size=10)
def _create_column_to_quantity_mapping(section_def: Section):
    mapping: Dict[str, Callable[[MSection, Any], MSection]] = {}

    def add_section_def(section_def: Section, path: List[Tuple[SubSection, Section]]):
        properties: Set[Property] = set()

        for quantity in section_def.all_quantities.values():
            if quantity in properties:
                continue
            properties.add(quantity)

            annotation = quantity.m_get_annotations('tabular')
            annotation = annotation[0] if isinstance(annotation, list) else annotation
            if annotation and annotation.name:
                col_name = annotation.name
            else:
                col_name = quantity.name
                if len(path) > 0:
                    col_name = f'{".".join([item[0].name for item in path])}.{col_name}'

            if col_name in mapping:
                raise MetainfoError(
                    f'The schema has non unique column names. {col_name} exists twice. '
                    f'Column names must be unique, to be used for tabular parsing.')

            def set_value(
                    section: MSection, value, path=path, quantity=quantity,
                    annotation: TabularAnnotation = annotation):

                import numpy as np
                for sub_section, section_def in path:
                    next_section = None
                    try:
                        next_section = section.m_get_sub_section(sub_section, -1)
                    except (KeyError, IndexError):
                        pass
                    if not next_section:
                        next_section = section_def.section_cls()
                        section.m_add_sub_section(sub_section, next_section, -1)
                    section = next_section

                if annotation and annotation.unit:
                    value *= ureg(annotation.unit)

                # NaN values are not supported in the metainfo. Set as None
                # which means that they are not stored.
                if isinstance(value, float) and math.isnan(value):
                    value = None

                if isinstance(value, (int, float, str)):
                    value = np.array([value])

                if value is not None:
                    if len(value.shape) == 1 and len(quantity.shape) == 0:
                        if len(value) == 1:
                            value = value[0]
                        elif len(value) == 0:
                            value = None
                        else:
                            raise MetainfoError(
                                'The shape of {quantity.name} does not match the given data.')
                    elif len(value.shape) != len(quantity.shape):
                        raise MetainfoError(
                            'The shape of {quantity.name} does not match the given data.')

                section.m_set(quantity, value)

            mapping[col_name] = set_value

        for sub_section in section_def.all_sub_sections.values():
            if sub_section in properties:
                continue
            next_base_section = sub_section.sub_section
            properties.add(sub_section)
            for sub_section_section in next_base_section.all_inheriting_sections + [next_base_section]:
                add_section_def(sub_section_section, path + [(sub_section, sub_section_section,)])

    add_section_def(section_def, [])
    return mapping


def parse_columns(pd_dataframe, section: MSection):
    '''
    Parses the given pandas dataframe and adds columns (all values as array) to
    the given section.
    '''
    import pandas as pd
    data: pd.DataFrame = pd_dataframe

    mapping = _create_column_to_quantity_mapping(section.m_def)  # type: ignore
    for column in mapping:
        if '/' in column:
            # extract the sheet & col names if there is a '/' in the 'name'
            sheet_name, col_name = column.split('/')
            if sheet_name not in list(data):
                raise ValueError(
                    'The sheet name {sheet_name} doesn''t exist in the excel file')

            df = pd.DataFrame.from_dict(data.loc[0, sheet_name])
            mapping[column](section, df.loc[:, col_name])
        else:
            # Otherwise, assume the sheet_name is the first sheet of excel/csv
            df = pd.DataFrame.from_dict(data.iloc[0, 0])
            if column in df:
                mapping[column](section, df.loc[:, column])


def parse_table(pd_dataframe, section_def: Section, logger):
    '''
    Parses the given pandas dataframe and creates a section based on the given
    section_def for each row. The sections are filled with the cells from
    their respective row.
    '''
    import pandas as pd
    data: pd.DataFrame = pd_dataframe
    sections: List[MSection] = []
    sheet_name = 0

    mapping = _create_column_to_quantity_mapping(section_def)  # type: ignore

    # data object contains the entire excel file with all of its sheets (given that an
    # excel file is provided, otherwise it contains the csv file). if a sheet_name is provided,
    # the corresponding sheet_name from the data is extracted, otherwise its assumed that
    # the columns are to be extracted from first sheet of the excel file.
    for column in mapping:
        if column == section_def.name:
            continue
        if '/' in column:
            sheet_name = column.split('/')[0]

    df = pd.DataFrame.from_dict(data.loc[0, sheet_name] if isinstance(sheet_name, str) else data.iloc[0, sheet_name])

    for row_index, row in df.iterrows():
        section = section_def.section_cls()
        try:
            for column in mapping:
                col_name = column.split('/')[1] if '/' in column else column

                if col_name in df:
                    try:
                        mapping[column](section, row[col_name])
                    except Exception as e:
                        logger.error(
                            f'could not parse cell',
                            details=dict(row=row_index, column=col_name), exc_info=e)
        except Exception as e:
            logger.error(f'could not parse row', details=dict(row=row_index), exc_info=e)
        sections.append(section)

    return sections


def read_table_data(
        path, file_or_path=None,
        comment: str = None, sep: str = None, skiprows: int = None):
    import pandas as pd
    df = pd.DataFrame()

    if file_or_path is None:
        file_or_path = path

    if path.endswith('.xls') or path.endswith('.xlsx'):
        excel_file: pd.ExcelFile = pd.ExcelFile(
            file_or_path if isinstance(file_or_path, str) else file_or_path.name)
        for sheet_name in excel_file.sheet_names:
            df.loc[0, sheet_name] = [
                pd.read_excel(excel_file, sheet_name=sheet_name, comment=comment).to_dict()
            ]
    else:
        df.loc[0, 0] = [
            pd.read_csv(
                file_or_path, engine='python',
                comment=comment,
                sep=sep,
                skipinitialspace=True
            ).to_dict()
        ]

    return df


class TabularDataParser(MatchingParser):
    creates_children = True

    def __init__(self) -> None:
        super().__init__(
            name='parser/tabular', code_name='tabular data',
            domain=None,
            mainfile_mime_re=r'text/.*|application/.*',
            mainfile_name_re=r'.*\.archive\.(csv|xlsx?)$')

    def _get_schema(self, filename: str, mainfile: str):
        dir = os.path.dirname(filename)
        match = re.match(r'^(.+\.)?([\w\-]+)\.archive\.(csv|xlsx?)$', os.path.basename(filename))
        if not match:
            return None

        schema_name = match.group(2)
        for extension in ['yaml', 'yml', 'json']:
            schema_file_base = f'{schema_name}.archive.{extension}'
            schema_file = os.path.join(dir, schema_file_base)
            if not os.path.exists(schema_file):
                continue
            return os.path.join(os.path.dirname(mainfile), schema_file_base)

        return None

    def is_mainfile(
        self, filename: str, mime: str, buffer: bytes, decoded_buffer: str,
        compression: str = None
    ) -> Union[bool, Iterable[str]]:
        # We use the main file regex capabilities of the superclass to check if this is a
        # .csv file
        import pandas as pd
        is_tabular = super().is_mainfile(filename, mime, buffer, decoded_buffer, compression)
        if not is_tabular:
            return False

        try:
            data = read_table_data(filename)
        except Exception:
            # If this cannot be parsed as a .csv file, we don't match with this file
            return False
        data = pd.DataFrame.from_dict(data.iloc[0, 0])
        return [str(item) for item in range(0, data.shape[0])]

    def parse(
        self, mainfile: str, archive: EntryArchive, logger=None,
        child_archives: Dict[str, EntryArchive] = None
    ):
        if logger is None:
            logger = utils.get_logger(__name__)

        # We use mainfile to check the files existence in the overall fs,
        # and archive.metadata.mainfile to get an upload/raw relative schema_file
        schema_file = self._get_schema(mainfile, archive.metadata.mainfile)
        if schema_file is None:
            logger.error('Tabular data file without schema.', details=(
                'For a tabular file like name.schema.archive.csv, there has to be an '
                'uploaded schema like schema.archive.yaml'))
            return

        try:
            schema_archive = cast(Context, archive.m_context).load_raw_file(
                schema_file, archive.metadata.upload_id, None)
            package = schema_archive.definitions
            section_def = package.section_definitions[0]
        except Exception as e:
            logger.error('Could not load schema', exc_info=e)
            return

        if TableRow.m_def not in section_def.base_sections:
            logger.error('Schema for tabular data must inherit from TableRow.')
            return

        annotation: TabularParserAnnotation = section_def.m_get_annotations('tabular_parser')
        kwargs = annotation.dict(include={'comment', 'sep', 'skiprows'}) if annotation else {}
        data = read_table_data(mainfile, **kwargs)
        child_sections = parse_table(data, section_def, logger=logger)
        assert len(child_archives) == len(child_sections)

        table = Table()
        archive.data = table

        child_section_refs: List[MSection] = []
        for child_archive, child_section in zip(child_archives.values(), child_sections):
            child_archive.data = child_section
            child_section_refs.append(child_section)
            child_section.table_ref = table
        table.row_refs = child_section_refs
