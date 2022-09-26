# Example posting a text URL:

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example posting a local text file:

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    files={
        'text': open('/path/to/your/file.txt', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example directly sending a text string:

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'YOUR_TEXT_HERE',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())
