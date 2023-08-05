from datazen import ROOT_NAMESPACE as ROOT_NAMESPACE
from datazen.enums import DataType as DataType
from datazen.environment.base import LOADTYPE as LOADTYPE
from datazen.environment.schema import SchemaEnvironment as SchemaEnvironment
from datazen.environment.variable import VariableEnvironment as VariableEnvironment
from typing import Any, List

LOG: Any

class ConfigEnvironment(VariableEnvironment, SchemaEnvironment):
    configs_valid: bool
    def __init__(self) -> None: ...
    def load_configs(self, cfg_loads: LOADTYPE = ..., var_loads: LOADTYPE = ..., sch_loads: LOADTYPE = ..., sch_types_loads: LOADTYPE = ..., name: str = ...) -> dict: ...
    def add_config_dirs(self, dir_paths: List[str], rel_path: str = ..., name: str = ..., allow_dup: bool = ...) -> int: ...
