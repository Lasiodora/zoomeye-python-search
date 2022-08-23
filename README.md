# Simple searcher for ZoomEye 

First of all, you should set API-KEY in code.

***
```
usage: zoomeye_search.py [-h] [-o FILE_NAME] -d DORK [-p PAGE] [--ip IP]
                         [--url URL]

optional arguments:

  -h, --help    show this help message and exit
  -o FILE_NAME  output file                         default value = output.txt
  -d DORK       zoomeye dork. example: Apache       No default. You should set zoomyeye dork
  -p PAGE       Count of pages from ZoomEye         default value = 5 (this is not enough, so set 50 or more)
  --ip IP       output IP:PORT                      default value = False ()
  --url URL     output https://URL                  default value = True

```
---

## Example starting
```
python3 zoomeye_search.py -d app:"Microsoft IIS httpd"+country:"DE" -p 50 --ip True --url False -o my_out_file.txt
```

