def get_release(self):
    import requests
    from bs4 import BeautifulSoup

    current = requests.get("http://data.wikipathways.org/current/gmt/")
    html = BeautifulSoup(current.text, "html.parser")
    link = html.find("a")
    link_text = link.contents[0]
    version = link_text.split("-")
    version = version[1]
    return version
