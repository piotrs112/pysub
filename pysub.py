import requests
from bs4 import BeautifulSoup
#from user_agent import generate_user_agent

#headers = generate_user_agent(os=('win', 'mac', 'linux'))
r = requests.get("https://addic7ed.com") #, headers=headers)
if r.status_code != 200:
    raise ConnectionError

soup = BeautifulSoup(r.text, "lxml")
body = soup.body
showlist = body.find('select', {'id':'qsShow'})
shows = showlist('option')

for show in shows [:10]:
    print("NAME: {} ID: {}".format(show.get_text(), show.get('value')))
