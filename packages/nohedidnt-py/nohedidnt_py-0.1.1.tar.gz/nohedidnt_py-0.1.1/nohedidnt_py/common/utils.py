# -*- coding: utf-8 -*-
from nohedidnt_py.common.aliases import *


# Configs -------------------------------------


class NhdConfig(BaseConfig):
    allow_population_by_field_name = True
    anystr_strip_whitespace = True
    arbitrary_types_allowed = True
    smart_union = True
    underscore_attrs_are_private = True
    use_enum_values = True
    validate_assignment = True


# Defaults ------------------------------------


@dataclass(config=NhdConfig, frozen=True)
class NhdDefaults:
    # Package
    PKG_ABBR: str = "nhd"
    PKG_AUTHOR: str = "NoHeDidn't"
    PKG_NAME: str = "nohedidnt_py"
    # Paths
    HOME_DIR: Path = Path.home()
    # FileInfos
    ENCODING_ALT: str = "iso8859_2"
    ENCODING_DFT: str = "utf-8"
    # Collections
    DIRTIES = Box(
        cls_name=["Meta"],
        path_name=[".DS_Store", ".git", ".idea", ".venv", "_devel"],
        pkg_name=["common", "constants", "core"],
    )


nhd_defaults = NhdDefaults()


# Catalogues ----------------------------------


nhd_enums: Registry = catalogue.create(nhd_defaults.PKG_ABBR, "enums")
nhd_factories: Registry = catalogue.create(nhd_defaults.PKG_ABBR, "factories")
nhd_type_conversions: Registry = catalogue.create(nhd_defaults.PKG_ABBR, "type_conversions")


# Dynamics ------------------------------------


def nhd_dynamics() -> DynamicsTupl:
    dirty_pkg_names: StrList = nhd_defaults.DIRTIES.get("pkg_name", list())
    home_dir: Path = nhd_defaults.HOME_DIR
    pkg_dir: Path = Path().resolve()
    pkg_name: str = nhd_defaults.PKG_NAME
    
    if not pkg_dir.exists() or not pkg_dir.is_dir():
        raise ValueError("Invalid pkg_dir")
    
    if pkg_dir.stem in dirty_pkg_names:
        while pkg_dir.stem in dirty_pkg_names:
            pkg_dir = pkg_dir.parent
            if pkg_dir.stem not in dirty_pkg_names:
                break
    
    if not pkg_name == pkg_dir.stem:
        pkg_name = pkg_dir.stem
    
    name_count = pkg_dir.parts.count(pkg_name)
    while name_count > 1:
        pkg_dir = pkg_dir.parent
        name_count = pkg_dir.parts.count(pkg_name)
        
        if name_count <= 1:
            break
    
    if not pkg_dir.exists() or not pkg_dir.is_dir() or home_dir not in pkg_dir.parents:
        raise ValueError("Invalid pkg_dir")
    
    env_file: Path = pkg_dir.joinpath(".env")
    
    return env_file, pkg_dir, pkg_name


env_file, pkg_dir, pkg_name = nhd_dynamics()

# TypeGuard
install_import_hook(pkg_name)


# EnVars --------------------------------------


class NhdEnvars(BaseSettings):
    pkg_abbr: str = Field(default=nhd_defaults.PKG_ABBR, env="PKG_ABBR")
    pkg_author: str = Field(default=nhd_defaults.PKG_AUTHOR, env="PKG_AUTHOR")
    # Paths
    pw_dir: OptPath = Field(default=None, env="pwd")
    tmp_dir: OptPath = Field(default=None, env="tmpdir")
    venv_dir: OptPath = Field(default=None, env="virtual_env")
    # Modes
    devel_mode: bool = Field(default=False, env="devel_mode")
    short_mode: bool = Field(default=False, env="short_mode")
    test_mode: bool = Field(default=False, env="test_mode")
    
    # Config
    class Config(NhdConfig):
        env_file: Path = env_file
        env_file_encoding: str = nhd_defaults.ENCODING_DFT


nhd_envars = NhdEnvars()
