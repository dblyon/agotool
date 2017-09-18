import db_config, tools



if __name__ == "__main__":
    ECHO = False
    TESTING = False # which DB are we connecting to ('metaprot' or 'test')
    DO_LOGGING = False
    volume_mountpoint=None # mount point set at 'docker run -v LocalPath:MountPoint'
    connection = db_config.Connect(echo=ECHO, testing=TESTING, do_logging=DO_LOGGING, volume_mountpoint=volume_mountpoint, run_agotool_as_container=True)
    print(connection.get_URL())
    print(connection.DATABASE)

    function_type = "GO"
    limit_2_parent = u"Biological Process"
    go_slim_or_basic = "basic"
    backtracking = True
    protein_ans_list = ['Q9XC60', 'P40417']
    assoc_dict = tools.get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=limit_2_parent, basic_or_slim=go_slim_or_basic, backtracking=backtracking)
    print(assoc_dict)

