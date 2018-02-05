import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import psycopg2

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)) 

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)

def get_cursor_old(host='localhost', dbname='agotool', user='dblyon', password='', port=5432):
    # Define our connection string
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)

    # engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
    conn_string = "host='{}' dbname='{}' user='{}' password='{}' port='{}'".format(host, dbname, user, password, port)
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor

if __name__ == "__main__":
    import os
    # user = os.environ['POSTGRES_USER']
    # pwd = os.environ['POSTGRES_PASSWORD']
    # db = os.environ['POSTGRES_DB']
    # host = 'db'
    # port = '5432'
    # print("user", user)
    # print("pwd", pwd)
    # print("db", db)

    user = os.environ['POSTGRES_USER']
    pwd = os.environ['POSTGRES_PASSWORD']
    db = os.environ['POSTGRES_DB']
    host = 'db'
    port = '5432'
    # engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
    cursor = get_cursor_old(user=user, password=pwd, host=host, port=port, dbname=db)
    # cursor = get_cursor()
    # cursor = get_cursor_old(host=host, dbname=db, user=user, password="postgres")
    cursor.execute("SELECT * FROM functions WHERE functions.type='KEGG' LIMIT 5")
    records = cursor.fetchall()
    print(records)