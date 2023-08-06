from __future__ import annotations

import json
import logging
from pathlib import Path

import typer

from module_qc_analysis_tools.cli.globals import CONTEXT_SETTINGS, OPTIONS

log = logging.getLogger(__name__)

stack = []


def lookup(input_dict, search_key):
    # recursion to look up the desired key in a dict and record the path
    for k, v in input_dict.items():
        if k == search_key:
            return v
        elif isinstance(v, dict):
            _v = lookup(v, search_key)
            if _v is not None:
                stack.append(k)
                return _v


def overwrite(in_file, config_file):
    with config_file.open() as jsonFile:
        config_file_data = json.load(jsonFile)
    with in_file.open() as jsonFile:
        in_file_data = json.load(jsonFile)

    original_par = lookup(config_file_data, "Parameter")

    if original_par is None:
        raise KeyError(f"Parameter not found in config file {config_file}! ")

    # Check if chip name matched
    if in_file_data["Identifiers"]["Name"] != original_par["Name"]:
        raise KeyError("Chip name mismatched! Please check the input")

    # overwrite the Parameter part
    for k, v in in_file_data.items():
        if k in original_par.keys():
            log.info(f"[{k}] Change from {original_par[k]} to {v}")
            original_par[k] = v

    stack.reverse()

    part_config_file_data = config_file_data
    for k in stack:
        part_config_file_data = part_config_file_data[k]
    part_config_file_data["Parameter"] = original_par

    with config_file.open("w") as jsonFile:
        json.dump(config_file_data, jsonFile, indent=4)


app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    input_file: Path = OPTIONS["input_file"], config_file: Path = OPTIONS["config_file"]
):
    overwrite(input_file, config_file)


if __name__ == "__main__":
    typer.run(main)
