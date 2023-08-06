import unittest
import pandas as pd

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from stock_scraper import process

class ProcessTestCase(unittest.TestCase):

    def tableExitsCheck(self):
        self.tableExists = process.tableExitsCheck
        