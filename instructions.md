**Obs:** Desenvolvimento realizado integralmente utilizando Ubuntu 18.04 x64
     Codificação respeitando limite de 80 caracteres


## Ferramentas utilizadas:

- Codificação
    - Visual Code (https://code.visualstudio.com/docs/?dv=linux64_deb)

- Banco de Dados (PostgreSQL)
    - Criar arquivo etc/apt/sources.list.d/pgdg.list e adicionar a seguinte linha: deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main

    $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
      sudo apt-key add -

    $ sudo apt-get update

    $ sudo apt-get install postgresql-10


## Criação do banco de dados
  $ sudo su postgres

  $ createuser -P -s -e sysdba
  - usar senha "masterkey" (sem aspas)

  $ createdb desafio_4all

  $ psql -d desafio_4all -1 -f <filename>.sql

    filename seria o arquivo tables.sql localizado neste projeto

## Utilização do projeto
  *$ sudo apt-get install python-pip

  *$ sudo apt-get install python3-venv

  $ cd pasta_do_projeto

  *$ mkdir env

  *$ python3 -m venv env

  $ source env/bin/activate

  $ cd project

  $ source exports.sh

  *$ pip install -U pip

  *$ pip install -r requirements.txt

  $ python3 run.py arquivo1.txt arquivo2.txt etc

    - Exemplo: python3 run.py /home/giovannigaspar/Downloads/data_points/data_points_20180101.txt


**Obs:** *Necessário apenas na primeira execução
