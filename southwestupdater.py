#!/usr/bin/python
import requests
import time
import json
from datetime import datetime
import smtplib

url = r'https://www.southwest.com/api/air-operations/v1/air-operations/api/air/flights/status'
dep_data = {"originationAirportCode":"DEN","destinationAirportCode":"AUS","departureDate":"2016-04-29","flightNumber":"2317"}
ret_data = {"originationAirportCode":"AUS","destinationAirportCode":"DEN","departureDate":"2016-05-01","flightNumber":"5251"}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'en-US,en;q=0.8',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Length': '114',
  'Content-Type': 'application/json',
  'Cookie': 'AMCV_65D316D751E563EC0A490D4C%40AdobeOrg=283337926%7CMCIDTS%7C16920%7CMCMID%7C04453000527618196929045432390817030668%7CMCAID%7CNONE; s_fid=3C33536B3E48AEAF-38604F3540350392; s_cc=True; akavpau_prod_fullsite=1461864910~id=168caaaab8bd45a5515ba52835343080',
  'Host': 'www.southwest.com',
  'Origin': 'https://www.southwest.com',
  'Referer': 'https://www.southwest.com/air/flight-status/results.html?originationAirportCode=DEN&destinationAirportCode=AUS&departureDate=2016-04-29&flightNumber=2317',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
  'X-API-Key': 'l7xx944d175ea25f4b9c903a583ea82a1c4c',
  'X-User-Experience-ID': '698f5ba5-d2d7-4119-b0d1-287afa7dca58'
}

email_from = 'jabrouwerutil@gmail.com'
email_to = ['8328183641@tmomail.net', 'jabrouwer82@gmail.com']
old_dep_status = 'none'
new_dep_status = 'none'
old_dep_time = 'none'
new_dep_time = 'none'
old_arr_status = 'none'
new_arr_status = 'none'
old_status = 'none'
new_statue = 'none'


def check_dep_status():
  print('Checking departure status')
  return requests.post(url, data=json.dumps(dep_data), headers=headers)

def check_ret_status():
  print('Checking return status')
  return requests.post(url, data=json.dumps(ret_data), headers=headers)

def canceled():
  print('Checking canceled status')
  return 'cancel' in (new_dep_status + old_arr_status).lower()

def flight_departed():
  print('Checking if the plane has departed')
  dep_time = datetime.strptime(new_dep_time, '%H:%M')
  dep_datetime = datetime.now().replace(hour=dep_time.hour, minute=dep_time.minute)
  now = datetime.now()
  return (now - dep_datetime).days >= 0 and (now - dep_datetime).seconds > 10*60

def should_notify():
  print('Checking if a notification should be sent')
  if new_status != old_status:
    return True
  return False

def notify():
  print('-- Sending notification --')
  message = ''
  if new_dep_status != old_dep_status:
    message += 'Departure status changed from {old} to {new}\n'.format(old=old_dep_status, new=new_dep_status)
  if new_dep_time != old_dep_time:
    message += 'Departure time changed from {old} to {new}\n'.format(old=old_dep_time, new=new_dep_time)
  if new_arr_status != old_arr_status:
    message += 'Arrival status changed from {old} to {new}\n'.format(old=old_arr_status, new=new_arr_status)
  message += '\n\n'
  message += 'Old status was:\n{old_status}\n\nNew status is:\n{new_status}'.format(old_status=json.dumps(old_status, sort_keys=True, indent=2, separators=(',', ': ')), new_status=json.dumps(new_status, sort_keys=True, indent=2, separators=(',', ': ')))

  server = smtplib.SMTP('smtp.gmail.com:587')
  server.ehlo()
  server.starttls()
  server.login('jabrouwerutil@gmail.com', 'utilpassword')
  for email in email_to:
    server.sendmail(email_from, email, message)
  server.close()

def start():
  print('Starting')
  global old_dep_status
  global old_dep_time
  global old_arr_status
  global old_status
  global new_dep_status
  global new_dep_time
  global new_arr_status
  global new_status
  while True:
    response = check_dep_status()
    new_status = response.json()['data']['searchResults'][0]['summary']
    new_dep_status = new_status['departureStatus']
    new_dep_time = new_status['departureTime']
    new_arr_status = new_status['arrivalStatus']

    if should_notify():
      notify();

    old_dep_status = new_dep_status
    old_dep_time = new_dep_time
    old_arr_status = new_arr_status
    old_status = new_status

    if canceled():
      print('-- Flight canceled --')
      break
    if flight_departed():
      print('-- Flight departed --')
      break
    time.sleep(60)

if __name__ == '__main__':
  start()



