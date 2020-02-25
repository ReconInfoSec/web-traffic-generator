# web-traffic-generator

A quick and dirty HTTP/S "organic" traffic generator.

## About

Just a simple (poorly written) Python script that aimlessly "browses" the internet by starting at pre-defined `ROOT_URLS` and randomly "clicking" links on pages until the pre-defined `MAX_DEPTH` is met.

I created this as a noise generator to use for an Incident Response / Network Defense simulation. The only issue is that my simulation environment uses multiple IDS/IPS/NGFW devices that will not pass and log simple TCPreplays of canned traffic. I needed the traffic to be as organic as possible, essentially mimicking real users browsing the web.

Tested on Ubuntu 14.04 & 16.04 minimal, but should work on any system with Python installed.

[![asciicast](https://asciinema.org/a/304683.png)](https://asciinema.org/a/304683)

## How it works

About as simple as it gets...

**First, specify a few settings at the top of the script...**

- `MAX_DEPTH = 10`, `MIN_DEPTH = 5` Starting from each root URL (ie: www.yahoo.com), our generator will click to a depth
radomly selected between MIN_DEPTH and MAX_DEPTH.

*The interval between every HTTP GET requests is chosen at random between the following two variables...*

- `MIN_WAIT = 5` Wait a minimum of `5` seconds between requests... Be careful with making requests to quickly as that tends to piss off web servers.
- `MAX_WAIT = 10` I think you get the point.

- `DEBUG = False` A poor man's logger. Set to `True` for verbose realtime printing to console for debugging or development. I'll incorporate proper logging later on (maybe).

- `ROOT_URLS = [url1,url2,url3]` The list of root URLs to start from when browsing. Randomly selected.

- `blacklist = [".gif", "intent/tweet", "badlink", etc...]` A blacklist of strings that we check every link against. If the link contains any of the strings in this list, it's discarded. Useful to avoid things that are not traffic-generator friendly like "Tweet this!" links or links to image files.

- `userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3).......'` You guessed it, the user-agent our headless browser hands over to the web server. You can probably leave it set to the default, but feel free to change it. I would strongly suggest using a common/valid one or else you'll likely get rate-limited quick.

## Dependencies

Only thing you need and *might* not have is `requests`. Grab it with

```bash
sudo pip install requests
```

## Usage

Create your config file first:

```bash
cp config.py.template config.py
```

Run the generator:

```bash
python gen.py
```

## Troubleshooting and debugging

To get more deets on what is happening under the hood, change the Debug variable in `config.py` from `False` to `True`. This provides the following output...

```console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Traffic generator started
Diving between 3 and 10 links deep into 489 different root URLs,
Waiting between 5 and 10 seconds between requests.
This script will run indefinitely. Ctrl+C to stop.
Randomly selecting one of 489 URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursively browsing [https://arstechnica.com] ~~~ [depth = 7]
  Requesting page...
  Page size: 77.6KB
  Data meter: 77.6KB
  Good requests: 1
  Bad reqeusts: 0
  Scraping page for links
  Found 171 valid links
  Pausing for 7 seconds...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursively browsing [https://arstechnica.com/author/jon-brodkin/] ~~~ [depth = 6]
  Requesting page...
  Page size: 75.7KB
  Data meter: 153.3KB
  Good requests: 2
  Bad reqeusts: 0
  Scraping page for links
  Found 168 valid links
  Pausing for 9 seconds...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursively browsing [https://arstechnica.com/information-technology/2020/01/directv-races-to-decommission-broken-boeing-satellite-before-it-explodes/] ~~~ [depth = 5]
  Requesting page...
  Page size: 43.8KB
  Data meter: 197.1KB
  Good requests: 3
  Bad reqeusts: 0
  Scraping page for links
  Found 32 valid links
  Pausing for 8 seconds...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursively browsing [https://www.facebook.com/sharer.php?u=https%3A%2F%2Farstechnica.com%2F%3Fpost_type%3Dpost%26p%3D1647915] ~~~ [depth = 4]
  Requesting page...
  Page size: 64.2KB
  Data meter: 261.2KB
  Good requests: 4
  Bad reqeusts: 0
  Scraping page for links
  Found 0 valid links
  Stopping and blacklisting: no links
```

The last URL attempted provides a good example of when a particular URL throws an error. We simply add it to our `config.blacklist` array in memory, and continue browsing. This prevents a known bad URL from returning to the queue.
