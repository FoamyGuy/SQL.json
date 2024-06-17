from sql_dot_json import JSONDatabase

# Vulnerable to injection using string substitution into a SQL statement

"""
This script is a basic command line utility to lookup an email address from a username.

Normal usage involves running the script and entering a username when prompted.

However the script is vulnerable to SQL Injection because it does not use
value substitution, and it's input from the user is not sufficiently sanitized.

To under stand this basic injection vulnerability consider the input:

jane;SELECT * FROM UserTable;

With this input the user is including semi-colon's in their input which serve
as delimiters for the SQL statements. Using this technique the malicious user
is able to execute their own SQL statement that the developer never intended.

In the example above that statement would dump the entire database back to
the user exposing private information of other users within the system.
However the attacker has the capability to do whatever they want including
adding their own user accounts, manipulating permissions, deleting data etc..

In order to avoid this vulnerability the code should use value substituion
with the SQL statement instead of python string formatting.
"""

json_db = JSONDatabase("example_db_sql.json")
username_in = input("What is your username? ")
result = json_db.execute_full_query(f"SELECT email FROM UserTable WHERE username={username_in}")
if result:
    if isinstance(result, list) and len(result) == 1:
        print(f"Your email is: {result[0][0]}")
    else:
        print(f"DB Response: {result}")
else:
    print(f"User '{username_in}' not found")
