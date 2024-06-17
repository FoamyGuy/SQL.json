from sql_dot_json import JSONDatabase

if __name__ == "__main__":
    json_db = JSONDatabase("example_db_sql.json")

    print("\n------------------------\n")

    print("Command: SELECT email FROM UserTable WHERE username=lily;")
    result = json_db.execute_full_query("SELECT email FROM UserTable WHERE username=lily;")
    print(f"Result: {result}")

    print("\n------------------------\n")

    print("Command: INSERT INTO UserTable VALUES (4,wilma,wilma@fakeemail.com);")
    result = json_db.execute_full_query("INSERT INTO UserTable VALUES (4,wilma,wilma@fakeemail.com);")
    print(f"Result: {result}")

    print("\n------------------------\n")

    print("Command: SELECT * FROM UserTable WHERE id=4;")
    result = json_db.execute_full_query("SELECT * FROM UserTable WHERE id=4;")
    print(f"Result: {result}")

    print("\n------------------------\n")

    print("Command: SELECT * FROM UserTable;")
    result = json_db.execute_full_query("SELECT * FROM UserTable;")
    print(f"Result: {result}")

    print("\n------------------------\n")

    print("Command: DELETE FROM UserTable WHERE id=4;")
    result = json_db.execute_full_query("DELETE FROM UserTable WHERE id=4;")
    print(f"Result: {result}")

    print("\n------------------------\n")

    print('Command: SELECT * FROM UserTable WHERE username=?;", ("jill",)')
    result = json_db.execute_full_query("SELECT * FROM UserTable WHERE username=?;", ("jill",))
    print(f"Result: {result}")

    print("\n------------------------\n")
