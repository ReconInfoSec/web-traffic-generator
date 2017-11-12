# web-traffic-generator
A quick and dirty HTTP/S "organic" traffic generator. 

## About
Just a simple (poorly written) Python script that aimlessly "browses" the internet by starting at pre-defined `rootURLs` and randomly "clicking" links on pages until the pre-defined `clickDepth` is met.

I created this as a noise generator to use for an Incident Response / Network Defense simulation. The only issue is that my simulation environment uses multiple IDS/IPS/NGFW devices that will not pass and log simple TCPreplays of canned traffic. I needed the traffic to be as organic as possible, essentially mimicking real users browsing the web. 

Tested on Ubuntu 14.04 & 16.04 minimal, but should work on any system with Python installed.

[![asciicast](https://asciinema.org/a/147170.png)](https://asciinema.org/a/147170)

## How it works
About as simple as it gets...

**First, specify a few settings at the top of the script...**

- `clickDepth = 5` Starting from each root URL (ie: www.yahoo.com), our generator will click `5` links deep before moving to the next root URL.

*The interval between every HTTP GET requests is chosen at random between the following two variables...*

- `minWait = 5` Wait a minimum of `5` seconds between requests... Be careful with making requests to quickly as that tends to piss off web servers.
- `maxWait = 10` I think you get the point.


- `debug = False` A poor mans logger. Set to `True` for verbose realtime logging to console for debugging or development. I'll incorporate proper logging later on (maybe).


- `rootURLs = [url1,url2,url3]` The list of root URLs to start from when browsing. When we hit the end, we simply start back from the beginning.

- `blacklist = [".gif", "intent/tweet", "badlink", etc...]` A blacklist of strings that we check every link against. If the link contains any of the strings in this list, it's discarded. Useful to avoid things that are not traffic-generator friendly like "Tweet this!" links or links to image files.

- `userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3).......'` You guessed it, the user-agent our headless browser hands over to the web server. You can probably leave it set to the default, but feel free to change it. I would strongly suggest using a common/valid one or else you'll likely get rate-limited quick. 

## Dependencies
Only thing you need and *might* not have is `requests`. Grab it with 
```
sudo pip install requests
```

## Usage
Create your config file first: 
```
cp config.py.template config.py
```

Run the generator: 
```
python gen.py
```


## Troubleshooting and debugging
To get more deets on what is happening under the hood, change the Debug variable in `config.py` from `False` to `True`. This provides the following output...

```
Traffic generator started...
----------------------------
https://github.com/ecapuano/web-traffic-generator

Clcking 5 links deep into 7 different root URLs,
waiting between 5 and 10 seconds between requests.

This script will run indefinitely. Ctrl+C to stop.
requesting: https://digg.com/
Page size: 388840
Data meter: 388840 bytes
Good requests: 1
Bad reqeusts: 0
Sleeping for 6 seconds...
------------------------------------------------------
config.blacklist: ['https://t.co', 't.umblr.com', 'messenger.com', 'itunes.apple.com', 'l.facebook.com', 'bit.ly', 'mediawiki', '.css', '.ico', '.xml', 'intent/tweet', 'twitter.com/share', 'signup', 'login', 'dialog/feed?', '.png', '.jpg', '.json', '.svg', '.gif', 'zendesk', 'clickserve']
URL: 1 / 7 -- Depth: 0 / 5
Choosing random link from total: 221
Link chosen: 64 of 221
requesting: http://nautil.us/issue/54/the-unspoken/physics-has-demoted-mass
Page size: 85012
Data meter: 473852 bytes
Good requests: 2
Bad reqeusts: 0
Sleeping for 7 seconds...
------------------------------------------------------
config.blacklist: ['https://t.co', 't.umblr.com', 'messenger.com', 'itunes.apple.com', 'l.facebook.com', 'bit.ly', 'mediawiki', '.css', '.ico', '.xml', 'intent/tweet', 'twitter.com/share', 'signup', 'login', 'dialog/feed?', '.png', '.jpg', '.json', '.svg', '.gif', 'zendesk', 'clickserve']
URL: 1 / 7 -- Depth: 1 / 5
Choosing random link from total: 16
Link chosen: 0 of 16
requesting: http://shop.nautil.us?utm_source=mainsite&utm_medium=popup&utm_campaign=springsale_2017
Page size: 58467
Data meter: 532319 bytes
Good requests: 3
Bad reqeusts: 0
Sleeping for 5 seconds...
------------------------------------------------------
config.blacklist: ['https://t.co', 't.umblr.com', 'messenger.com', 'itunes.apple.com', 'l.facebook.com', 'bit.ly', 'mediawiki', '.css', '.ico', '.xml', 'intent/tweet', 'twitter.com/share', 'signup', 'login', 'dialog/feed?', '.png', '.jpg', '.json', '.svg', '.gif', 'zendesk', 'clickserve']
URL: 1 / 7 -- Depth: 2 / 5
Choosing random link from total: 93
Link chosen: 88 of 93
requesting: http://shop.nautil.us/rss.php?action=popularproducts&amp;type=rss
Page size: 25106
Data meter: 557425 bytes
Good requests: 4
Bad reqeusts: 0
Sleeping for 6 seconds...
------------------------------------------------------
config.blacklist: ['https://t.co', 't.umblr.com', 'messenger.com', 'itunes.apple.com', 'l.facebook.com', 'bit.ly', 'mediawiki', '.css', '.ico', '.xml', 'intent/tweet', 'twitter.com/share', 'signup', 'login', 'dialog/feed?', '.png', '.jpg', '.json', '.svg', '.gif', 'zendesk', 'clickserve']
URL: 1 / 7 -- Depth: 3 / 5
Choosing random link from total: 18
Link chosen: 15 of 18
requesting: http://shop.nautil.us/may-june-2017/
Page size: 62543
Data meter: 619968 bytes
Good requests: 5
Bad reqeusts: 0
Sleeping for 9 seconds...
------------------------------------------------------
config.blacklist: ['https://t.co', 't.umblr.com', 'messenger.com', 'itunes.apple.com', 'l.facebook.com', 'bit.ly', 'mediawiki', '.css', '.ico', '.xml', 'intent/tweet', 'twitter.com/share', 'signup', 'login', 'dialog/feed?', '.png', '.jpg', '.json', '.svg', '.gif', 'zendesk', 'clickserve']
URL: 1 / 7 -- Depth: 4 / 5
Choosing random link from total: 70
Link chosen: 16 of 70
requesting: http://shop.nautil.us/my-test/
Page size: 206
Data meter: 620174 bytes
Good requests: 6
Bad reqeusts: 0
Sleeping for 7 seconds...
^CException on URL: http://shop.nautil.us/my-test/  -- removing from list and trying again!
```

The last URL attempted provides a good example of when a particular URL throws an error. We simply add it to our `config.blacklist` array in memory, and continue browsing. This prevents a known bad URL from returning to the queue. 
