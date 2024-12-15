#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\semantic_clustering\main.py

import argparse
import sys

import webbrowser
from pathlib import Path

from asreview.data import load_data
from asreview.entry_points import BaseEntryPoint
from asreviewcontrib.semantic_clustering.interactive import run_app
from asreviewcontrib.semantic_clustering.semantic_clustering import run_clustering_steps  # noqa: E501


class SemClusEntryPoint(BaseEntryPoint):
    description = "Semantic clustering tools for ASReview."
    extension_name = "semantic_clustering"

    def __init__(self):
        self.version = "0.1"

    def execute(self, argv):
        args = _parse_arguments(
            version=f"{self.extension_name}: {self.version}", argv=argv)

        if args.filepath:
            data = load_data(args.filepath)
            run_clustering_steps(
                data,
                args.output,
                args.reduce_dimensionality,
                args.remove_abstracts,
                args.remove_urls)

        elif args.app:
            run_app(args.app, args.metadata)

        sys.exit(1)


# check file extension
def _valid_file(fp):
    if Path(fp).suffix.lower() != ".tsv":
        raise ValueError('File must have a .tsv extension')


# argument parser
def _parse_arguments(version="Unknown", argv=None):
    parser = argparse.ArgumentParser(prog='asreview semantic_clustering')
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-f",
        "--filepath",
        metavar="INPUT FILEPATH",
        help="processes the specified file",
        type=str,
    )
    group.add_argument(
        "-a",
        "--app",
        metavar="INPUT FILEPATH",
        help="runs the app from a file created with the semantic clustering "
        "extension",
        type=str,
    )

    parser.add_argument(
        "-m",
        "--metadata",
        metavar="INPUT FILEPATH",
        help="runs the app from a file created with the semantic clustering "
        "extension metadata",
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
        "--transformer",
        help="select a transformer to use",
        metavar="TRANSFORMER",
        type=str,
        default='allenai/scibert_scivocab_uncased'
    )

    parser.add_argument(
        "--reduce_dimensionality",
        action="store_true",
        help="reduce dimensionality after top2vec",
    )

    parser.add_argument(
        "--remove_abstracts",
        action="store_true",
        help="remove abstracts",
    )

    parser.add_argument(
        "--remove_urls",
        action="store_true",
        help="remove urls",
    )

    # Exit if no arguments are given
    if len(argv) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # Check if the file extension is correct
    # if args.app is not None:
        # _valid_file(args.app)

    if args.output is not None:
        _valid_file(args.output)

    return args
