"""
Setup and commands for the Scribe-Data command line interface.

.. raw:: html
    <!--
    * Copyright (C) 2024 Scribe
    *
    * This program is free software: you can redistribute it and/or modify
    * it under the terms of the GNU General Public License as published by
    * the Free Software Foundation, either version 3 of the License, or
    * (at your option) any later version.
    *
    * This program is distributed in the hope that it will be useful,
    * but WITHOUT ANY WARRANTY; without even the implied warranty of
    * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    * GNU General Public License for more details.
    *
    * You should have received a copy of the GNU General Public License
    * along with this program.  If not, see <https://www.gnu.org/licenses/>.
    -->
"""

#!/usr/bin/env python3
import argparse

from .list import list_wrapper
from .query import query_data

LIST_DESCRIPTION = "List languages, word types and combinations of each that Scribe-Data can be used for."
QUERY_DESCRIPTION = "Query data from Wikidata for the given languages and word types."
TOTAL_DESCRIPTION = "Check Wikidata for the total available data for the given languages and word types."
CONVERT_DESCRIPTION = "Convert data returned by Scribe-Data to different file types."
CLI_EPILOG = "Visit the codebase at https://github.com/scribe-org/Scribe-Data and documentation at https://scribe-data.readthedocs.io/en/latest/ to learn more!"


def main() -> None:
    # MARK: CLI Base

    parser = argparse.ArgumentParser(
        prog="Scribe-Data",
        description="The Scribe-Data CLI is a tool for extracting language data from Wikidata and other sources.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
        epilog=CLI_EPILOG,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser._actions[0].help = "Show this help message and exit."
    parser.add_argument(
        "-v", "--verbose", help="Increase output verbosity.", action="store_true"
    )
    parser.add_argument("-u", "--update", help="Update the Scribe-Data CLI.")

    # MARK: List

    list_parser = subparsers.add_parser(
        "list",
        aliases=["l"],
        help=LIST_DESCRIPTION,
        description=LIST_DESCRIPTION,
        epilog=CLI_EPILOG,
    )
    list_parser._actions[0].help = "Show this help message and exit."
    list_parser.add_argument(
        "--language",
        "-lang",
        nargs="?",
        const=True,
        help="Run list command on all or given languages.",
    )
    list_parser.add_argument(
        "--word-type",
        "-wt",
        nargs="?",
        const=True,
        help="Run list command on all or given word types.",
    )

    # MARK: Query

    query_parser = subparsers.add_parser(
        "query",
        aliases=["q"],
        help=QUERY_DESCRIPTION,
        description=QUERY_DESCRIPTION,
        epilog=CLI_EPILOG,
    )
    query_parser._actions[0].help = "Show this help message and exit."
    query_parser.add_argument(
        "-lang", "--language", type=str, help="The language(s) to query."
    )
    query_parser.add_argument(
        "-wt", "--word-type", type=str, help="The word type(s) to query."
    )
    query_parser.add_argument(
        "-od", "--output-dir", type=str, help="The output directory path for results."
    )
    query_parser.add_argument(
        "-ot",
        "--output-type",
        type=str,
        choices=["json", "csv", "tsv"],
        help="The output file type.",
    )
    query_parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Whether to overwrite existing files (default: False).",
    )

    # MARK: Total

    total_parser = subparsers.add_parser(
        "total",
        aliases=["t"],
        help=TOTAL_DESCRIPTION,
        description=TOTAL_DESCRIPTION,
        epilog=CLI_EPILOG,
    )
    total_parser._actions[0].help = "Show this help message and exit."
    total_parser.add_argument(
        "-lang", "--language", type=str, help="The language(s) to check totals for."
    )
    total_parser.add_argument(
        "-wt", "--word-type", type=str, help="The word type(s) to check totals for."
    )

    # MARK: Convert

    convert_parser = subparsers.add_parser(
        "convert",
        aliases=["c"],
        help=CONVERT_DESCRIPTION,
        description=CONVERT_DESCRIPTION,
        epilog=CLI_EPILOG,
    )
    convert_parser._actions[0].help = "Show this help message and exit."
    convert_parser.add_argument(
        "-f", "--file", type=str, help="The file to convert to a new type."
    )
    convert_parser.add_argument(
        "-ko",
        "--keep-original",
        action="store_false",
        help="Whether to keep the file to be converted (default: True).",
    )
    convert_parser.add_argument(
        "-json", "--to-json", type=str, help="Convert the file to JSON format."
    )
    convert_parser.add_argument(
        "-csv", "--to-csv", type=str, help="Convert the file to CSV format."
    )
    convert_parser.add_argument(
        "-tsv", "--to-tsv", type=str, help="Convert the file to TSV format."
    )
    convert_parser.add_argument(
        "-sqlite", "--to-sqlite", type=str, help="Convert the file to SQLite format."
    )

    # MARK: Setup CLI

    args = parser.parse_args()

    if args.command in ["list", "l"]:
        list_wrapper(args.language, args.word_type)

    elif args.command in ["query", "q"]:
        query_data(
            args.language,
            args.word_type,
            args.output_dir,
            args.overwrite,
            args.output_type,
        )

    elif args.command in ["total", "t"]:
        return

    elif args.command in ["convert", "c"]:
        return

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
