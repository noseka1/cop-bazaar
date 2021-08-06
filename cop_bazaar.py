#!/usr/bin/env python3
import logging
import os
import pprint
import requests
import sys
import urllib
import yaml
from datetime import datetime

from model.repository import Repository
from model.category import Category

CONFIG = "./cop/config.yaml"


class MarkDownOutputGenerator(object):

    __OUTPUT_DIR = "./cop/output"
    __SORT_BY_STARS = "Stars"
    __SORT_BY_LAST_UPDATED = "Last Updated"

    def __category_basename(self, category, sort_by):
        return ("%s.%s.md" % (category.title, sort_by)).replace('/', '_')

    def __category_link(self, category, sort_by):
        return urllib.parse.quote(self.__category_basename(category, sort_by))

    def __category_filename(self, category, sort_by):
        basename = self.__category_basename(category, sort_by)
        filename = ("%s/%s" % (self.__OUTPUT_DIR, basename))
        return filename

    def __add_sort_by_link(self, out_file, category, sort_by):
        if sort_by == self.__SORT_BY_STARS:
            out_file.write("[Sort by Last Updated](%s)" % (
                self.__category_link(category, self.__SORT_BY_LAST_UPDATED)))
        else:
            out_file.write("[Sort by Stars](%s)" % (
                self.__category_link(category, self.__SORT_BY_STARS)))

    def __write_category(self, category, sort_by):
        fname = self.__category_filename(category, sort_by)
        logging.info("Writing %s", fname)
        try:
            out_file = open(fname, 'w')
            try:
                out_file.write("# %s by %s\n" % (category.title, sort_by))
                out_file.write("\n")

                if sort_by == self.__SORT_BY_STARS:
                    sorted_repositories = sorted(
                        category.repositories,
                        key=lambda repo: repo.data['stargazers_count'],
                        reverse=True)
                else:
                    sorted_repositories = sorted(
                        category.repositories,
                        key=lambda repo: repo.data['pushed_at'],
                        reverse=True)

                self.__add_sort_by_link(out_file, category, sort_by)
                out_file.write("\n")
                out_file.write("\n")

                out_file.write("Name | Description | Last Updated | Stars \n")
                out_file.write("--- | --- | --- | --- \n")

                for repo in sorted_repositories:
                    description = repo.data['description']
                    if description is not None:
                        description = description.replace("|", "\|")
                    out_file.write("[%s](%s) | %s | %s | %s \n" % (
                        repo.data['repo_path'],
                        repo.data['html_url'],
                        description,
                        repo.data['pushed_at'][0:len('2020-01-01')],
                        repo.data['stargazers_count']
                    ))
                out_file.write("\n")

                self.__add_sort_by_link(out_file, category, sort_by)

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

    def __generate_front_page(self):
        fname = ("%s/%s" % (self.__OUTPUT_DIR, "README.md"))
        logging.info("Writing %s", fname)
        try:
            out_file = open(fname, 'w')
            try:
                out_file.write(
                    "# Welcome to OpenShift Bazaar Source Code Index\n")
                out_file.write("\n")
                out_file.write(
                    "This is a catalog of OpenShift related projects created by Red Hatters.\n")
                out_file.write("\n")
                out_file.write("## Choose a category\n")
                for category in Category.all:
                    out_file.write("* [%s](%s) - %s\n" % (category.title, self.__category_link(category, self.__SORT_BY_STARS),
                                                          category.desc))
                out_file.write("\n")
                out_file.write("## Contributing\n")
                out_file.write("If you would like to add your project to the catalog, clone the https://github.com/noseka1/cop-bazaar"
                               " git repository, include your project in the *config.yaml* file and submit your change as a pull request.\n")
                out_file.write("\n")
                out_file.write("Last updated %s" %
                               (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            finally:
                out_file.close()
        except:
            logging.exception("Failed to write file '" + fname + "'")

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
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    def __load_config(self):
        with open(CONFIG) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

    def __prepare_data(self, config):
        categories = {"all": Category("All", "All projects.")}

        for category_yaml in config['categories']:
            categories[category_yaml['name']] = Category(
                category_yaml['title'], category_yaml['desc'])

        for repo_yaml in config['repositories']:
            repo = Repository(repo_yaml['url'])
            for category_yaml in repo_yaml['categories']:
                repo.categories.append(categories[category_yaml])
            # grab info from the web
            repo.fetchRepoData()
            # add repo to the referred categories
            for category in repo.categories:
                category.repositories.append(repo)
            # add repo to the category All
            categories['all'].repositories.append(repo)

    def main(self):
        self.__init_logging()
        config = self.__load_config()
        self.__prepare_data(config)
        MarkDownOutputGenerator().generate_output()


Main().main()
