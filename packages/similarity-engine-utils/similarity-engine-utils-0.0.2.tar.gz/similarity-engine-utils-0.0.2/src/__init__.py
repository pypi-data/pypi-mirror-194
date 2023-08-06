from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Version of the similarity-engine-utils package
__version__ = "0.0.2"

# Read package main configs
_cfg = tomllib.loads(resources.read_text("milvus", "config.toml"))
MILVUS_HOST = _cfg["milvus"]["host"]
