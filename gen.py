#!/usr/bin/python

#
# written by @eric_capuano
# https://github.com/ecapuano/web-traffic-generator
#
# published under MIT license :) do what you want.
#
#20170714 shyft ADDED python 2.7 and 3.x compatibility and generic config
#20200225 rarawls ADDED recursive, depth-first browsing, color stdout
from __future__ import print_function 
import requests, re, time, random 
try:
    import config
except ImportError:
    class ConfigClass:  # minimal config incase you don't have the config.py
        MAX_DEPTH = 10  # dive no deeper than this for each root URL
        MIN_DEPTH = 3   # dive at least this deep into each root URL
        MAX_WAIT = 10   # maximum amount of time to wait between HTTP requests
        MIN_WAIT = 5    # minimum amount of time allowed between HTTP requests
        DEBUG = True    # set to True to enable useful console output

        # use this single item list to test how a site responds to this crawler
        # be sure to comment out the list below it.
        #ROOT_URLS = ["https://digg.com/"] 
        ROOT_URLS = [
            "https://www.reddit.com"
            ]


        # items can be a URL "https://t.co" or simple string to check for "amazon"
        blacklist = [
            'facebook.com',
            'pinterest.com'
            ]  

        # must use a valid user agent or sites will hate you
        USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    config = ConfigClass 

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    NONE = '\033[0m'


def debug_print(message, color=Colors.NONE):
    """ A method which prints if DEBUG is set """
    if config.DEBUG:
        print(color + message + Colors.NONE)


def hr_bytes(bytes_, suffix='B', si=False):
    """ A method providing a more legible byte format """

    bits = 1024.0 if si else 1000.0

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes_) < bits:
            return "{:.1f}{}{}".format(bytes_, unit, suffix)
        bytes_ /= bits
    return "{:.1f}{}{}".format(bytes_, 'Y', suffix)


def do_request(url):
    """ A method which loads a page """

    global data_meter
    global good_requests
    global bad_requests

    debug_print("  Requesting page...".format(url))

    headers = {'user-agent': config.USER_AGENT}

    try:
        r = requests.get(url, headers=headers, timeout=5)
    except:
        # Prevent 100% CPU loop in a net down situation
        time.sleep(30)
        return False

    page_size = len(r.content)
    data_meter += page_size

    debug_print("  Page size: {}".format(hr_bytes(page_size)))
    debug_print("  Data meter: {}".format(hr_bytes(data_meter)))

    status = r.status_code

    if (status != 200):
        bad_requests += 1
        debug_print("  Response status: {}".format(r.status_code), Colors.RED)
        if (status == 429):
            debug_print(
                "  We're making requests too frequently... sleeping longer...")
            config.MIN_WAIT += 10
            config.MAX_WAIT += 10
    else:
        good_requests += 1

    debug_print("  Good requests: {}".format(good_requests))
    debug_print("  Bad reqeusts: {}".format(bad_requests))

    return r


def get_links(page):
    """ A method which returns all links from page, less blacklisted links """

    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(page.content))
    valid_links = [link for link in links if not any(
        b in link for b in config.blacklist)]
    return valid_links


def recursive_browse(url, depth):
    """ A method which recursively browses URLs, using given depth """
    # Base: load current page and return
    # Recursively: load page, pick random link and browse with decremented depth

    debug_print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    debug_print(
        "Recursively browsing [{}] ~~~ [depth = {}]".format(url, depth))

    if not depth:  # base case: depth of zero, load page

        do_request(url)
        return

    else:  # recursive case: load page, browse random link, decrement depth

        page = do_request(url)  # load current page

        # give up if error loading page
        if not page:
            debug_print(
                "  Stopping and blacklisting: page error".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        # scrape page for links not in blacklist
        debug_print("  Scraping page for links".format(url))
        valid_links = get_links(page)
        debug_print("  Found {} valid links".format(len(valid_links)))

        # give up if no links to browse
        if not valid_links:
            debug_print("  Stopping and blacklisting: no links".format(
                url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        # sleep and then recursively browse
        sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
        print("  Pausing for {} seconds...".format(sleep_time))
        time.sleep(sleep_time)

        recursive_browse(random.choice(valid_links), depth - 1)


if __name__ == "__main__":

    # Initialize global variables
    data_meter = 0
    good_requests = 0
    bad_requests = 0

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Traffic generator started")
    print("https://github.com/ecapuano/web-traffic-generator")
    print("Diving between 3 and {} links deep into {} root URLs,".format(
        config.MAX_DEPTH, len(config.ROOT_URLS)))
    print("Waiting between {} and {} seconds between requests. ".format(
        config.MIN_WAIT, config.MAX_WAIT))
    print("This script will run indefinitely. Ctrl+C to stop.")

    while True:

        debug_print("Randomly selecting one of {} Root URLs".format(
            len(config.ROOT_URLS)), Colors.PURPLE)

        random_url = random.choice(config.ROOT_URLS)
        depth = random.choice(range(config.MIN_DEPTH, config.MAX_DEPTH))

        recursive_browse(random_url, depth)

