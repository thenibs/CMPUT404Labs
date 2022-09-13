import requests

print(requests.__version__)

print(requests.get("http://www.google.com/"))

print("\n" + requests.get("https://raw.githubusercontent.com/thenibs/CMPUT404Labs/main/getVersion.py").text)