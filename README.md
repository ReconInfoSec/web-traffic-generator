# web-traffic-generator
A quick and dirty HTTP/S "organic" traffic generator. 

## About
Just a simple (poorly written) Python script that aimlessly "browses" the internet by starting at pre-defined `rootURLs` and randomly "clicking" links on pages until the pre-defined `clickDepth` is met.

I created this as a noise generator to use for an Incident Response / Network Defense simulation. The only issue is that my simulation environment uses multiple IDS/IPS/NGFW devices that will not pass and log simple TCPreplays of canned traffic. I needed the traffic to be as organic as possible, essentially mimicking real users browsing the web. 

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
Only thing you need and *might* not have is `requests`. Grab it with `sudo pip install requests`

## Usage
`python gen.py`
