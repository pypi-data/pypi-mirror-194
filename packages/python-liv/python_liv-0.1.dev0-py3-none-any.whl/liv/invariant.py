from dataclasses import dataclass

import yaml
from pycparser.plyparser import Coord


@dataclass
class Invariant:
    formula: str
    coord: Coord


def from_yaml(entry):
    coord = Coord(
        entry["location"]["file_name"],
        entry["location"]["line"],
        entry["location"]["column"],
    )
    return Invariant(formula=entry["loop_invariant"]["string"], coord=coord)


def load_loop_invariants(witnesspath):
    with open(witnesspath, "r") as witnessfile:
        witnessentries = yaml.safe_load(witnessfile)
    return [
        from_yaml(entry)
        for entry in witnessentries
        if entry["entry_type"] == "loop_invariant"
    ]
