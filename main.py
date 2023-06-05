import  json, ssl, urllib.request
from math import sin, cos, sqrt, atan2, radians

# Approximate radius of earth in km
R = 6373.0

LINE_ACCESS_TOKEN = "S34hJZ2g+F/+0JQ+3hMUcM6rMhPgFcuJG+3btN3DBM/N0udLeyOwcZH4Vr1Sc8/oa44h3d1IVs1kx9AZbF37ABYs/BNgE+acOW4IypudZAgu1KwQgJjbGdDbQTw1aIMX/9OL3lFIXpPhMw7M7i5TZwdB04t89/1O/w1cDnyilFU="
LINE_SECRET_KEY = "bbf752b28f9e378d2b50057b40630a1d"
UBIKE_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

context = ssl._create_unverified_context()

with urllib.request.urlopen(UBIKE_URL, context=context) as jsondata:
     data = json.loads(jsondata.read().decode('utf-8-sig')) 

def get_sites(data, user_lat, user_lng, top_number):
    top_data = []
    for i,v in enumerate(data):
        lat = v["lat"]
        lng = v["lng"]
        dlng = user_lng - lng
        dlat = user_lat - lat
        a = sin(dlat / 2)**2 + cos(lat) * cos(user_lat) * sin(dlng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        if len(top_data) > top_number:
            (max_dist, max_id) = max((v["dist"],j) for j,v in enumerate(top_data))
            if max_dist > distance:
                top_data[max_id] = {"id":i, "dist":distance} 
        else:
            top_data.append({"id":i, "dist":distance})
    
    
    return sorted(top_data, key=lambda k: k['dist'])
    



sites = get_sites(data, 25.033964, 121.564468, 10)

for i in sites:
    d = data[i["id"]]
    sbi = d["sbi"] # available bike 
    tot = d["tot"] # total bike 
    bemp = d["bemp"] # free bike 
    name = d["sna"].replace("YouBike2.0_", "")
    lat, lng = d["lat"], d["lng"]
    google_map_link = "https://www.google.com/maps/search/?api=1&query={},{}".format(lat, lng)
    # userLocation[event.source.userId].latitude;
    # const lng = userLocation[event.source.userId].longitude;
    print(name, i["dist"], google_map_link) 