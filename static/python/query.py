from collections import defaultdict
import psycopg2, math

UNSIGNED_2_SIGNED_CONSTANT = int(math.pow(2, 63))


def get_cursor(host='localhost', dbname='agotool', user='dblyon', password=''):
    """

    :param host:
    :param dbname:
    :param user:
    :param password:
    :return: DB Cursor instance object
    """
    # Define our connection string
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor

def query_example(cursor):
    cursor.execute("SELECT * FROM child_2_parent_table LIMIT 5")
    records = cursor.fetchall()
    print(records)

def map_secondary_2_primary_ANs(ans_list):
    """
    map secondary UniProt ANs to primary ANs,
    AN only in dict if mapping exists
    :param ans_list: ListOfString
    :return: Dict (key: String(Secondary AN), val: String(Primary AN))
    """
    cursor = get_cursor()
    ans_list = str(ans_list)[1:-1]
    sql_statement = "SELECT protein_secondary_2_primary_an.sec, protein_secondary_2_primary_an.pri FROM protein_secondary_2_primary_an WHERE protein_secondary_2_primary_an.sec IN({})".format(ans_list)
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    secondary_2_primary_dict = {}
    for res in result:
        secondary = res[0]
        primary = res[1]
        secondary_2_primary_dict[secondary] = primary
    return secondary_2_primary_dict



if __name__ == "__main__":
    pass
