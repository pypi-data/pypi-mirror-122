from data_base import SqlDB
import unittest
import pandas as pd

class TableExistsTestCase(unittest.TestCase):
    def test_tableExists(self):
        self.config_sql = SqlDB()
        self.dataTables = ['stock_content','stock_headlines','stock_sentiment']


        for dataTable in self.dataTables:
            actual_value = self.config_sql.tableExists(table_name=str(dataTable))
            self.assertIsInstance(actual_value, bool)
            # self.assertEqual(expected_values, actual_value)

unittest.main(argv=[''], verbosity=2, exit=False)

class RetreiveDataTableTestCase(unittest.TestCase):
    def test_retriveTableInfo(self):
        self.config_sql = SqlDB()
        self.dataTables = ['stock_content','stock_headlines','stock_sentiment']
        expected_values = pd.DataFrame

        for dataTable in self.dataTables:
            actual_value = self.config_sql.retriveTableInfo(table_name=str(dataTable))
            self.assertEqual(expected_values, actual_value)

class createTableTestCase(unittest.TestCase):
    
    def test_createTable(self):
        self.config_sql = SqlDB()
        self.dataTables = ['stock_content','stock_headlines','stock_sentiment']
        expected_values = pd.DataFrame

        for dataTable in self.dataTables:
            actual_value = self.config_sql.createTable(table_name=str(dataTable))
            self.assertEqual(expected_values, actual_value)

class appendDataTestCase(unittest.TestCase):
    
    def test_appendData(self):
        self.config_sql = SqlDB()
        self.dataTables = ['stock_content','stock_headlines','stock_sentiment']
        expected_values = pd.DataFrame

        for dataTable in self.dataTables:
            actual_value = self.config_sql.appendData(table_name=str(dataTable))
            self.assertEqual(expected_values, actual_value)

class getNewRowsTestCase(unittest.TestCase):
    
    def test_getNewRows(self):
        config_sql = SqlDB()
        self.new_dt = pd.DataFrame({'a':[1,2], 'b':[3,4],'c':[5,6]})
        self.source_dt = pd.DataFrame({'a':[1,2], 'b':[3,4]})
        expected_values = pd.DataFrame
        actual_value= config_sql.getNewRows(new_dt=self.new_dt,source_dt=self.source_dt)
        self.assertEqual(expected_values,actual_value)
        