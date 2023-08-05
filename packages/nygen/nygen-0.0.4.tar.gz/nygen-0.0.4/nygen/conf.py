from pathlib import Path

import appdirs
import toml
from nconf import config

from nygen.lib.formatter import Formatter


appname = "nygen"
appauthor = "nfearnley"
datadir = Path(appdirs.user_data_dir(appname, appauthor))
confpath = datadir / f"{appname}.conf"


@config
class NygenConf:
    pass


def load_conf() -> tuple[NygenConf, dict[str, any]]:
    try:
        with confpath.open("r") as f:
            data = toml.load(f)
    except FileNotFoundError:
        data = {}
    conf = NygenConf.load(data)

    return conf, data


def init_conf(conf_vars: dict[str, str]):
    formatter = Formatter()
    formatter.load(conf_vars=conf_vars)
    confpath.parent.mkdir(parents=True, exist_ok=True)
    with confpath.open("w") as f:
        toml.dump(formatter.to_conf(), f)
    return confpath
