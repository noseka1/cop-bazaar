#!/usr/bin/env python
import logging
import os
import pprint
import requests
import sys

from model.repository import Repository
from model.category import Category

import categories
import repositories

class MarkDownOutputGenerator(object):

    __OUTPUT_DIR = "output"
    __SORT_BY_STARS = "stars"
    __SORT_BY_LAST_UPDATED = "last_updated"

    def __generate_front_page(self):
        fname  = ("%s/%s" % (self.__OUTPUT_DIR, "README.md"))
        logging.info("Writing %s", fname)
        try:
            out_file = open(fname, 'w')
            try:
                out_file.write("# Welcome to OCP Bazaar\n")
                out_file.write("\n")
                for category in Category.all:
                    out_file.write("[%s](%s)\n" % (category.title, self.__category_basename(category, self.__SORT_BY_STARS)))
            finally:
                out_file.close()
        except:
            logging.exception("Failed to write file '" + fname + "'")

    def __category_basename(self, category, sort_by):
        return ("%s.%s.md" % (category.title, sort_by)).replace('/','_')

    def __category_filename(self, category, sort_by):
        basename = self.__category_basename(category, sort_by)
        filename = ("%s/%s" % (self.__OUTPUT_DIR, basename))
        return filename

    def __write_category(self, category, sort_by):
        fname = self.__category_filename(category, sort_by)
        logging.info("Writing %s", fname)
        try:
            out_file = open(fname, 'w')
            try:
                out_file.write("# %s\n" % (category.title))
                out_file.write("\n")

                if sort_by == self.__SORT_BY_STARS:
                    sorted_repositories = sorted(category.repositories, key=lambda repo: repo.data['stargazers_count'])
                else:
                    sorted_repositories = sorted(category.repositories, key=lambda repo: repo.data['pushed_at'])

                for repo in sorted_repositories:
                    out_file.write("Name | Description | Last Updated | Stars | Forks\n")
                    out_file.write("--- | --- | --- | --- | ---\n")
                    out_file.write("[%s](%s) | %s | %s | %s | %s\n" % (
                        repo.data['repo_path'],
                        repo.data['html_url'],
                        repo.data['description'],
                        repo.data['pushed_at'],
                        repo.data['stargazers_count'],
                        repo.data['forks_count']
                    ))
                out_file.write("\n")

                if sort_by == self.__SORT_BY_STARS:
                    out_file.write("[Sort by Last Updated](%s)" %(self.__category_basename(category, self.__SORT_BY_LAST_UPDATED)))
                else:
                    out_file.write("[Sort by Stars](%s)" %(self.__category_basename(category, self.__SORT_BY_STARS)))

            finally:
                out_file.close()
        except:
            logging.exception("Failed to write file '" + fname + "'")

    def __generate_category(self, category):
        self.__write_category(category, self.__SORT_BY_STARS)
        self.__write_category(category, self.__SORT_BY_LAST_UPDATED)

    def __generate_categories(self):
        for category in Category.all:
            logging.info("Generating category %s", category.title)
            self.__generate_category(category)

    def generate_output(self):
        os.mkdir(self.__OUTPUT_DIR)
        self.__generate_front_page()
        self.__generate_categories()

class Main(object):

    def __init_logging(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    def __prepare_data(self):
        for repo in Repository.all:
            # grab info from the web
            repo.fetchRepoData()
            # add repo to the referred categories
            for category in repo.categories:
                category.repositories.append(repo)
            # add repo to the category All
            category.ALL.repositories.append(repo)

    def main(self):
        self.__init_logging()
        self.__prepare_data()
        MarkDownOutputGenerator().generate_output()

Main().main()
