#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\top2vec\main.py

import argparse
import sys
from pathlib import Path

from asreview.data import load_data
from asreview.entry_points import BaseEntryPoint
from asreviewcontrib.top2vec.projector import create_projector_config
from asreviewcontrib.top2vec.top2vec_clustering import run_clustering  # noqa: E501


class Top2VecEntryPoint(BaseEntryPoint):
    description = "Top2Vec clustering tools for ASReview."
    extension_name = "top2vec"

    def __init__(self):
        self.version = "0.1"

    def execute(self, argv):
        args = _parse_arguments(
            version=f"{self.extension_name}: {self.version}", argv=argv)

        if args.filepath:
            data = load_data(args.filepath)
            run_clustering(
                data,
                args.output,
                args.reduce_dimensionality,
                args.remove_abstracts,
                args.remove_urls)

        elif args.create_projector_config:
            create_projector_config(args.create_projector_config, args.metadata)

        sys.exit(1)


# check file extension
def _valid_file(fp):
    if Path(fp).suffix.lower() != ".tsv":
        raise ValueError('File must have a .tsv extension')


# argument parser
def _parse_arguments(version="Unknown", argv=None):
    parser = argparse.ArgumentParser(prog='asreview top2vec')
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-f",
        "--filepath",
        metavar="INPUT FILEPATH",
        help="processes the specified file",
        type=str,
    )
    group.add_argument(
        "-c",
        "--create_projector_config",
        metavar="INPUT FILEPATH",
        help="creates a embedding projector config file for the specified data file",
        type=str,
    )

    parser.add_argument(
        "-m",
        "--metadata",
        metavar="INPUT FILEPATH",
        help="creates a embedding projector config file for the specified metadata file",
        type=str,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + version,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="output file name",
        metavar="OUTPUT FILE NAME",
        type=str,
        default="output.tsv"
    )

    parser.add_argument(
        "--reduce_dimensionality",
        action="store_true",
        help="reduce dimensionality after top2vec",
    )

    parser.add_argument(
        "--remove_abstracts",
        action="store_true",
        help="remove abstracts (if any)",
    )

    parser.add_argument(
        "--remove_urls",
        action="store_true",
        help="remove urls (if any)",
    )

    # Exit if no arguments are given
    if len(argv) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # Check if the file extension is correct
    if args.create_projector_config is not None:
        _valid_file(args.create_projector_config)

    if args.metadata is not None:
        _valid_file(args.metadata)

    if args.output is not None:
        _valid_file(args.output)

    return args
