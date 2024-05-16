from argparse import ArgumentParser
from pathlib import Path

from .toolkit import log_metadata


savemeta_parser = ArgumentParser(
    prog="pyrtoolkit:save-meta",
    sage="python3 -m pyrtoolkit.save-meta ",
    description="save current metadata as meta.toml"
)
savemeta_parser.add_argument("outdir", type=Path, default=Path.cwd())
savemeta_parser.add_argument("repodir", type=Path, default=Path.cwd())
savemeta_parser.add_argument("description", type=str, default="")

def savemeta():
    args = savemeta_parser.parse_args()
    log_metadata(
        root_folder=args.repodir,
        output_folder=args.outir,
        description=args.description
    )