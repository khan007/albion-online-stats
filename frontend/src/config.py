import os
import sys
import toml

CFG_VERSION = '0.5'

default = """
[window]
width = 300
height = 220
font-size = '10px'
opacity = 0.8

[app]

[config]
# do not change
version = '%s'
""" % (CFG_VERSION)


_script_path = sys.argv[0]  # pyinstaller creates tmpdir for python files, thus this is the way to get executable path
_config = None

def config():
    global _script_path
    global _config

    if _config:
        return _config

    conf_file = os.path.join(os.path.dirname(
        _script_path), 'albion-online-stats.cfg')

    try:
        with open(conf_file, "r") as cfg_file:
            cfg = toml.load(cfg_file)
            if cfg['config']['version'] != CFG_VERSION:
                raise Exception('Version changed')
            return cfg
    except(Exception) as e:
        with open(conf_file, "w") as cfg_file:
            cfg_file.write(default)
            return toml.loads(default)

    return {}
