import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

def get_image_links(query_):

    # query_ = query_.replace(' ', '+')

    url = f'https://www.google.com/search?hl=en&tbm=isch&q={query_}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        if response.status_code == 400:
            print("Bad Request: The server could not understand the request due to invalid syntax.")
        elif response.status_code == 401:
            print("Unauthorized: The client must authenticate itself to get the requested response.")
        elif response.status_code == 403:
            print("Forbidden: The client does not have access rights to the content.")
        elif response.status_code == 404:
            print("Not Found: The server can not find the requested resource.")
        elif response.status_code == 500:
            print("Internal Server Error: The server has encountered a situation it doesn't know how to handle.")
        elif response.status_code == 502:
            print(
                "Bad Gateway: The server, while acting as a gateway or proxy, received an invalid response "
                "from the upstream server.")
        elif response.status_code == 503:
            print("Service Unavailable: The server is not ready to handle the request.")
        elif response.status_code == 504:
            print(
                "Gateway Timeout: The server, while acting as a gateway or proxy, did not get a response "
                "in time from the upstream server.")
        else:
            print(f"Failed to retrieve web page. HTTP Status Code: {response.status_code}")

            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    image_tags = soup.find_all('img')

    image_links = []
    for img in image_tags:
        if 'data-src' in img.attrs:
            image_links.append(img['data-src'])
        elif 'src' in img.attrs and img['src'].startswith('http'):
            image_links.append(img['src'])

    return image_links[1:5]


# api
@app.route('/get_image_links', methods=["GET"])
def get_image_links_endpoint():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No query parameter provided'}), 400

    links = get_image_links(query)
    return jsonify({'links': links})


if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000/get_image_links?query=Garden+Glory+Hose

# before api
# if __name__ == "__main__":
#     query = "Beko BL77 Integrated"
#     links = get_image_links(query)
#     for link in links:
#         print(link)
