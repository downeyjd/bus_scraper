import requests, bs4, time, csv

#### setup variables
f_writeout = 1 #binary flag to enable logging to local CSV file
sb_url = 'https://buseta.wmata.com/m/index?q=1003237' #test url, ft totten station bus stop
nb_url = 'https://buseta.wmata.com/m/index?q=2001159' #test url, twinbrook station bus stop
#sb_url = 'https://buseta.wmata.com/m/index?q=3002518' #url for laurel-bowie & montpelier south-bound route 87 bus stop
#nb_url = 'https://buseta.wmata.com/m/index?q=3002573' #url for greenbelt metro north-bound route 87 bus stop
distances = ['approaching', 'at stop'] #bus distance statuses to capture, i.e., don't log "2.3 miles" statuses
max_time = 3 #time in minutes away from stop under which to start logging presence
route_names = ['E4  WEST to FRIENDSHIP HEIGHTS', 'C4  EAST to PRINCE GEORGES PLAZA STATION'] #test routes to capture on bus stop pages
####################

temp = []
results = []
nb_pagedata = requests.get(nb_url)
sb_pagedata = requests.get(sb_url)
current_date = time.strftime('%x')
current_time = time.strftime('%X')
nb_cleanpagedata = bs4.BeautifulSoup(nb_pagedata.text, 'html.parser')
sb_cleanpagedata = bs4.BeautifulSoup(sb_pagedata.text, 'html.parser')
nb_arrivals = nb_cleanpagedata.find_all(class_='arrivalsAtStop')
sb_arrivals = sb_cleanpagedata.find_all(class_='arrivalsAtStop')

for arrival in nb_arrivals:
    for hit in arrival.parent.strings:
        temp.append(hit.strip(', ').replace('\xa0', ' '))

for arrival in sb_arrivals:
    for hit in arrival.parent.strings:
        temp.append(hit.strip(', ').replace('\xa0', ' '))

if (int(temp[1].split(' ')[0]) < max_time or temp[2] in distances) and temp[0] in route_names:
    results.append([current_date, current_time, temp[0], temp[1], temp[2], temp[3]])

if f_writeout:
    if results:
        with open(r'bus_log.csv', 'a') as f:
            logger = csv.writer(f)
            logger.writerows(results)
        f.close()
else:
    print(results)
