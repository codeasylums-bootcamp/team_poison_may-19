import requests
import json
req = requests.get('https://api.railwayapi.com/v2/between/source/rnc/dest/ndls/date/30-05-2019/apikey/3fpm2m6sqr/')
req = req.json()
for i in req['trains']:
    if i['from_station']['code']=='RNC' and i['to_station']['code']=='NDLS':
        print(i['name'],i['number'])