from pathlib import Path
import importlib.resources

import nygen.data
from nygen.conf import load_conf
from nygen.lib.formatter import Formatter
from nygen.lib.conda import create_conda, conda_exists
from nygen.lib.exceptions import DestinationExistsException, CondaEnvironmentExistsException


def is_dir_empty(p: Path) -> bool:
    try:
        next(p.iterdir())
        is_empty = False
    except StopIteration:
        is_empty = True
    return is_empty


def precheck_dst(dstpath: Path) -> None:
    if dstpath.exists() and not is_dir_empty(dstpath):
        raise DestinationExistsException(f"Destination path not empty: {dstpath.absolute()}")


def precheck_conda(name):
    if conda_exists(name):
        raise CondaEnvironmentExistsException(f"Conda environment already exists: {name}")


def gen_project(name, cmd_vars: dict[str, str]):
    print(f"Generating project {name}")
    conf, conf_vars = load_conf()
    formatter = Formatter()
    formatter["name"] = name
    formatter.load(cmd_vars=cmd_vars, conf_vars=conf_vars)

    dst_root = Path(name)

    formatter.fill_defaults()

    formatter.precheck()
    precheck_dst(dst_root)
    precheck_conda(name)

    print(f"Creating conda environment {name!r} with Python {formatter['python']}")
    python_path = create_conda(name, formatter["python"])
    formatter["python_path"] = repr(python_path)

    print("Generating file structure")
    for src, dst in map_paths(dst_root, formatter):
        gen_file(src, dst, formatter)

    print(f"Successfully created project at {dst_root.absolute()}")


def map_paths(dst_root: Path, formatter: Formatter) -> list[tuple[Path, Path]]:
    src_root: Path = importlib.resources.files(nygen.data) / "template"
    srcs = [p for p in src_root.rglob("*") if not (p.name == "__pycache__" or p.suffix == ".pyc") and p.is_file()]
    path_maps = [(src, map_path(src, src_root, dst_root, formatter)) for src in srcs]
    return path_maps


def map_path(src: Path, src_root: Path, dst_root: Path, formatter: Formatter):
    rel_src = src.relative_to(src_root)
    rel_src = Path(formatter.format(str(rel_src)))
    dst = dst_root / rel_src
    return dst


def gen_file(src: Path, dst: Path, formatter: Formatter):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(formatter.format(src.read_text()))
