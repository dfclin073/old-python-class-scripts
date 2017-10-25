#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import requests

def main():
    queue = ["http://10.0.0.210:8084"]
    count = 0
    jar = ''
    download = requests.get(queue.pop(), cookies=jar)
    jar = download.cookies
    while  (count < 45):
        count = count + 1
        print count
        print queue
        soup = BeautifulSoup(download.text)

        for link in soup.findAll('a'):
        #turns link into a string split the string on the " then turns it into a list prints the second item
        #print str(link).split("\"")[1]
            print str(link.get('href'))
            queue.append(str(link.get('href')))
        download = requests.get(queue.pop(), cookies=jar)
    print download.text
if __name__ == "__main__":
    main()
