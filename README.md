# ytm-cli

A CLI script to control [youtube-music](https://github.com/th-ch/youtube-music)

Call the script with one of:

- toggle-play
- previous
- next
- like
- dislike
- info

to perform that action. You can specify a host and port, or use the defaults.

If you have notify-send installed, you can show the newly playing track info.

```
usage: ytmCli.py [-h] [-i] [-n NAME] [-p PORT] action

CLI client for YouTube Music desktop app

positional arguments:
action The command to run: next, previous, toggle-play, like, dislike, info

options:
  -h, --help show this help message and exit
  -i, --info Show track info after command
  -n, --name NAME The name of the host to connect to (default: localhost)
  -p, --port PORT The port to connect to (default: 26538)
```
