#!/usr/bin/env python

import logging
import pprint
import requests
import sys

from model.repository import Repository
from model.category import Category

import categories
import repositories

class Main(object):

    def init_logging(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    def main(self):
        self.init_logging()

        for repo in Repository.all:
            repo.fetchRepoData()
            for category in repo.categories:
                category.repositories.append(repo)

        for category in Category.all:
            print(category.title)
            for repo in category.repositories:
                print(repo.__dict__)

Main().main()
