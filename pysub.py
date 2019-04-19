import requests
from bs4 import BeautifulSoup
#from user_agent import generate_user_agent

#file properties for now
q_name = "Chilling Adventures of Sabrina"
q_season = 2
q_episode = 5
q_version = "TBS"

def connect(addr: str) -> requests.models.Response:
    #headers = generate_user_agent(os=('win', 'mac', 'linux'))
    r = requests.get(addr) #, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
    return r


#connect to server
r = connect("https://addic7ed.com")


#get shows list
soup = BeautifulSoup(r.text, "lxml")
body = soup.body
showlist = body.find('select', {'id':'qsShow'})


#find tv show & get ID
show = showlist.find(string=q_name).parent

## TODO: add proper search check
if show != None and show != []:
    #print("NAME: {} ID: {}".format(show.get_text(), show.get('value')))
    showID = show.get('value')


#connect to show page & select season & episode
r = connect("https://addic7ed.com/season/{}/{}".format(showID, q_season))
soup = BeautifulSoup(r.text, "lxml")
body = soup.body
print(body)
