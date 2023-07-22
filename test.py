from poorman_http.client import HTTPClient

with HTTPClient(
    host="localhost",
    port=8000,
    headers={"Host": "localhost", "User-Agent": "poorman-http", "Accept": "*/*"},
) as test:
    res = test.get(endpoint="/")
    data = res.json()

    print(data)
