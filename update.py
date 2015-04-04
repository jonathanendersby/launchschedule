#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import pytz

months = {'January': 1,'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
          'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12, 'Jan': 1, 
          'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6, 'Jul': 7,'Aug': 8, 'Sep': 9, 'Sept': 9, 'Oct': 10, 
          'Nov': 11, 'Dec': 12 }

url = 'http://spaceflightnow.com/launch-schedule/'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def launch_json():
    data = {'launches': [], 'copyright':'Data from http://spaceflightnow.com/ via Fair Use', 'url':url, 'update_time': str(datetime.datetime.now()) }
    req = requests.get(url, timeout=5)
    soup = BeautifulSoup(req.content, 'html.parser')
    dns = soup('div', {'class': 'datename'})
    mds = soup('div', {'class': 'missiondata'})
    mdescs = soup('div', {'class': 'missdescrip'})

    launches=[]

    if len(dns) == len(mds) == len(mdescs):
        # All our data points match up, we can continue
    
        for i in range(len(dns)):
            launch = {'str_date':unicode(dns[i]), 'str_data': mds[i].text, 
                'description': unicode(mdescs[i].text)}
            launches.append(launch)

    for launch in launches:

        soup = BeautifulSoup(launch['str_date'], 'html.parser')
        launch['launch_date'] = soup('span', {'class': 'launchdate'})[0].text
        launch['mission'] = soup('span', {'class': 'mission'})[0].text
        launch['mission'] = launch['mission'].replace(u'\u2022','|')
        launch['vehicle'] = launch['mission'].split('|')[0].strip()
        launch['mission'] = launch['mission'].split('|')[1].strip()
    
        del launch['str_date'] # delete the mess
    
        data_parts = launch['str_data'].split('\n')
        launch['launch_window'] = data_parts[0].split(':', 1)[1].strip()
    
        hours = minutes = 0
        
        if ' GMT ' in launch['launch_window']:
            hours = minutes = None
            # We've got a GMT lauch time, lets try build a real date.
            # 'May 6'  and '0709 GMT ...'
            # 'Aug. 6'
            
            if is_number(launch['launch_window'][0:4]):
                # caters for "1300-1700 GMT (9 a.m.-1 p.m. EDT)" etc
                hours = launch['launch_window'][0:2]
                minutes = launch['launch_window'][2:4]

                
        clean_date = launch['launch_date'].replace('.','')
        cdp = clean_date.split(' ') # clean date parts
        valid_date = False
        if len(cdp) == 2:
            # we have a two parter, is the first part a month.
            if cdp[0] in months:
            
                # We've got a month
                try:
                    if int(cdp[1]) >= 1 and int(cdp[1]) <= 31:
                        # we've got a day                    
                        launch['gmt_date'] = str(datetime.datetime(2015, months[cdp[0]], 
                            int(cdp[1]), int(hours), int(minutes),0,0, pytz.UTC))
                
                except:
                    launch['gmt_date'] = None

        launch['launch_site'] = data_parts[1].split(':')[1].strip()
        del launch['str_data']
    
        data['launches'] = launches
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    print launch_json()
