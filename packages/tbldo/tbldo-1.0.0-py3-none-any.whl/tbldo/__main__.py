#!/usr/bin/env python3

import argparse
import subprocess as sp
from concurrent.futures import ThreadPoolExecutor
import itertools as it
import warnings as wn
import pathlib as pl

from sqlalchemy import create_engine, text
import pandas as pd

COMMAND_HELP = "The command to run and apply substitutions to"


def _run_sql_row(row, colnames, command, verbose):
    substitutions = {key: value for key, value in zip(colnames, row)}
    command = command.format(**substitutions)
    if verbose:
        print(command)
    sp.run(command, shell=True)


def _run_df_row(row, verbose):
    command = row["__COMMAND__"]
    del row["__COMMAND__"]
    for key, value in row.items():
        new_command = command.replace(f"{{{key}}}", value)
        if new_command == command:
            wn.warn(
                f"{key} was found in row columns but not in command substitution patterns"
            )
        command = new_command
    if verbose:
        print(command)
    sp.run(command, shell=True)


def dfdoer(dframe, threads=1, verbose=False):
    with ThreadPoolExecutor(threads) as executor:
        return list(
            executor.map(
                _run_df_row, (item[1] for item in dframe.iterrows()), it.repeat(verbose)
            )
        )


def sqldo(args):
    engine = create_engine(args.db)
    conn = engine.connect()
    query = args.query
    query_path = pl.Path(query)
    if query_path.exists():
        with open(query_path) as fo:
            query = fo.read()

    statements = query.split(";")[0:-1]
    for statement in statements:
        query_result = conn.execute(text(statement))

    description = query_result.cursor.description
    colnames = [item[0] for item in description]

    with ThreadPoolExecutor(args.threads) as executor:
        return list(
            executor.map(
                _run_sql_row,
                query_result,
                it.repeat(colnames),
                it.repeat(args.command),
                it.repeat(args.verbose),
            )
        )


def csvdo(args):
    dframe = pd.read_csv(args.csv, delimiter=args.delimeter)
    dframe["__COMMAND__"] = args.command
    return dfdoer(dframe, args.threads, args.verbose)


def main():
    parser = argparse.ArgumentParser(
        description="Table-do. Run a command, substituting in values according to a table structure."
    )

    subparsers = parser.add_subparsers()

    parser_csv = subparsers.add_parser("csv", help="csv input help")
    parser_csv.add_argument("command", help=COMMAND_HELP)
    parser_csv.add_argument("csv", help="Path to the csv file")
    parser_csv.add_argument("--delimeter", default=",", help="The delimiter to use")
    parser_csv.set_defaults(func=csvdo)

    parser_sql = subparsers.add_parser("sql", help="sql input help")
    parser_sql.add_argument("command", help=COMMAND_HELP)
    parser_sql.add_argument("db", help="database connection string")
    parser_sql.add_argument(
        "query",
        help="The sql query that returns the table to be used. If query is an existing file, it uses the contents of the file as the query.",
    )
    parser_sql.set_defaults(func=sqldo)

    parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Number of threads to use to kick off the commands",
    )
    parser.add_argument(
        "--verbose", help="Print out command being run.", action="store_true"
    )

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
