__author__ = "Giovanni Gaspar"
__copyright__ = ""
__version__ = "0.1"
__maintainer__ = "Giovanni Gaspar"
__email__ = "giovannigaspar@outlook.com"
__status__ = "Development"


import time, os


# Importando conexão e métodos do banco de dados
from db import get_dict_resultset, ONE

# Biblioteca de geolocalização open source: https://github.com/geopy/geopy
from geopy.geocoders import Nominatim


# Inicializando a biblioteca (sintaxe padrão)
geolocator = Nominatim(user_agent="desafio_4all")


def read_coordinates_file(filename, debug=False):
    """
    Leitura de coordenadas a partir de um arquivo.
    Obtém as informações pertinentes de um arquivo (latitude e longitude) e
    retorna um array em forma de dicionário.


    :param filename: nome do arquivo (caminho completo + nome)

    :param debug: utilizado para imprimir as coordenadas conforme são obtidas
    como forma de debug


    :return: Dicionário contendo as informações no formato
    [{'lat':'y', 'lon':'x'}]
    """
    coordinates = []
    with open(filename, 'r', newline='') as f:
        content = f.readlines()
        for idx, line in enumerate(content):
            # Como nem sempre existe a linha "distance", esse código gera erro
            #if (idx+1) % 3 == 0:
            #    coordinates.append({
            #        'lat': content[idx-2].split('   ')[1].rstrip('\n'),
            #        'lon': content[idx-1].split('   ')[1].rstrip('\n')
            #    })
            # Como existe um padrão em que sempre há Latitude e Longitude, essa
            # forma funcionou melhor
            if len(line.split('Longitude:')) > 1:
                # Foi necessária essa linha, pois existem casos que não há
                # latitude e longitude no arquivo de texto
                if len(content[idx-1].split('Latitude')) > 1:
                    coordinates.append({
                        'lat': content[idx-1].split('   ')[1].rstrip('\n'),
                        'lon': content[idx].split('   ')[1].rstrip('\n')
                    })
    if debug:
        print(coordinates)
    return coordinates


def get_locations(coordinates, debug=False):
    """
    Obtém informações de um local (endereço, CEP, bairro, etc) a partir de
    coordenadas (latitude e longitude) geográficas.


    :param coordinates: coordenadas a serem verificadas. Espera-se que estejam
    no padrão [{'lat':'y', 'lon':'x'}]

    :param debug: utilizado para imprimir as informações do local como forma de
    debug

    :return: JSON contendo as informações do local pesquisado
    """
    points = coordinates['lat'] + ', ' + coordinates['lon']
    try:
        location = geolocator.reverse(points)
        if debug:
            print(location.raw)
        time.sleep(1) # O Serviço do nomatim suporta apenas 1 requisição por segundo
        return location.raw
    except:
        return get_locations(coordinates, debug)


def populate_database(js):
    """
    Armazena informações no banco de dados a partir de um JSON.

    :param js: JSON contendo as informações a serem armazenadas.
    """
    sql = '''
        INSERT INTO RESULTADOS (
            latitude,
            longitude,
            rua,
            numero,
            bairro,
            cidade,
            cep,
            estado,
            pais,
            endereco
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING ID
    '''

    js_address = js['address']
    param = (
        js['lat'],
        js['lon'],
        js_address.get('road', None),
        js_address.get('house_number', None),
        js_address.get('suburb', None),
        js_address.get('city', None),
        js_address.get('postcode', None),
        js_address.get('state', None),
        js_address.get('country', None),
        js['display_name']
    )
    return get_dict_resultset(sql, param, ONE)


def main_route(filename):
    insertedItems = 0
    if os.path.isfile(filename):
        # Leitura do arquivo de coordenadas
        coordinates = read_coordinates_file(filename)

        # Armazena informações no banco de dados e imprimi IDs armazenados
        for items in coordinates:
            r = populate_database(get_locations(items))
            if r:
                insertedItems = (insertedItems + 1)
                print(r)
            else:
                print(
                    'Não há informações disponíveis para o item:\n' +str(items))
    else:
        print('Arquivo "'+filename+'" não encontrado!')
    return insertedItems
