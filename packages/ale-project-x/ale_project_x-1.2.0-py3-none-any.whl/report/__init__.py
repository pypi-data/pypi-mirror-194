from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "0.0.1"

_reportCfg = tomllib.loads(resources.read_text("report", "config.toml"))
INPUT_FOLDER = _reportCfg['path']['inputFolder']
OUTPUT_FOLDER = _reportCfg['path']['outputFolder']

print(INPUT_FOLDER)
