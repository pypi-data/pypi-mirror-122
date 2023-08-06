from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class SplitGrid(Function):
    """Split a single sensor grid file into multiple smaller grids."""

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    input_grid = Inputs.file(description='Input grid file.', path='grid.pts')

    @command
    def split_grid(self):
        return 'honeybee-radiance grid split grid.pts ' \
            '{{self.sensor_count}} --folder output --log-file output/grids_info.json'

    grids_list = Outputs.list(
        description='A JSON array that includes information about generated sensor '
        'grids.', path='output/grids_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output'
    )


@dataclass
class SplitGridFolder(Function):
    """Create new sensor grids folder with evenly distribute sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder.
    """

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    grid_count = Inputs.int(
        description='Number of output sensor grids to be created. This number is '
        'usually equivalent to the number of processes that will be used to run the '
        'simulations in parallel.', spec={'type': 'integer', 'minimum': 1}
    )

    sensor_count = Inputs.int(
        description='Minimum number of sensors in each output grid. Use this number to '
        'ensure the number of sensors in output grids never gets very small. To ignore '
        'this limitation set the value to 1 otherwise the number of grids will be '
        'adjusted based on minimum sensor count if needed. Default: 2000.', default=2000,
        spec={'type': 'integer', 'minimum': 1}
    )

    @command
    def split_grid_folder(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder ' \
            '{{self.grid_count}} --min-sensor-count {{self.sensor_count}}'

    sensor_grids = Outputs.list(
        description='A JSON array that includes information about generated sensor '
        'grids.', path='output_folder/_info.json'
    )

    dist_info = Outputs.file(
        description='A JSON file with distribution information.',
        path='output_folder/_redist_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output_folder'
    )


@dataclass
class MergeFiles(Function):
    """Merge several files with similar starting name into one."""

    name = Inputs.str(
        description='Base name for files to be merged.',
        default='grid'
    )

    extension = Inputs.str(
        description='File extension including the . before the extension (e.g. .res, '
        '.ill)'
    )

    folder = Inputs.folder(
        description='Target folder with the input files.',
        path='input_folder'
    )

    @command
    def merge_files(self):
        return 'honeybee-radiance grid merge input_folder grid ' \
            ' {{self.extension}} --name {{self.name}}'

    result_file = Outputs.file(
        description='Output result file.', path='{{self.name}}{{self.extension}}'
    )


@dataclass
class MergeFolderData(Function):
    """Restructure files in a distributed folder."""

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    extension = Inputs.str(
        description='Extension of the files to collect data from. It will be ``pts`` '
        'for sensor files. Another common extension is ``ill`` for the results of '
        'daylight studies.'
    )

    @command
    def merge_files(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder ' \
            ' {{self.extension}}'

    output_folder = Outputs.folder(
        description='Output folder with newly generated files.', path='output_folder'
    )
