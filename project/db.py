import os
import psycopg2
import psycopg2.extras


# Variáveis globais utilizadas para execução genérica do SQL.
ONE = 1
ALL = 2


# Conexão com o banco de dados utilizando variáveis de ambiente.
conn = psycopg2.connect(
    host='localhost',
    dbname=os.getenv('DATABASE_NAME'),
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD')
)


def get_dict_resultset(sql, param, results):
    """
    Realiza operações no banco de dados e retorna os resultados (caso houver)
    em forma de um dicionário.
    Se a operação for bem sucedida, realiza um COMMIT no banco de dados. Caso
    contrário, realiza um ROLLBACK.

    :param sql: SQL a ser executado no banco.
    :param param: parâmetros de execução do comando SQL.
    :param results: Quantidade de resultados esperada
    (ONE -> um resultado, ALL -> Vários resultados. None -> Nenhum retorno)

    :return: Dicionário formatado com os valores do retorno da execução ou None
    em caso de falha.
    """

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    ans = None
    dict_result = []

    try:
        cur.execute(sql, param)
    except Exception:
        cur.execute('ROLLBACK')
        return None

    if results == ONE:
        ans = cur.fetchone()
        if ans:
            dict_result.append(dict(ans))
            cur.execute('COMMIT')
            return dict_result[0]
    elif results == ALL:
        ans = cur.fetchall()
        if ans:
            for row in ans:
                dict_result.append(dict(row))
            cur.execute('COMMIT')
            return dict_result
    return None