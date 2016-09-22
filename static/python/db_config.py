import os, time
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


class Connect(object):
    DATABASE = {"drivername": "postgres",
                "host": "localhost",
                "port": "5432",
                "username": "dblyon",
                "password": ""}

    def __init__(self, echo, testing, do_logging):
        self.echo = echo
        self.testing = testing
        self.do_logging = do_logging
        self.DATABASE = self.get_DATABASE_config(self.testing)
        self.engine = self.db_connect(self.DATABASE, self.echo)
        self.Session = sessionmaker(bind=self.engine)
        self.TABLES_DIR = self.get_TABLES_DIR(self.testing)
        self.FN_LOG = self.get_FN_LOG(self.testing)
        if self.do_logging is not None:
            self.log_stuff(self.FN_LOG, self.do_logging)

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

    def get_DATABASE_config(self, testing):
        if testing:
            self.DATABASE["database"] = "test"
        else:
            self.DATABASE["database"] = "metaprot"
        return self.DATABASE

    @staticmethod
    def get_TABLES_DIR(testing):
        if testing:
            TABLES_DIR = r"/Users/dblyon/modules/cpr/metaprot/sql/tables/test"
        else:
            TABLES_DIR = r"/Users/dblyon/modules/cpr/metaprot/sql/tables"
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
        else:
            logging.basicConfig(filename=FN_LOG, level=logging.DEBUG)
        string2log_prefix = "#" * 80 + "\n" + "Current date & time " + time.strftime("%c") + "\n"
        logging.info(string2log_prefix)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

    def get_constants(self):
        return self.DATABASE, self.TABLES_DIR, self.FN_LOG

