import argparse
import re
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from bs4.element import Tag
#from user_agent import generate_user_agent


#file args
parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='TV show filename')
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
args = parser.parse_args()
if args.verbose: print('Filename: {}'.format(args.filename))


args.verbose = True
#file properties for now
filename = 'the.magicians.(2016).s02e05.web.x264-sva[ettv].mkv'
search = re.search(r's\d\de\d\d', filename)
q_season, q_episode = re.findall(r'\d\d', filename[search.span()[0]:search.span()[1]])
q_name = filename[0:search.span()[0]].replace('.', ' ').strip().title()
q_version = filename[search.span()[1]:]

query = {
q_season,
q_episode,
q_name,
q_version,
}
print(q_name)

def connect(addr: str):
    #headers = generate_user_agent(os=('win', 'mac', 'linux'))
    r = requests.get(addr) #, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
    return r

def is_right_episode(tag: Tag):
    if tag('td')[1].text == query.q_episode.__str__():
        return True
    else: return False

#connect to server, get show list
r = connect('https://addic7ed.com')
showlist = BeautifulSoup(r.text, 'lxml', parse_only=SoupStrainer(id='qsShow'))


#find tv show & get ID
show = showlist.find(string=q_name).parent
## TODO: add proper search check
if show != None and show != []:
    #print('NAME: {} ID: {}'.format(show.get_text(), show.get('value')))
    showID = show.get('value')


#connect to show page & select season & episode
r = connect('https://addic7ed.com/season/{}/{}'.format(showID, q_season))
all_subs = BeautifulSoup(r.text, 'lxml', parse_only=SoupStrainer('tr')).find_all('tr', {'class': 'epeven'})

subs = []
#format data
for row in all_subs:
    row = row('td')
    if row[3].text == 'English' and re.search(row[4].text.upper(), q_version.upper()) != None and int(row[1].text) == int(q_episode):
        subs.append({
        'lang': row[3].text,
        'vers': row[4].text,
        })


#filters



#print out the subtitles
if args.verbose:
    for sub in subs:
        print('{}   {}'.format(sub['lang'], sub['vers']))
