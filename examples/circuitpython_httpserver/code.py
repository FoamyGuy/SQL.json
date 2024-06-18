# SPDX-FileCopyrightText: 2024 DJDevon3
#
# SPDX-License-Identifier: MIT

import wifi

from adafruit_connection_manager import get_radio_socketpool
from adafruit_httpserver import Server, Request, Response, REQUEST_HANDLED_RESPONSE_SENT, POST
from sql_dot_json import JSONDatabase

pool = get_radio_socketpool(wifi.radio)
server = Server(pool, "/static", debug=True)
json_db = JSONDatabase("example_db_sql.json")


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    index_content = None
    with open("static/index.html", "r") as f:
        index_content = f.read()

    index_content = index_content.replace("{{ results_display }}", "none")
    index_content = index_content.replace("{{ results }}", "")

    return Response(request, index_content, content_type="text/html")


@server.route("/lookup_username", methods=[POST])
def search_username(request: Request):
    username_in = request.form_data.get("username")
    # Handle URLEncoding
    username_in = username_in.replace("+", " ")
    username_in = username_in.replace("%3B", ";")
    
    print(username_in)

    index_content = None
    with open("static/index.html", "r") as f:
        index_content = f.read()

    result = json_db.execute_full_query(f"SELECT email FROM UserTable WHERE username={username_in}")
    if result:
        if isinstance(result, list) and len(result) == 1:
            result_str = f"Email is: {result[0][0]}"
        else:
            result_str = f"DB Response: {result}"
    else:
        result_str = f"User '{username_in}' not found"

    index_content = index_content.replace("{{ results_display }}", "block")
    index_content = index_content.replace("{{ results }}", result_str)

    return Response(request, index_content, content_type="text/html")


# server.serve_forever(str(wifi.radio.ipv4_address))

# Start the server.
server.start(str(wifi.radio.ipv4_address))
while True:
    try:
        # Do something useful in this section,
        # for example read a sensor and capture an average,
        # or a running total of the last 10 samples

        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        # If you want you can stop the server by calling server.stop() anywhere in your code
    except OSError as error:
        print(error)
        continue
