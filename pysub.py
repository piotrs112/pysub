import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from bs4.element import Tag
#from user_agent import generate_user_agent

#file properties for now
q_name = "Chilling Adventures of Sabrina"
q_season = 2
q_episode = 5
q_version = "TBS"

def connect(addr: str):
    #headers = generate_user_agent(os=('win', 'mac', 'linux'))
    r = requests.get(addr) #, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
    return r

def is_right_episode(tag: Tag):
    if tag('td')[1].text == q_episode.__str__():
        return True
    else: return False

#connect to server, get show list
r = connect("https://addic7ed.com")
showlist = BeautifulSoup(r.text, "lxml", parse_only=SoupStrainer(id="qsShow"))


#find tv show & get ID
show = showlist.find(string=q_name).parent
## TODO: add proper search check
if show != None and show != []:
    #print("NAME: {} ID: {}".format(show.get_text(), show.get('value')))
    showID = show.get('value')


#connect to show page & select season & episode
r = connect("https://addic7ed.com/season/{}/{}".format(showID, q_season))
all_subs = BeautifulSoup(r.text, "lxml", parse_only=SoupStrainer('tr')).find_all('tr', {'class': 'epeven'})

ok_subs = []
#format data
for row in all_subs:
    row = row('td')
    for cell in row:
        cell = cell.text
    ok_subs.append({
    'ep': row[1],
    'lang': row[3],
    'vers': row[4],
    })
