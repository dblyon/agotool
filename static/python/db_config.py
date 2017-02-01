import os, time
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Connect(object):
    DATABASE = {"drivername": "postgres",
                "host": "localhost",
                "port": "5432",
                "username": "guest",
                "password": ""}

    def __init__(self, echo, testing, do_logging, volume_mountpoint=None):
        """
        :param echo:
        :param testing:
        :param do_logging: Bool or String (False: no logging; True: debug; Sting: 'debug' or 'warning')
        """
        self.echo = echo
        self.testing = testing
        self.do_logging = do_logging
        self.volume_mountpoint = volume_mountpoint
        self.DATABASE = self.get_DATABASE_config()
        self.engine = self.db_connect(self.DATABASE, self.echo)
        self.Session = sessionmaker(bind=self.engine)
        self.TABLES_DIR = self.get_TABLES_DIR(self.testing)
        self.FN_LOG = self.get_FN_LOG(self.testing)
        if self.do_logging:
            self.log_stuff(self.FN_LOG, self.do_logging)

        self.DATABASE, self.TABLES_DIR, self.FN_LOG = self.get_constants()
        Base.metadata.reflect(self.engine)
        file_name_list = [fn for fn in os.listdir(self.TABLES_DIR) if fn.endswith("_table.txt")]
        self.table_name_list = [fn.lower().replace("_table.txt", "") for fn in file_name_list]
        self.file_name_list = [os.path.join(self.TABLES_DIR, fn) for fn in file_name_list]
        ### table_name, column_name_1, column_name_2, ... --> index = tableName_colName_idx
        self.tableName_2_fileName_dict = dict(zip(self.table_name_list, self.file_name_list))

    @staticmethod
    def db_connect(DATABASE, echo):
        """
        Performs database connection using database settings
        Returns sqlalchemy engine instance
        psycopg2:
        engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
        """
        return create_engine(URL(**DATABASE), echo=echo)

    def get_URL(self):
        return r"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}".format(**self.DATABASE)

    def get_session(self):
        session = self.Session()
        return session

    def get_DATABASE_config(self):
        if self.testing:
            self.DATABASE["database"] = "test"
        else:
            self.DATABASE["database"] = "metaprot"
        return self.DATABASE

    def get_TABLES_DIR(self, testing):
        if testing:
            if self.volume_mountpoint is None:
                TABLES_DIR = r"/Users/dblyon/modules/cpr/metaprot/sql/tables/test"
            else:
                TABLES_DIR = os.path.join(self.volume_mountpoint, "test")
        else:
            if self.volume_mountpoint is None:
                TABLES_DIR = r"/Users/dblyon/modules/cpr/metaprot/sql/tables"
            else:
                TABLES_DIR = self.volume_mountpoint
        return TABLES_DIR

    @staticmethod
    def get_FN_LOG(testing):
        if testing:
            FN_LOG = "log_psql_testing.txt"
        else:
            FN_LOG = "log_psqldb_metaprot.txt"
        if not os.path.exists(FN_LOG):
            fh = open(FN_LOG, "w")
            fh.close()
        return FN_LOG

    @staticmethod
    def log_stuff(FN_LOG, log_level):
        import logging
        if log_level == "warning":
            logging.basicConfig(filename=FN_LOG, level=logging.WARNING)
        elif log_level == "debug":
            logging.basicConfig(filename=FN_LOG, level=logging.DEBUG)
        else:
            logging.basicConfig(filename=FN_LOG, level=logging.DEBUG)
        string2log_prefix = "#" * 80 + "\n" + "Current date & time " + time.strftime("%c") + "\n"
        logging.info(string2log_prefix)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

    def get_constants(self):
        return self.DATABASE, self.TABLES_DIR, self.FN_LOG

