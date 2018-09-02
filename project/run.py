import sys, os
from app import main


#python run.py 'arquivo1' 'arquivo2' 'etc'
if len(sys.argv) < 2:
    print('Nenhum arquivo informado!')
else:
    files = sys.argv[1:]
    for file in files:
        filename = file
        if not os.path.isfile(filename):
            print('Arquivo não encontrado!')
        else:
            main(filename)
