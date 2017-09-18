from __future__ import print_function
import os, time, datetime
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()
Base = declarative_base(metadata=metadata)
from sqlalchemy.engine import reflection
from subprocess import call

import db_config

# ToDo
# - filter associations based on their presence in ontologies. e.g. AN123 has GO123, GO234, GO345 but GO345 is not in obo, thus kick it out

table_colName_tuples_for_indices = [("function_2_definition", "an"),
                                     ("functions", "an", "type"),
                                     ("go_2_slim", "an"),
                                     ("og_2_function", "og", "function"),
                                     ("ogs", "og"),
                                     ("ontologies", "child", "parent", "direct", "type"),
                                     ("peptides", "an", "missedcleavages", "aaseq"),
                                     ("protein_2_function", "an", "function"),
                                     ("protein_2_og", "an", "og"),
                                     ("protein_2_taxid", "an", "taxid"),
                                     ("protein_2_version", "an", "version"),
                                     ("protein_secondary_2_primary_an", "sec", "pri"),
                                     ("proteins", "an"),
                                     ("taxa", "taxid", "taxname", "scientific"),
                                     ("taxid_2_rank", "taxid", "rank")]

table_colName_tuples_for_indices_for_agotool = [("protein_2_function", "an", "function"),
                                                ("protein_secondary_2_primary_an", "sec", "pri"),
                                                ("ontologies", "child", "parent", "direct", "type"),
                                                ("protein_2_og", "an", "og"),
                                                ("og_2_function", "og", "function"),
                                                ("go_2_slim", "an"),
                                                ("functions", "an", "type")]

# class Database(object):
#
#     def __init__(self, echo=True, testing=True, do_logging=True):
#         self.echo = echo
#         self.testing = testing
#         self.do_logging = do_logging
#         self.con = db_config.Connect(echo=self.echo, testing=self.testing, do_logging=self.do_logging)
#         self.DATABASE, self.TABLES_DIR, self.FN_LOG = self.con.get_constants()
#         Base.metadata.reflect(self.con.engine)
#         file_name_list = [fn for fn in os.listdir(self.TABLES_DIR) if fn.endswith("_table.txt")]
#         self.table_name_list = [fn.lower().replace("_table.txt", "") for fn in file_name_list]
#         self.file_name_list = [os.path.join(self.TABLES_DIR, fn) for fn in file_name_list]
#         ### table_name, column_name_1, column_name_2, ... --> index = tableName_colName_idx
#         self.tableName_2_fileName_dict = dict(zip(self.table_name_list, self.file_name_list))
#
#     def get_session(self):
#         return self.con.get_session()


def get_table_2_indices_dict(table_colName_tuples_for_indices):
    table_2_indices_dict = {}
    for tableName_cols in table_colName_tuples_for_indices:
        table_name, column_name_list, = tableName_cols[0], tableName_cols[1:]
        for column_name in column_name_list:
            index_name = "{}_{}_idx".format(table_name, column_name)
            if not table_name in table_2_indices_dict:
                table_2_indices_dict[table_name] = [index_name]
            else:
                table_2_indices_dict[table_name].append(index_name)
    return table_2_indices_dict

def get_table_2_indices_dict_of_specific_tables(table_names_list):
    table_2_indices_dict_all = get_table_2_indices_dict(table_colName_tuples_for_indices)
    table_2_indices_dict = {}
    for table in table_names_list:
        table_2_indices_dict[table] = table_2_indices_dict_all[table]
    return table_2_indices_dict

def create_tables(engine):
    """
    :param engine: sqlalchemy engine instance
    :return:
    """
    Base.metadata.create_all(engine)

def drop_table(session, table_name):
    sql_statement = text("DROP TABLE IF EXISTS {}".format(table_name))  # CASCADE drops dependent tables as well # CASCADE
    result = session.execute(sql_statement)
    return result

def drop_index(session, index_name):
    sql_statement = text("DROP INDEX IF EXISTS {}".format(index_name))
    result = session.execute(sql_statement)
    return result

def copy_from_files(session, table_name, file_name):
    sql_statement = text("COPY {} FROM '{}'".format(table_name, file_name))
    result = session.execute(sql_statement)
    return result

def create_index(session, table_name, column_name, index_name):
    sql_statement = text("CREATE INDEX {} ON {}({})".format(index_name, table_name, column_name))
    result = session.execute(sql_statement)
    return result

def analyze_db(session):
    sql_statement = text("ANALYZE VERBOSE")
    result = session.execute(sql_statement)
    return result

def vacuum(connection, full=False):
    # session = Session(bind=db.con.engine)
    session = connection.get_session()
    session.connection(execution_options={'isolation_level': 'AUTOCOMMIT'})
    # work with session
    sql_statement = text("VACUUM")
    if full:
        sql_statement = text("VACUUM FULL")
    result = session.execute(sql_statement)
    # commit transaction.  the connection is released
    # and reverted to its previous isolation level.
    session.commit()
    return result

# entities tables
class Proteins(Base):
    __tablename__ = "proteins"
    # __tablename__ = Base.metadata.tables["proteins"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    # taxid = Column(Integer, nullable=False)
    header = Column(String, nullable=False)
    aaseq = Column(String, nullable=False)

    def __repr__(self):
        return "<Proteins: an: {}, header: {}, aaseq: {})>".format(self.an, self.header, self.aaseq)

class Peptides(Base):
    __tablename__ = "peptides"
    # __tablename__ = Base.metadata.tables["peptides"]

    id = Column(Integer, primary_key=True)
    aaseq = Column(String, nullable=False)
    an = Column(String, nullable=False)
    missedcleavages = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Peptides: aaseq: {}, an: {}, missedcleavages: {}, length: {})>".format(self.aaseq, self.an, self.missedcleavages, self.length)

class Taxa(Base):
    __tablename__ = "taxa"
    # __tablename__ = Base.metadata.tables["taxa"]

    id = Column(Integer, primary_key=True)
    taxid = Column(String, nullable=False)
    taxname = Column(String, nullable=False)
    scientific = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Taxa: taxid: {}, taxname: {}, scientific: {})>".format(self.taxid, self.taxname, self.scientific)

class Taxid_2_rank(Base):
    __tablename__ = "taxid_2_rank"
    # __tablename__ = Base.metadata.tables["taxid_2_rank"]

    id = Column(Integer, primary_key=True)
    taxid = Column(String, nullable=False)
    rank = Column(String, nullable=False)

    def __repr__(self):
        return "<Taxid_2_rank: taxid: {}, rank: {})>".format(self.taxid, self.rank)

class Ogs(Base):
    __tablename__ = "ogs"
    # __tablename__ = Base.metadata.tables["ogs"]

    id = Column(Integer, primary_key=True)
    og = Column(String, nullable=False)
    taxid = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return "<Ogs: og: {}, taxid: {}, description: {})>".format(self.og, self.taxid, self.description)

class Functions(Base):
    __tablename__ = "functions"
    # __tablename__ = Base.metadata.tables["functions"]

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    an = Column(String, nullable=False)

    def __repr__(self):
        return "<Functions: type: {}, name: {}, an: {})>".format(self.type, self.name, self.an)

class Ontologies(Base):
    __tablename__ = "ontologies"
    # __tablename__ = Base.metadata.tables["ontologies"]

    id = Column(Integer, primary_key=True)
    child = Column(String, nullable=False) # not Integer
    parent = Column(String, nullable=False)
    direct = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Ontologies: child: {}, parent: {}, direct: {}, type: {})>".format(self.child, self.parent, self.direct, self.type)

class Protein_2_og(Base):
    __tablename__ = "protein_2_og"
    # __tablename__ = Base.metadata.tables["protein_2_og"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    og = Column(String, nullable=False)

    def __repr__(self):
        return "<Protein_2_og(Protein AN to Orthologous Group: an: {}, og: {})>".format(self.an, self.og)

class Protein_2_version(Base):
    __tablename__ = "protein_2_version"
    # __tablename__ = Base.metadata.tables["protein_2_version"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    version = Column(String, nullable=False)

    def __repr__(self):
        return "<Protein_2_og(Protein AN to version of fasta-DB: an: {}, version: {})>".format(self.an, self.version)

class Og_2_function(Base):
    __tablename__ = "og_2_function"
    # __tablename__ = Base.metadata.tables["og_2_function"]

    id = Column(Integer, primary_key=True)
    og = Column(String, nullable=False)
    function = Column(String, nullable=False)

    def __repr__(self):
        return "<Og_2_function(Orthologous Group to Function: og: {}, function: {})>".format(self.og, self.function)

class Protein_2_function(Base):
    __tablename__ = "protein_2_function"
    # __tablename__ = Base.metadata.tables["protein_2_function"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    function = Column(String, nullable=False)

    def __repr__(self):
        return "<Protein_2_function: an: {}, function: {})>".format(self.an, self.function)

class Function_2_definition(Base):
    __tablename__ = "function_2_definition"
    # __tablename__ = Base.metadata.tables["function_2_definition"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    definition = Column(String, nullable=False)

    def __repr__(self):
        return "<Function_2_definition: an: {}, definition: {})>".format(self.an, self.definition)

class Go_2_slim(Base):
    __tablename__ = "go_2_slim"
    # __tablename__ = Base.metadata.tables["go_2_slim"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    slim = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Go_2_slim: an: {}, slim: {})>".format(self.an, self.slim)

class Protein_2_taxid(Base):
    """
    all of UniProt since info parsed from EBI_IDMAPPINGS
    """
    __tablename__ = "protein_2_taxid"
    # __tablename__ = Base.metadata.tables["protein_2_taxid"]

    id = Column(Integer, primary_key=True)
    an = Column(String, nullable=False)
    taxid = Column(String, nullable=False)

    def __repr__(self):
        return "<Protein_2_taxid: an: {}, taxid: {})>".format(self.an, self.taxid)

class Protein_secondary_2_primary_an(Base):
    """
    download from
    ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/
    sec_ac.txt
    Description: Secondary accession numbers: index
    """
    __tablename__ = "protein_secondary_2_primary_an"

    id = Column(Integer, primary_key=True)
    sec = Column(String, nullable=False)
    pri = Column(String, nullable=False)

    def __repr__(self):
        return "<Protein_Secondary_2_Primary_AN: secondary: {}, primary: {})>".format(self.sec, self.pri)

def get_indices_already_created_list(engine):
    insp = reflection.Inspector.from_engine(engine)
    indices_already_created_list = []
    for name in insp.get_table_names():
        for index in insp.get_indexes(name):
            indices_already_created_list.append(index['name'])
    return indices_already_created_list

# def drop_and_fill_table_and_indices(db, table_2_indices_dict, drop_indices_=True, drop_tables_=True, fill_tables_copy_from_files=True, create_indices=True):
def drop_and_fill_table_and_indices(connection, table_2_indices_dict, drop_indices_=True, drop_tables_=True, fill_tables_copy_from_files=True, create_indices=True):
    start_time = time.time()
    session = connection.get_session()
    ## drop tables and their indices
    for table_name in table_2_indices_dict:
        indices_list = table_2_indices_dict[table_name]
        if drop_indices_:
            for index_name in indices_list:
                drop_index(session, index_name)
        if drop_tables_:
            result = drop_table(session, table_name)
        session.commit()

    ### create tables
    # engine = db.con.engine
    engine = connection.engine
    create_tables(engine)

    #### fill tables, copy from file
    if fill_tables_copy_from_files:
        print("#" * 80, "\nFilling tables with copy from file\n")
        for index_, table_name in enumerate(table_2_indices_dict):
            index_ += 1
            print("Table name {}, Number {} out of {}".format(table_name, index_, len(table_2_indices_dict)))
            # file_name = db.tableName_2_fileName_dict[table_name]
            file_name = connection.tableName_2_fileName_dict[table_name]
            result = copy_from_files(session, table_name, file_name)
            session.commit()

    #### create indices
    if create_indices:
        print("#" * 80, "\nCreating indices\n")
        for index_table, table_name in enumerate(table_2_indices_dict):
            index_table += 1
            print("Table name {}, Number {} out of {}".format(table_name, index_table, len(table_2_indices_dict)))
            indices_list = table_2_indices_dict[table_name]
            for index_idx, index_name in enumerate(indices_list):
                index_idx += 1
                print("Index name {}, Number {} out of {}".format(table_name, index_idx, len(indices_list)))
                column_name = index_name.split("_")[-2]
                result = create_index(session, table_name, column_name, index_name)
                session.commit()
    analyze_db(session)
    session.commit()
    print_runtime(start_time)

def update_specific_tables(db, tables_2_update_list, drop_indices_=True, drop_tables_=True, fill_tables_copy_from_files=True, create_indices=True):
    table_2_indices_dict = get_table_2_indices_dict_of_specific_tables(tables_2_update_list)
    drop_and_fill_table_and_indices(db, table_2_indices_dict, drop_indices_, drop_tables_, fill_tables_copy_from_files, create_indices)

def teardowm_database(engine):
    Base.metadata.drop_all(engine)
    # vacuum(full=True)

# def create_all(db, for_agotool=False):
def create_all(connection, for_agotool=False):
    start_time = time.time()
    # ### connect to db
    # engine = db_connect(echo=True)
    # session = Session(bind=engine)

    # engine = db.con.engine
    # teardowm_database(engine)
    teardowm_database(connection.engine)
    # session = db.get_session()
    session = connection.get_session()
    session.commit()

    if for_agotool:
        table_2_indices_dict = get_table_2_indices_dict(table_colName_tuples_for_indices_for_agotool)
    else:
        table_2_indices_dict = get_table_2_indices_dict(table_colName_tuples_for_indices)
    # drop_and_fill_table_and_indices(db, table_2_indices_dict)
    drop_and_fill_table_and_indices(connection, table_2_indices_dict)

    print_runtime(start_time)

def print_runtime(start_time):
    print("#" * 80, "\n", "--- runtime: {} ---".format(str(datetime.timedelta(seconds=int(time.time() - start_time)))))

# grip DataBase_Schema.md --export --wide --title="Data Base Schema"

def dump_database(tables_2_dump_list, output_dir, fn_out):
    """
    execute as bash command and NOT as sql statement
    e.g. working example
    pg_dump -U dblyon metaprot -t 'protein_2_function' -t 'protein_secondary_2_primary_an' -t 'ontologies' -t 'protein_2_og' -t 'og_2_function' -t 'go_2_slim' > metaprot_agotool.pgsql
    """
    tables_2_dump = ""
    for table_name in tables_2_dump_list:
        tables_2_dump += "-t '{}' ".format(table_name)
    tables_2_dump = tables_2_dump.strip()
    shellcmd = "cd {}\n".format(output_dir)
    shellcmd += "pg_dump -U dblyon metaprot {} > {}".format(tables_2_dump, fn_out)
    print(shellcmd)
    call(shellcmd, shell=True)


if __name__ == "__main__":
    connection = db_config.Connect(echo=True, testing=True, do_logging=False, volume_mountpoint="/tables")
    create_all(connection, for_agotool=True)

    ### update these tables and their indices:
    # session = db.get_session()
    # tables_2_update_list = ["protein_2_function"] #["taxid_2_rank", "taxa", "ontologies"]
    # drop_tables_ = True
    # fill_tables_copy_from_files = True
    # drop_indices_ = True
    # create_indices = True
    # update_specific_tables(db, tables_2_update_list, drop_indices_, drop_tables_, fill_tables_copy_from_files, create_indices)
    #tables_2_dump_list = ["protein_2_function",
    #                      "protein_secondary_2_primary_an",
    #                      "ontologies",
    #                      "protein_2_og",
    #                      "og_2_function",
    #                      "go_2_slim",
    #                      "functions"]
    #output_dir = r"/Users/dblyon/Downloads"
    #fn_out = "metaprot_agotool.pgsql"
    #dump_database(tables_2_dump_list, output_dir, fn_out)

