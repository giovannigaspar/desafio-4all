import unittest
import json
from app import main_route
from db import get_dict_resultset, ALL


class MyTest(unittest.TestCase):
    def test_01_insert(self):
        r = main_route('tests/test1.txt') + main_route('tests/test2.txt')
        print('\n\n'+str(r)+' itens inseridos no banco de dados!')

    def test_02_select(self):
        sql = '''
            SELECT * FROM RESULTADOS
        '''
        r = get_dict_resultset(sql, None, ALL)
        f = open("log.json", "w")
        print('\n\nAbra o arquivo "log.json" em '+
                'um navegador para verificar os dados inseridos!')
        f.write(json.dumps(r))

    def test_03_delete(self):
        sql = '''
            DELETE FROM RESULTADOS
        '''
        get_dict_resultset(sql, None, None)
        print('\n\nBanco de dados apagado!')


if __name__ == '__main__':
    unittest.main()
