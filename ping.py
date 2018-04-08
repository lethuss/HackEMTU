import subprocess
import re, datetime
import requests
from requests.auth import HTTPBasicAuth
import pymongo


client = pymongo.MongoClient()
db = client['hack']
collection = db.data

linha = 197


def getIps():
    ip_re = re.compile("(?P<ip>[\d]+\.[\d]+\.[\d]+\.[\d]+)")
    #mac_re = re.compile("(?P<mac>[\w\d]{2}:[\w\d]{2}:[\w\d]{2}:[\w\d]{2}:[\w\d]{2}:[\w\d]{2})")
    cmd = 'nmap -sP --host-timeout=5000ms --max-retries=2 192.168.40.1/24'.split()
    #cmd = 'arp -a -n'.split()

    a = subprocess.check_output(cmd)

    #ips_raw = re.findall(ip_re,a)

    # for item in ips_raw:
    #     cmd2 = ('ping -c 1 ' + item + ' -W 1').split()
    #     print (cmd2)
    #     try:
    #         print(subprocess.check_output(cmd2))
    #     except:
    #         pass


    return re.findall(ip_re,a)





now = {}
in_check = {}

while True:

    ips = getIps()

    for ip in ips:
        if not(ip in now.keys()) and  not(ip in in_check.keys()):

            data = requests.get('https://noxxonsat-nxnet.appspot.com/rest/usuarios/v2?linha=052',auth=HTTPBasicAuth('hackatona2018-10', 'unicamp2018-10'))
            data = data.json()

            lat = data['linhas'][0]['veiculos'][0]['latitude']
            lon = data['linhas'][0]['veiculos'][0]['longitude']

            in_check[ip] = {'d': datetime.datetime.utcnow(),
                       'i': 0,
                       'lat': lat,
                       'lon':lon
                       }

        else:

            if ip in in_check.keys():
                if in_check[ip]['i'] < 6:
                    in_check[ip]['i'] += 1
                else:
                    now[ip] = in_check[ip]
                    del in_check[ip]
            else:
                now[ip]['i'] = 0

    for key in now.keys():
        if not(key in ips):
            if now[key]['i'] < 5:
                now[key]['i'] += 1
            else:
                data = requests.get('https://noxxonsat-nxnet.appspot.com/rest/usuarios/v2?linha=052', auth=HTTPBasicAuth('hackatona2018-10', 'unicamp2018-10'))
                data = data.json()

                lat = data['linhas'][0]['veiculos'][0]['latitude']
                lon = data['linhas'][0]['veiculos'][0]['longitude']

                aux = {
                    'lat': lat,
                    'lon': lon,
                    'lat_orig': now[key]['lat'],
                    'long_orig': now[key]['lon'],
                    'time_orig': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
                    'id_orig': key
                    }

                post_id = collection.insert_one(aux)


                print ("{} | {} - {} | {} {} - {} {}".format(key, now[key]['d'], datetime.datetime.utcnow(),now[key]['lat'],now[key]['lon'], lat, lon))
                now.pop(key)


    print len(now)