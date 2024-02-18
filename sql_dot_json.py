import json
import re


class SQLException(Exception):
    pass


class JSONDatabase:
    def __init__(self, json_file):
        self.file = json_file
        self.data = self.load_data(json_file)

    def load_data(self, json_file):
        with open(json_file, 'r') as f:
            return json.load(f)

    def save_data(self, json_file):
        with open(json_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def max_id(self, table):
        largest = 0
        for row in self.data[table]["table"]:
            if largest < row["id"]:
                largest = row["id"]
        return largest

    def sanitize(self, value):
        return value.replace(";", "").replace(" ", "").replace("=", "")

    def replace_vars(self, query_string, sql_args):
        updated_query_str = query_string
        for arg in sql_args:
            updated_query_str = updated_query_str.replace("?", self.sanitize(arg), 1)
        return updated_query_str

    def to_csv(self, table):
        csv_str = ",".join(self.data[table]["cols"])
        csv_str += "\n"

        for row in self.data[table]["table"]:

            vals = []
            for col in self.data[table]["cols"]:
                vals.append(str(row[col]))
            row_str = ",".join(vals)
            row_str += "\n"
            csv_str += row_str
        return csv_str
    def execute_full_query(self, query_string, sql_args=None):
        if sql_args is not None:
            query_string = self.replace_vars(query_string, sql_args)
        querys = query_string.split(";")
        result = None
        for _query in querys:
            if _query:
                result = self.execute_single_query(_query)
        return result

    def execute_single_query(self, query):
        command, *rest = query.split()
        print(f"command: {command} rest:{rest}")

        if command == 'SELECT':
            fields = rest[0]
            if rest[1] != "FROM":
                raise SQLException("Did not find FROM in expected location.")
            table = rest[2]
            condition = None
            if len(rest) > 3:
                if rest[3] != "WHERE":
                    raise SQLException("Did not find WHERE in expected location.")
                if len(rest) < 5:
                    raise SQLException("WHERE found without condition.")
                condition = rest[4]
            return self.select(fields, table, condition)
        elif command == 'INSERT':
            if rest[0].upper() != "INTO":
                raise SQLException("INSERT missing INTO.")
            table = rest[1]
            if rest[2].upper() != "VALUES":
                raise SQLException("INSERT INTO missing VALUES")
            print(f"rest: {rest}")
            val_str = "".join(rest[3:])
            # val_items = re.search("^\(.*\)$", val_str)
            values = val_str[1:][:-1].split(",")
            for idx, _ in enumerate(values):
                try:
                    values[idx] = int(_)
                except ValueError:
                    pass

            # print(values)
            return self.insert(table, values)
        elif command == "DELETE":
            # print("DELETE Command")
            if rest[0] != "FROM":
                raise SQLException("Expected FROM after DELETE.")
            if len(rest) < 4 or rest[2] != "WHERE":
                raise SQLException("Expected WHERE and Condition after Table.")
            table = rest[1]
            conditions = [rest[3]]
            return self.delete(table, conditions)
        elif command == "DROP":
            if rest[0] != "TABLE":
                raise SQLException("Expected TABLE after DROP.")
            if len(rest) < 2:
                raise SQLException("Expected Table name after DROP TABLE.")
            table = rest[1]
            return self.drop_table(table)
        else:
            return "Unsupported command."

    def drop_table(self, table):
        if table not in self.data:
            return "Table Not Found"

        del self.data[table]
        self.save_data(self.file)
        return f"Table {table} Deleted"

    def select(self, fields, table, condition):
        if table in self.data:
            out_data = []
            for row in self.data[table]["table"]:
                if condition:
                    if not self._matches_conditions(row, [condition]):
                        # print("has condition and was not matched")
                        continue

                _row_data = []
                if fields == "*":
                    for field in row.keys():
                        _row_data.append(row.get(field))
                else:
                    for field in fields.split(","):
                        _row_data.append(row.get(field))
                out_data.append(_row_data)
            return out_data
        else:
            return f"Table '{table}' not found."

    def delete(self, table, conditions):
        del_count = 0

        for row_idx in range(len(self.data[table]["table"]) - 1, -1, -1):
            if self._matches_conditions(self.data[table]["table"][row_idx], conditions):
                del_count += 1
                self.data[table]["table"].pop(row_idx)

        # self.data[table] = [row for row in self.data.get(table, []) if not self._matches_conditions(row, conditions)]
        self.save_data(self.file)
        return f"DELETED {del_count} rows."

    def insert(self, table, values):
        new_row_obj = {}
        for idx, col in enumerate(self.data[table]["cols"]):
            if values[idx] == "AUTOID":
                new_row_obj[col] = self.max_id(table) + 1
            else:
                new_row_obj[col] = values[idx]
        for row in self.data[table]["table"]:
            if row["id"] == new_row_obj["id"]:
                raise SQLException("Integrity Error: Duplicate ID")
        self.data[table]["table"].append(new_row_obj)
        self.save_data(self.file)
        return f"ROW INSERTED INTO {table}"

    def _matches_conditions(self, row, conditions):
        # print(f"checking match: {row} - {conditions}")
        for condition in conditions:
            key, value = condition.split('=')
            # print(f"row val: {row.get(key)} condition_val: {value}")
            try:
                value = int(value)
            except ValueError:
                pass
            if row.get(key) != value:
                return False
        return True


if __name__ == "__main__":
    json_db = JSONDatabase("tmp_sql.json")

    # while True:
    #     query = input("Enter an SQL query (Exit w/ Ctrl-C): ")
    #     result = json_db.execute_query(query)
    #     print(result)

    # json_db.save_data("your_json_data.json")

    result = json_db.execute_full_query("SELECT email FROM UserTable WHERE username=johns;")
    print(result)

    result = json_db.execute_full_query("DELETE FROM UserTable WHERE id=4;")
    print(result)

    result = json_db.execute_full_query("SELECT * FROM UserTable;")
    print(result)

    result = json_db.execute_full_query("SELECT email FROM UserTable WHERE username=?;", ("johns",))
    print(result)
    
    print(json_db.to_csv("UserTable"))

    # result = json_db.execute_full_query("DROP TABLE UserTable;")
    # print(result)

    # print(json_db.data)

    # Vulnerable to injection using string substitution into a SQL statement
    # username_in = input("what is your username? ")
    # result = json_db.execute_full_query(f"SELECT email FROM UserTable WHERE username={username_in}")
    # if result:
    #     if isinstance(result, list):
    #         print(f"Your email is: {result[0][0]}")
    #     elif isinstance(result, str):
    #         print(f"DB Response: {result}")
    # else:
    #     print("User not found")

    # Not vulnerable to injection. Uses ? for variables and passes arguments to execute.
    # username_in = input("what is your username? ")
    # result = json_db.execute_full_query(f"SELECT email FROM UserTable WHERE username=?", (username_in,))
    # print(result)
    # if result:
    #     if isinstance(result, list):
    #         print(f"Your email is: {result[0][0]}")
    #     elif isinstance(result, str):
    #         print(f"DB Response: {result}")
    # else:
    #     print("User not found")
