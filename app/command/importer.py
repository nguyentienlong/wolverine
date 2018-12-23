#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mongoengine import NotUniqueError

from app import log
from abc import abstractmethod, ABC
from app.model import Manufacturer, Brand, Model

import csv


logger = log.get_logger()


class Importer(object):
    def __init__(self, handler, source):
        self._handler = handler
        self._source = source

    def process(self):
        self._handler.handle(self._source)


class AbstractHandler(ABC):
    @abstractmethod
    def handle(self, source):
        pass


class ManufacturerHandler(AbstractHandler):
    def handle(self, source):
        doc_count = 0
        try:
            with open(source) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    manufacturer = Manufacturer()
                    manufacturer.name = (row['name']).lower()
                    manufacturer.popularity = row['popularity']
                    try:
                        manufacturer.save()
                        doc_count += 1
                    except NotUniqueError as e:
                        logger.error(e)
                        continue
        except Exception as e:
            logger.error(e)
        logger.info('{} manufacturers imported'.format(doc_count))


class BrandHandler(AbstractHandler):
    def handle(self, source):
        doc_count = 0
        try:
            with open(source) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['brand']:
                        manufacturer = Manufacturer.objects(
                            name=(row['manufacturer']).lower()
                        ).first()
                        if isinstance(manufacturer, Manufacturer):
                            brand = Brand()
                            brand.name = (row['brand']).lower()
                            brand.popularity = row['popularity']
                            brand.manufacturer = row['manufacturer'].lower()
                            try:
                                brand.save()
                                doc_count += 1
                            except NotUniqueError as e:
                                logger.error(e)
                                continue
                        else:
                            logger.info("Manufacturer {} is not existed".
                                        format(row['manufacturer']))
        except Exception as e:
            logger.error(e)
        logger.info('{} brands imported'.format(doc_count))


class ModelHandler(AbstractHandler):
    def handle(self, source):
        doc_count = 0
        try:
            with open(source) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    model = Model()
                    model.name = (row['name']).lower()
                    model.popularity = row['popularity']
                    try:
                        model.save()
                        doc_count += 1
                    except NotUniqueError as e:
                        logger.error(e)
                        continue
        except Exception as e:
            logger.error(e)
        logger.info('{} models imported'.format(doc_count))
