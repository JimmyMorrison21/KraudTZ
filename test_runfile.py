import os.path
import unittest
from runfile import *

class Test_work(unittest.TestCase):
    def test_tick_find(self):
        self.assertEqual(type(tick_find(name='NAME',price = '1000')),type(None)) # Тестим логику, если не соотв. условию,
                                                                                # то вернется None
    def test_config_being(self):
        self.assertIsNot(os.path.exists('KraudTZ/config.json'), True) #Проверяем существование конфига

    def test_something(self):
        self.assertRaises( Exception, tick_find(name= 1000 ,price = 'NAME'))