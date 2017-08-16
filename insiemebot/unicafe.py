import re
import requests

from bs4 import BeautifulSoup


MENU_URL = 'https://www.uni-cafe.at/'
TOP = "\S+ \d+/\d+/\d+"
BOT = "Das Uni Cafe als"


def today():
    r = requests.get(MENU_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    match = re.search("{}\s*(.*?)\s*{}".format(TOP, BOT), soup.get_text(), re.DOTALL)
    res = [s.strip().replace("\n"," ") for s in match.group(1).split("* * *")]
    res = [s for s in res if s]
    return "\n".join(res)
