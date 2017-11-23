TEST_DIR = "test"
TABLES_DIR = "tables"

def foo_fail(testing):
    print("Test dir 2:", TEST_DIR)
    print("Tables dir 2:", TABLES_DIR)
    if testing:
        TABLES_DIR = TEST_DIR

def foo_works(testing):
    global TABLES_DIR
    print("Test dir 2:", TEST_DIR)
    print("Tables dir 2:", TABLES_DIR)
    if testing:
        TABLES_DIR = TEST_DIR

if __name__ == "__main__":
    print("Test dir 1: ", TEST_DIR)
    print("Tables dir 1:", TABLES_DIR)

    foo_fail(testing=False)
    # foo_works(testing=False)
