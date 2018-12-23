#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import importlib
from mongoengine import connection

from app.command.importer import *
from app import config

db = connection.connect(db=config.DB_NAME, port=int(config.DB_PORT))


def main(args):
    handler = getattr(
        importlib.import_module("app.command.importer"),
        '{}_handler'.format(args.type).title().replace('_', '')
    )
    Importer(handler=handler(), source=args.file_name).process()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description="Import data"
    )
    arg_parser.add_argument("-t", "--type", dest="type",
                            help="type can be [manufacturer, brand, model]",
                            required=True
                            )
    arg_parser.add_argument("-f", "--file", dest="file_name",
                            help="csv file name",
                            required=True)
    args = arg_parser.parse_args()

    main(args)
