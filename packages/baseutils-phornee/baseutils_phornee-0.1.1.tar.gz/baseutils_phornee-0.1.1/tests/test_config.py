import unittest
import os
import sys
import yaml
from pathlib import Path
from baseutils_phornee import Config
import shutil

import logging

log = logging.getLogger('baseutils_phornee')
sh = logging.StreamHandler(sys.stdout)
log.addHandler(sh)
log.setLevel(logging.INFO)


class Testing(unittest.TestCase):

    def test_yaml_merge_dictionary(self):
        # Root is dictionary
        config_template = {'single': 'singlevalue',
                           'singlemerge': 'template',
                           'fruits': ['orange', 'apple', 'banana']}
        config1 = {'vehicles': ['car', 'truck'],
                   'fruits': ['mango'],
                   'single2': 'singlevalue2',
                   'singlemerge': 'second'}
        Config._mergeConfig(config1, config_template)

        expected_value = {'single': 'singlevalue',
                          'singlemerge': 'second',
                          'fruits': ['orange', 'apple', 'banana', 'mango'],
                          'vehicles': ['car', 'truck'],
                          'single2': 'singlevalue2'}

        self.assertEqual(config_template, expected_value)
   
    def test_yaml_merge_list(self):
        # Root is list
        config_template = [
                            {'single': 'singlevalue',
                             'singlemerge': 'template',
                             'fruits': ['orange', 'apple', 'banana']},
                            {'single2': 'singlevalue2',
                             'singlemerge2': 'template',
                             'fruits2': ['mango', 'lemon', 'banana']},
                           ]
        config_mismatch = {'test': 'test'}
        try:
            Config._mergeConfig(config_mismatch, config_template)
        except Exception as e:
            self.assertTrue("Exception raised when trying to merge dict and list: expected result.")
        else:
            self.assertFalse("Exception should be raised, and was not.")

        config_template2 = [
                            {'single3': 'singlevalue',
                             'singlemerge': 'template',
                             'fruits': ['orange', 'apple', 'banana']}
                           ]
        Config._mergeConfig(config_template2, config_template)

        expected_merge = [
                            {'single': 'singlevalue',
                             'singlemerge': 'template',
                             'fruits': ['orange', 'apple', 'banana']},
                            {'single2': 'singlevalue2',
                             'singlemerge2': 'template',
                             'fruits2': ['mango', 'lemon', 'banana']},
                            {'single3': 'singlevalue',
                             'singlemerge': 'template', 
                             'fruits': ['orange', 'apple', 'banana']}]
        self.assertEqual(config_template, expected_merge)

    def test_from_scrath(self):
        # Remove config file, to start from scratch
        var_config_path = Config.getConfigPath('baseutils_tests', 'config_new.yml')
        if os.path.exists(var_config_path):
            os.remove(Config.getConfigPath('baseutils_tests', 'config_new.yml'))

        # Instatiate a config file from scratch, based only on template
        # Will be automatically writen to file
        template_path = '{}/data/config_template.yml'.format(Path(__file__).parent)
        config = Config(package_name='baseutils_tests', 
                        template_path=template_path, 
                        config_file_name='config_new.yml')
        
        try:
            # Check that resulting config file equals the template file
            with open(var_config_path, 'r') as config_file:
                config_read = yaml.load(config_file, Loader=yaml.FullLoader)
                with open(template_path, 'r') as template_config_file:
                    template_config_read = yaml.load(template_config_file, Loader=yaml.FullLoader)
                    self.assertEqual(config_read, template_config_read)
        except Exception as e:
            self.assertFalse('File not found: {}'.format(e))
        finally:
            os.remove(Config.getConfigPath('baseutils_tests', 'config_new.yml'))

    def test_update_config(self):
        # Copy already-made config to var destination
        existing_path = '{}/data/config_existing.yml'.format(Path(__file__).parent)
        var_config_path = Config.getConfigPath('baseutils_tests', 'config_existing.yml')
        shutil.copy(existing_path, var_config_path)

        # Instatiate a config file from scratch, with an updated template, with an existing config
        template_path = '{}/data/config_template.yml'.format(Path(__file__).parent)
        config = Config(package_name='baseutils_tests', 
                        template_path=template_path, 
                        config_file_name='config_existing.yml')

        expected_merged = {'key_template1': 'template', 
                           'key_template2': 'changed', 
                           'key_template3': 'new in config'}

        # Check memory matches
        self.assertEqual(config.getDict(), expected_merged)

        config.write()

        try:
            # Check that resulting config file equals the template file
            with open(var_config_path, 'r') as config_file:
                config_read = yaml.load(config_file, Loader=yaml.FullLoader)
                expected_merged = {'key_template1': 'template',
                                   'key_template2': 'changed',
                                   'key_template3': 'new in config'}
                self.assertEqual(config_read, expected_merged)
        except Exception as e:
            self.assertFalse('File not found: {}'.format(e))
        finally:
            os.remove(Config.getConfigPath('baseutils_tests', 'config_existing.yml'))


if __name__ == '__main__':
    unittest.main()
