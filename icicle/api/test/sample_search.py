import sys
import urllib2
from base64 import b64encode
from pprint import pprint

# For testing the hosted API via the command line.
#
# $> python sample_search.py "search this string"
if __name__ == "__main__":
    api_url = 'https://9u56icss4c.execute-api.us-west-2.amazonaws.com/dev'
    keyword = b64encode(sys.argv[1])
    content = urllib2.urlopen("{0}/search/{1}".format(api_url, keyword)).read()
    pprint(content)
