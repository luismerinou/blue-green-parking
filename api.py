import json

import requests

r = requests.get('https://datos.madrid.es/egob/catalogo/title/SER-calles.json')

print(r.json().get('result').get('items'))
