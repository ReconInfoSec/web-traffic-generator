#!/usr/bin/python

import requests, re, time, random, config


def doRequest(url):
	global dataMeter
	global goodRequests
	global badRequests
	sleepTime = random.randrange(config.minWait,config.maxWait)
	
	if config.debug:
		print "requesting: %s" % url
	
	headers = {'user-agent': config.userAgent}
	
	try:
		r = requests.get(url, headers=headers)
	except:
		return False
		
	status = r.status_code
	
	pageSize = len(r.content)
	dataMeter = dataMeter + pageSize

	
	if config.debug:
		print "Page size: %s" % pageSize
		if ( dataMeter > 1000000 ):
			print "Data meter: %s MB" % (dataMeter / 1000000)
		else:
			print "Data meter: %s bytes" % dataMeter
	
	if ( status != 200 ):
		badRequests+=1
		if config.debug:
			print "Response status: %s" % r.status_code
		if ( status == 429 ):
			if config.debug:
				print "We're making requests too frequently... sleeping longer..."
			sleepTime+=30
	else:
		goodRequests+=1
	
	# need to sleep for random number of seconds!
	if config.debug:
		print "Good requests: %s" % goodRequests
		print "Bad reqeusts: %s" % badRequests
		print "Sleeping for %s seconds..." % sleepTime
		
	time.sleep(sleepTime)
	return r

def getLinks(page):
	links=[]

	pattern=r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
	
	matches = re.findall(pattern,page.content)
	
	for match in matches: # check all matches against config.blacklist
		if any(bl in match for bl in config.blacklist):
			pass
		else:
			links.insert(0,match)
		
	return links

def browse(urls):
	currURL = 1
	for url in urls:
		urlCount = len(urls)

		page = doRequest(url)  # hit current root URL
		if page:
			links = getLinks(page) # extract links from page
			linkCount = len(links)
		else:
			if config.debug:
				print "Error requesting %s" % url
			continue
			
			
		depth=0
		while ( depth < config.clickDepth ):
			if config.debug:
				print "------------------------------------------------------"
				print "config.blacklist: %s" % config.blacklist 
			# set the link count, which will change throughout the loop
			linkCount = len(links)
			if ( linkCount > 1): # make sure we have more than 1 link to use
			
				if config.debug:
					print "URL: %s / %s -- Depth: %s / %s" \
						% (currURL,urlCount,depth,config.clickDepth)
					print "Choosing random link from total: %s" % linkCount
					
				randomLink = random.randrange(0,linkCount - 1)
				
				if config.debug:
					print "Link chosen: %s of %s" % (randomLink,linkCount)
					
				clickLink = links[randomLink]
				
				try:
					# browse to random link on rootURL
					sub_page = doRequest(clickLink)
					if sub_page:
						checkLinkCount = len(getLinks(sub_page))
					else:
						if config.debug:
							print "Error requesting %s" % url
						break
					
					
					checkLinkCount = len(getLinks(sub_page))

					# make sure we have more than 1 link to pick from 
					if ( checkLinkCount > 1 ):
						# extract links from the new page
						links = getLinks(sub_page)
					else:
						# else retry with current link list
						if config.debug:
							print "Not enough links found! Found: %s  -- " \
								"Going back up a level" % checkLinkCount
						config.blacklist.insert(0,clickLink)
						# remove the dead-end link from our list
						del links[randomLink]
				except:
					if config.debug:
						print "Exception on URL: %s  -- " \
							"removing from list and trying again!" % clickLink
					# I need to expand more on exception type for config.debugging
					config.blacklist.insert(0,clickLink)
					# remove the dead-end link from our list
					del links[randomLink] 
					pass
				# increment counter whether request was successful or not 
				# so that we don't end up in an infinite failed request loop
				depth+=1
			else:
				# we land here if we went down a path that dead-ends
				# could implement logic to simply restart at same root
				if config.debug:
					print "Hit a dead end...Moving to next Root URL"
				config.blacklist.insert(0,clickLink)
				depth = config.clickDepth 
			
		
		currURL+=1 # increase rootURL iteration
	if config.debug:
		print "Done."

# initialize our global variables
dataMeter = 0
goodRequests = 0
badRequests = 0

while True:
	print "Traffic generator started..."
	print "----------------------------"
	print "https://github.com/ecapuano/web-traffic-generator"
	print ""
	print "Clicking %s links deep into %s different root URLs, " \
		% (config.clickDepth,len(config.rootURLs))
	print "waiting between %s and %s seconds between requests. " \
		% (config.minWait,config.maxWait)
	print ""
	print "This script will run indefinitely. Ctrl+C to stop."
	browse(config.rootURLs)
