import requests
from bs4 import BeautifulSoup
#from user_agent import generate_user_agent

q_name = "Chilling Adventures of Sabrina"


def connect(addr: str) -> requests.models.Response:
    #headers = generate_user_agent(os=('win', 'mac', 'linux'))
    r = requests.get(addr) #, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
    return r

r = connect("https://addic7ed.com")

soup = BeautifulSoup(r.text, "lxml")
body = soup.body
showlist = body.find('select', {'id':'qsShow'})
show = showlist.find(string=q_name).parent

if show != None and show != []:
    print("NAME: {} ID: {}".format(show.get_text(), show.get('value')))
