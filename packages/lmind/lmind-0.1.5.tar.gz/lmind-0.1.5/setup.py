# coding:utf-8
from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="lmind",
    install_requires=[
        "PTable>=0.9.2",
    ],
    # not cover the tasks.csv and conf.csv files when upgrate
    # package_data = {
    #     '': ['*.csv'],
    # }
)

