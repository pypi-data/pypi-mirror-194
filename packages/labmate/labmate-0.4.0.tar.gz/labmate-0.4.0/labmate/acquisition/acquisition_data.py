import os
from typing import Dict, List, Optional, Union

from ..syncdata import SyncData


class NotebookAcquisitionData(SyncData):
    """It's a SyncData that has information about the configs file and the cell.
    `configs` is a list of the paths to the files that saved by `save_config_files` function.
    `cell` is a str. It saves using `save_cell` function that will save it to `..._CELL.py` file"""

    def __init__(self,
                 filepath: str,
                 configs: Optional[Union[
                     Dict[str, str], List[str]]] = None,
                 cell: Optional[str] = None,
                 overwrite: Optional[bool] = True,
                 save_on_edit: bool = True,
                 save_files: bool = True):

        super().__init__(filepath=filepath, save_on_edit=save_on_edit, read_only=False, overwrite=overwrite)

        if isinstance(configs, list):
            configs = read_config_files(configs)

        self['configs'] = configs
        if cell is not None and cell != "none":
            self['acquisition_cell'] = cell
        self['useful'] = False
        self._save_files = save_files

    def save_config_files(self, configs: Optional[Dict[str, str]] = None, filepath: Optional[str] = None):
        if not self._save_files:
            return

        filepath = self._check_if_filepath_was_set(filepath, self._filepath)

        configs = configs or self['configs']
        if configs is None:
            return
        for name, value in configs.items():
            with open(filepath + '_' + name, 'w', encoding="utf-8") as file:
                file.write(value)

    def save_cell(self, cell: Optional[str] = None, filepath: Optional[str] = None):
        if not self._save_files:
            return

        filepath = self._check_if_filepath_was_set(filepath, self._filepath)

        cell = cell or (self['acquisition_cell'] if 'acquisition_cell' in self else None)
        if cell is None:
            return

        with open(filepath + '_CELL.py', 'w', encoding="utf-8") as file:
            file.write(cell)

    def save_additional_info(self):
        self['useful'] = True

        if not self._save_files:
            return
        self.save_cell()
        self.save_config_files()


def read_config_files(config_files: List[str]) -> Dict[str, str]:
    configs: Dict[str, str] = {}
    # existed_names = set()
    for config_file in config_files:
        config_file_name = os.path.basename(config_file)
        if config_file_name in configs:
            raise ValueError("Some of the files have the same name. So it cannot \
                                be pushed into dictionary to preserve unique key")
        configs[config_file_name] = read_file(config_file)
    return configs


def read_file(file: str) -> str:
    if not os.path.isfile(file):
        raise ValueError(f"Cannot read a file if it doesn't exist or it's not a file. \
                        Path: {os.path.abspath(file)}")
    with open(file, 'r', encoding="utf-8") as file_opened:
        return file_opened.read()
