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
    [{'lat':'y', 'long':'x'}]
    """    
    coordinates = []
    with open(filename, 'r', newline='') as f:
        content = f.readlines()
        for idx, line in enumerate(content):
            if (idx+1) % 3 == 0:
                coordinates.append({
                    'lat': content[idx-2].split('   ')[1].rstrip('\n'),
                    'long': content[idx-1].split('   ')[1].rstrip('\n')
                })
    if debug:
        print(coordinates)
    return coordinates


def get_locations(coordinates, debug=False):
    """
    Obtém informações de um local (endereço, CEP, bairro, etc) a partir de 
    coordenadas (latitude e longitude) geográficas.


    :param coordinates: coordenadas a serem verificadas. Espera-se que estejam
    no padrão [{'lat':'y', 'long':'x'}]

    :param debug: utilizado para imprimir as informações do local como forma de 
    debug

    :return: JSON contendo as informações do local pesquisado
    """
    points = coordinates['lat'] + ', ' + coordinates['long']
    location = geolocator.reverse(points)
    if debug:
        print(location.raw)
    return location.raw



def populate_database(info):
    """
    Armazena informações no banco de dados a partir de um JSON.

    :param info: JSON contendo as informações a serem armazenadas.
    """
    print(info)


def main():
    # Leitura do arquivo de coordenadas
    coordinates = read_coordinates_file('tests/data_points_20180101.txt', True)

    populate_database(get_locations(coordinates[0]))


main()