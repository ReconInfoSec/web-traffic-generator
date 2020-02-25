#!/usr/bin/python

#
# written by @eric_capuano
# https://github.com/ecapuano/web-traffic-generator
#
# published under MIT license :) do what you want.
#
#20170714 shyft ADDED python 2.7 and 3.x compatibility and generic config
from __future__ import print_function 
import requests, re, time, random 
try:
	import config
except ImportError:
	class ConfigClass: #minimal config incase you don't have the config.py
		CLICK_DEPTH = 5 # how deep to browse from the rootURL
		MIN_WAIT = 1 # minimum amount of time allowed between HTTP requests
		MAX_WAIT = 3 # maximum amount of time to wait between HTTP requests
		DEBUG = True # set to True to enable useful console output

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

def do_request(url):
	global data_meter
	global good_requests
	global bad_requests
	sleep_time = random.randrange(config.MIN_WAIT,config.MAX_WAIT)
	
	if config.DEBUG:
		print("requesting: %s" % url)
	
	headers = {'user-agent': config.USER_AGENT}
	
	try:
		r = requests.get(url, headers=headers, timeout=5)
	except:
		time.sleep(30) # else we'll enter 100% CPU loop in a net down situation
		return False
		
	status = r.status_code
	
	page_size = len(r.content)
	data_meter = data_meter + page_size

	
	if config.DEBUG:
		print("Page size: %s" % page_size)
		if ( data_meter > 1000000 ):
			print("Data meter: %s MB" % (data_meter / 1000000))
		else:
			print("Data meter: %s bytes" % data_meter)
	
	if ( status != 200 ):
		bad_requests+=1
		if config.DEBUG:
			print("Response status: %s" % r.status_code)
		if ( status == 429 ):
			if config.DEBUG:
				print("We're making requests too frequently... sleeping longer...")
			sleep_time+=30
	else:
		good_requests+=1
	
	# need to sleep for random number of seconds!
	if config.DEBUG:
		print("Good requests: %s" % good_requests)
		print("Bad reqeusts: %s" % bad_requests)
		print("Sleeping for %s seconds..." % sleep_time)
		
	time.sleep(sleep_time)
	return r

def get_links(page):
	links=[]

	pattern=r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
	
	matches = re.findall(pattern,str(page.content))
	
	for match in matches: # check all matches against config.blacklist
		if any(bl in match for bl in config.blacklist):
			pass
		else:
			links.insert(0,match)
		
	return links

def browse(urls):
	current_url = 1
	for url in urls:
		url_count = len(urls)

		page = do_request(url)  # hit current root URL
		if page:
			links = get_links(page) # extract links from page
			link_count = len(links)
		else:
			if config.DEBUG:
				print("Error requesting %s" % url)
			continue
			
			
		depth=0
		while ( depth < config.CLICK_DEPTH ):
			if config.DEBUG:
				print("------------------------------------------------------")
				print("config.blacklist: %s" % config.blacklist )
			# set the link count, which will change throughout the loop
			link_count = len(links)
			if ( link_count > 1): # make sure we have more than 1 link to use
			
				if config.DEBUG:
					print("URL: %s / %s -- Depth: %s / %s" \
						% (current_url,url_count,depth,config.CLICK_DEPTH))
					print("Choosing random link from total: %s" % link_count)
					
				random_link = random.randrange(0,link_count - 1)
				
				if config.DEBUG:
					print("Link chosen: %s of %s" % (random_link,link_count))
					
				click_link = links[random_link]
				
				try:
					# browse to random link on rootURL
					sub_page = do_request(click_link)
					if sub_page:
						check_link_count = len(get_links(sub_page))
					else:
						if config.DEBUG:
							print("Error requesting %s" % url)
						break
					
					
					check_link_count = len(get_links(sub_page))

					# make sure we have more than 1 link to pick from 
					if ( check_link_count > 1 ):
						# extract links from the new page
						links = get_links(sub_page)
					else:
						# else retry with current link list
						if config.DEBUG:
							print("Not enough links found! Found: %s  -- " \
								"Going back up a level" % check_link_count)
						config.blacklist.insert(0,click_link)
						# remove the dead-end link from our list
						del links[random_link]
				except:
					if config.DEBUG:
						print("Exception on URL: %s  -- " \
							"removing from list and trying again!" % click_link)
					# I need to expand more on exception type for config.debugging
					config.blacklist.insert(0,click_link)
					# remove the dead-end link from our list
					del links[random_link] 
					pass
				# increment counter whether request was successful or not 
				# so that we don't end up in an infinite failed request loop
				depth+=1
			else:
				# we land here if we went down a path that dead-ends
				# could implement logic to simply restart at same root
				if config.DEBUG:
					print("Hit a dead end...Moving to next Root URL")
				config.blacklist.insert(0,click_link)
				depth = config.CLICK_DEPTH 
			
		
		current_url+=1 # increase rootURL iteration
	if config.DEBUG:
		print("Done.")

# initialize our global variables
data_meter = 0
good_requests = 0
bad_requests = 0

while True:
	print("Traffic generator started...")
	print("----------------------------")
	print("https://github.com/ecapuano/web-traffic-generator")
	print("")
	print("Clicking %s links deep into %s different root URLs, " \
		% (config.CLICK_DEPTH,len(config.ROOT_URLS)))
	print("waiting between %s and %s seconds between requests. " \
		% (config.MIN_WAIT,config.MAX_WAIT))
	print("")
	print("This script will run indefinitely. Ctrl+C to stop.")
	browse(config.ROOT_URLS)
