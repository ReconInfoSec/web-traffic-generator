#!/usr/bin/python

import requests, re, time, random


clickDepth = 5 # how deep to browse from the rootURL
minWait = 5 # minimum amount of time allowed between HTTP requests
maxWait = 10 # maximum amount of time to wait between HTTP requests
debug = False # set to True to enable useful console output

# use this single item list to test how a site responds to this crawler
# be sure to comment out the list below it.
#rootURLs = ["https://digg.com/"] 

rootURLs = [
	"https://digg.com/",
	"https://www.yahoo.com",
	"https://www.reddit.com",
	"http://www.cnn.com",
	"http://www.ebay.com",
	"https://en.wikipedia.org/wiki/Main_Page",
	"https://austin.craigslist.org/"
	]


# items can be a URL "https://t.co" or simple string to check for "amazon"
blacklist = [
	"https://t.co", 
	"t.umblr.com", 
	"messenger.com", 
	"itunes.apple.com", 
	"l.facebook.com", 
	"bit.ly", 
	"mediawiki", 
	".css", 
	".ico", 
	".xml", 
	"intent/tweet", 
	"twitter.com/share", 
	"signup", 
	"login", 
	"dialog/feed?", 
	".png", 
	".jpg", 
	".json", 
	".svg", 
	".gif", 
	"zendesk",
	"clickserve"
	]  

# must use a valid user agent or sites will hate you
userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
	'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


def doRequest(url):
	global dataMeter
	global goodRequests
	global badRequests
	sleepTime = random.randrange(minWait,maxWait)
	
	if debug:
		print "requesting: %s" % url
	
	headers = {'user-agent': userAgent}
	r = requests.get(url, headers=headers)
	
	status = r.status_code
	
	pageSize = len(r.content)
	dataMeter = dataMeter + pageSize

	
	if debug:
		print "Page size: %s" % pageSize
		if ( dataMeter > 1000000 ):
			print "Data meter: %s MB" % (dataMeter / 1000000)
		else:
			print "Data meter: %s bytes" % dataMeter
	
	if ( status != 200 ):
		badRequests+=1
		if debug:
			print "Response status: %s" % r.status_code
		if ( status == 429 ):
			if debug:
				print "We're making requests too frequently... sleeping longer..."
			sleepTime+=30
	else:
		goodRequests+=1
	
	# need to sleep for random number of seconds!
	if debug:
		print "Good requests: %s" % goodRequests
		print "Bad reqeusts: %s" % badRequests
		print "Sleeping for %s seconds..." % sleepTime
		
	time.sleep(sleepTime)
	return r

def getLinks(page):
	links=[]

	pattern=r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
	
	matches = re.findall(pattern,page.content)
	
	for match in matches: # check all matches against blacklist
		if any(bl in match for bl in blacklist):
			pass
		else:
			links.insert(0,match)
		
	return links

def browse(urls):
	currURL = 1
	for url in urls:
		urlCount = len(urls)

		page = doRequest(url)  # hit current root URL
		links = getLinks(page) # extract links from page
		linkCount = len(links)
		
		depth=0
		while ( depth < clickDepth ):
			if debug:
				print "------------------------------------------------------"
				print "Blacklist: %s" % blacklist 
			# set the link count, which will change throughout the loop
			linkCount = len(links)
			if ( linkCount > 1): # make sure we have more than 1 link to use
			
				if debug:
					print "URL: %s / %s -- Depth: %s / %s" \
						% (currURL,urlCount,depth,clickDepth)
					print "Choosing random link from total: %s" % linkCount
					
				randomLink = random.randrange(0,linkCount - 1)
				
				if debug:
					print "Link chosen: %s of %s" % (randomLink,linkCount)
					
				clickLink = links[randomLink]
				
				try:
					# browse to random link on rootURL
					sub_page = doRequest(clickLink)
					checkLinkCount = len(getLinks(sub_page))

					# make sure we have more than 1 link to pick from 
					if ( checkLinkCount > 1 ):
						# extract links from the new page
						links = getLinks(sub_page)
					else:
						# else retry with current link list
						if debug:
							print "Not enough links found! Found: %s  -- " \
								"Going back up a level" % checkLinkCount
						blacklist.insert(0,clickLink)
						# remove the dead-end link from our list
						del links[randomLink]
				except:
					if debug:
						print "Exception on URL: %s  -- " \
							"removing from list and trying again!" % clickLink
					# I need to expand more on exception type for debugging
					blacklist.insert(0,clickLink)
					# remove the dead-end link from our list
					del links[randomLink] 
					pass
				# increment counter whether request was successful or not 
				# so that we don't end up in an infinite failed request loop
				depth+=1
			else:
				# we land here if we went down a path that dead-ends
				# could implement logic to simply restart at same root
				if debug:
					print "Hit a dead end...Moving to next Root URL"
				blacklist.insert(0,clickLink)
				depth = clickDepth 
			
		
		currURL+=1 # increase rootURL iteration
	if debug:
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
	print "Clicking %s links deep into %s different root URLs, " % (clickDepth,len(rootURLs))
	print "waiting between %s and %s seconds between requests. " % (minWait,maxWait)
	print ""
	print "This script will run indefinitely. Ctrl+C to stop."
	browse(rootURLs)
