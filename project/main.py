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
            if (idx+1) % 3 == 0:
                coordinates.append({
                    'lat': content[idx-2].split('   ')[1].rstrip('\n'),
                    'lon': content[idx-1].split('   ')[1].rstrip('\n')
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
    location = geolocator.reverse(points)
    if debug:
        print(location.raw)
    return location.raw



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
        js_address['suburb'],
        js_address['city'],
        js_address['postcode'],
        js_address['state'],
        js_address['country'],
        js['display_name']
    )
    return get_dict_resultset(sql, param, ONE)


def main():
    # Leitura do arquivo de coordenadas
    coordinates = read_coordinates_file('tests/data_points_20180101.txt')

    # Armazena informações no banco de dados e imprimi IDs armazenados
    for items in coordinates:        
        print(populate_database(get_locations(items)))


main()