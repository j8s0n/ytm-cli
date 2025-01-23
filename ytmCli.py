#!/usr/bin/python
#===================================================================================================
#   CLI client for the youtube-music desktop app:
#   https://github.com/th-ch/youtube-music
#===================================================================================================
import argparse
import subprocess
import time

import requests

NOTIFICATION_ID = 298623
NOTIFY_SEND = '/usr/bin/notify-send'
#===================================================================================================
def main():
  description = 'CLI client for YouTube Music desktop app'
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-i', '--info', action='store_true', dest='info',
                      help='Show track info after command')
  parser.add_argument('-n', '--name', action='store', dest='name', default='localhost',
                      help='The name of the host to connect to (default: localhost)')
  parser.add_argument('-p', '--port', action='store', dest='port', default='26538',
                      help='The port to connect to (default: 26538)')
  parser.add_argument('action', action='store',
                      help='The command to run: next, previous, toggle-play, like, dislike, info')
  args = parser.parse_args()

  if args.action in ['next', 'previous', 'dislike', 'toggle-play']:
    runCommandAndWaitForChange(args.name, args.port, args.action)
    if args.info and not getInfo(args.name, args.port).get('isPaused', False):
      showInfo(args.name, args.port)
  elif args.action in ['like']:
    runCommandAndDoNotWait(args.name, args.port, args.action)
  elif args.action == 'info':
    showInfo(args.name, args.port)

#===================================================================================================
def showInfo(name, port):
  response = getInfo(name, port)
  artist = response.get('artist', '')
  title = response.get('title', '')
  album = response.get('album', '')
  elapsed = formatTime(response.get('elapsedSeconds', 0))
  duration = formatTime(response.get('songDuration', 1))

  command = [NOTIFY_SEND, f'--replace-id={NOTIFICATION_ID}', '--expire-time=3000', title,
             f'{artist}\n{album}\n{elapsed} / {duration}']
  subprocess.check_call(command)

#===================================================================================================
def runCommandAndWaitForChange(name, port, command):
  info = getInfo(name, port)
  oldTitle = info.get('title', '')
  runCommandAndDoNotWait(name, port, command)

  sleepCount = 0
  while info.get('title', '') == oldTitle and sleepCount < 5:
    sleepCount += 1
    time.sleep(0.050)
    info = getInfo(name, port)

#===================================================================================================
def runCommandAndDoNotWait(name, port, command):
  url = f'http://{name}:{port}/api/v1/{command}'
  requests.post(url, timeout=500)

#===================================================================================================
def getInfo(name, port):
  url = f'http://{name}:{port}/api/v1/song-info'
  return requests.get(url, timeout=500).json()

#===================================================================================================
def formatTime(rawSeconds):
  minutes = int(rawSeconds/60)
  seconds = rawSeconds % 60
  return f'{minutes}:{seconds:02}'

#===================================================================================================
if __name__ == '__main__':
  main()
