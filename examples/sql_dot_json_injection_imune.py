from sql_dot_json import JSONDatabase

# Vulnerable to injection using string substitution into a SQL statement

"""
This script is a basic command line utility to lookup an email address from a username.

Normal usage involves running the script and entering a username when prompted.

This version of the utility correctly uses value substitution in order to avoid
the injection vulnerability in `sql_dot_json_injection_vuln.py`. If you'd like
to learn more about the topic see that file and the somments within it.
"""

# Not vulnerable to injection. Uses ? for variables and passes arguments to execute.
json_db = JSONDatabase("example_db_sql.json")
username_in = input("what is your username? ")
result = json_db.execute_full_query(f"SELECT email FROM UserTable WHERE username=?", (username_in,))
if result:
    if isinstance(result, list) and len(result) == 1:
        print(f"Your email is: {result[0][0]}")
    else:
        print(f"DB Response: {result}")
else:
    print(f"User '{username_in}' not found")
