import argparse
import re
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from bs4.element import Tag
#from user_agent import generate_user_agent


#file args
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='TV show filename')
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
args = parser.parse_args()
if args.verbose: print('filename: {}'.format(args.filename))


#file properties for now
search = re.search(r's\d\de\d\d', args.filename)
q_season, q_episode = re.findall(r'\d\d', args.filename[search.span()[0]:search.span()[1]])
q_name = args.filename[0:search.span()[0]].replace('.', ' ').strip().title()
q_version = args.filename[search.span()[1]:]


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
        'download': row[9].a.get('href')
        })


#download srt
r = requests.get("https://addic7ed.com" + subs[0]['download'], allow_redirects=True)
open(args.filename+'.srt', 'wb').write(r.content)


#print out the subtitles
if args.verbose:
    for sub in subs:
        print('{}   {}  {}'.format(sub['lang'], sub['vers'], sub['download']))
