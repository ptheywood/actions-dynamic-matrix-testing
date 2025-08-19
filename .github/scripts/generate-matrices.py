#! /usr/bin/env python3
from __future__ import annotations

import argparse
import json

"""Script to produce json of a github actions CI matrix, based on fixed versions and the type of matrix requested.

This is more complex than copy pasting lots of things, but should make updating the CI matrices simpler? 
"""

def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce a github actions job Matrix as json for the requested job")
    parser.add_argument("--type", choices=["build", "cmake", "wheel"], default="build", help="The type of matrix to produce")
    parser.add_argument("--scale", choices=["small", "medium", "big"], default="medium", help="The scale of matrix to produce")
    args = parser.parse_args()
    return args

def get_matrix(args: argparse.Namespace) -> dict[str, str]:
    CUDA_VERSIONS = ["12.0", "12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.8", "12.9", "13.0"]
       

    data = {}

    if args.type == "build":
        if args.scale == "small":
            data["cuda"] = [CUDA_VERSIONS[0]]
        elif args.scale == "medium":
            data["cuda"] = [CUDA_VERSIONS[0], CUDA_VERSIONS[-1]]
        elif args.scale == "big":
            data["cuda"] = CUDA_VERSIONS

    return data

def to_json(data: dict[str, str]) -> str:
    json_str = json.dumps(data, indent=4)
    return json_str

def main():
    args = cli()
    data = get_matrix(args)
    json_data = to_json(data)
    print(json_data)

if __name__ == "__main__":
    main()