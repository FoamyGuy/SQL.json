# SQL Dot JSON (Stylized as SQL.json)

## **SQL.json is not suitable for use in real projects.**

This project is a _VERY BASIC_ SQL engine that stores data in a .json file.
It was engineered to allow insecure usage in some specific ways,
and likely is insecure in other un-intended ways. It has very limited capabilities
compared to other "real" SQL engines like SQLite3.

### Drawbacks, Missing Features and Limitations

- The engine supports only a minimal subset of SQL commands: 
  SELECT, INSERT, DELETE, DROP TABLE
- Does not support escaped special characters
- Syntax is more strict than traditional SQL. 
  (i.e. No spaces allowed in comma seperated lists)
- Only tested with int and string values, other types may not work. 
- Spaces within strings may cause errors or get stripped
- Very inefficient compared to real SQL engines.

### How to use it?
- Create a .json file for the data. SQL.json does not support CREATE TABLE so you must create this file
  and populate it with a text editor of your choice.
  - Example data:
  
```json
{
"UserTable": {
  "cols": [
    "id",
    "username",
    "email"
  ],
  "table": [
    {
      "id": 0,
      "username": "johns",
      "email": "johns@fakemail.com"
    },
    {
      "id": 1,
      "username": "janes",
      "email": "janes@fakemail.com"
    },
    ...
  ]
  ```
- Initialize the database connector:
```
json_db = JSONDatabase("tmp_sql.json")
```
- execute a query:
```
result = json_db.execute_full_query("SELECT * FROM UserTable;")
print(result)
```

### Why did I create this?

It's intended to be used as a basic initial introduction to SQL and SQL Injection
vulnerabilities. It's ultimately intended to run on CircuitPython microcontrollers 
and be used along with Adafruit_HTTPServer library.


### Who is the project intended for?

People with little or no prior knowledge of SQL or databases, but want to learn.
People who do likely have some prior Python or CircuitPython experience.
People who may have prior experience with JSON.
