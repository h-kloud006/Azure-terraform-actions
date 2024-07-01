import unittest
import json
from utils.all_utils import read_config
from data_ingestion.partition import data_partition

import os

class TestPartitionDocx(unittest.TestCase):
    def test_partition_docx(self):
        print('Unit test for partition started')
        config_path = "./config/config.yaml"
        config = read_config(config_path)
        partition_config = config["partitioning"]
        
        partition_obj = data_partition(config_path)
        elements = partition_obj.process(data_path=partition_config['unittest_data_path'])
        
        text_elements = []
        table_elements = []
        for element in elements:
            if element.metadata['type'] == 'text':
                text_elements.append(element)
            elif element.metadata['type'] == 'table':
                table_elements.append(element)
        
        res_dict = {'text_elements': len(text_elements), 'table_elements': len(table_elements)}
        
        with open(r'./test_cases/data_ingestion/partition_dict.json', 'r') as f:
            reference_dict = json.load(f)
        # Add assertions here
        # For example, if partition_docx is supposed to return a list, you can check if result is a list
        self.assertEqual(res_dict['text_elements'], reference_dict['text_elements'], 'Text Elements doesnot match')
        print('\n- Unittest for Text Elements passed')
        self.assertEqual(res_dict['table_elements'], reference_dict['table_elements'], 'Table Elements doesnot match')
        print('\n- Unittest for Table Elements passed')
        print('\n -- Unittest for partition passed -- ')

if __name__ == '__main__':
    obj = TestPartitionDocx()
    obj.test_partition_docx()