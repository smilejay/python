#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 20, 2013
@summary: geography info about an IP address
@author: Jay <smilejay.com>
'''

import json, urllib2
from HTMLParser import HTMLParser
import re

class location_freegeoip():
    '''
    build the mapping of the ip address and its location.
    the geo info is from <freegeoip.net>
    '''
    
    def __init__(self, ip):
        '''
        Constructor of location_freegeoip class
        '''
        self.ip = ip
        self.api_format = 'json'
        self.api_url = 'http://freegeoip.net/%s/%s' % (self.api_format, self.ip)
    
    def get_geoinfo(self):
        """ get the geo info from the remote API.
        
            return a dict about the location.
        """
        urlobj = urllib2.urlopen(self.api_url)
        data = urlobj.read()
        datadict = json.loads(data, encoding='utf-8')
#        print datadict
        return datadict
    
    def get_country(self):
        key = 'country_name'
        datadict = self.get_geoinfo()
        return datadict[key] 
    
    def get_region(self):
        key = 'region_name'
        datadict = self.get_geoinfo()
        return datadict[key]
     
    def get_city(self):
        key = 'city'
        datadict = self.get_geoinfo()
        return datadict[key]

class location_taobao():
    '''
    build the mapping of the ip address and its location
    the geo info is from Taobao
    e.g. http://ip.taobao.com/service/getIpInfo.php?ip=112.111.184.63
    The getIpInfo API from Taobao returns a JSON object.
    '''
    def __init__(self, ip):
        self.ip = ip
        self.api_url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % self.ip
        
    def get_geoinfo(self):
        """ get the geo info from the remote API.
        
            return a dict about the location.
        """
        urlobj = urllib2.urlopen(self.api_url)
        data = urlobj.read()
        datadict = json.loads(data, encoding='utf-8')
#        print datadict
        return datadict['data']
    
    def get_country(self):
        key = u'country'
        datadict = self.get_geoinfo()
        return datadict[key]
    
    def get_region(self):
        key = 'region'
        datadict = self.get_geoinfo()
        return datadict[key]
     
    def get_city(self):
        key = 'city'
        datadict = self.get_geoinfo()
        return datadict[key]

    def get_isp(self):
        key = 'isp'
        datadict = self.get_geoinfo()
        return datadict[key]

class location_qq():
    '''
    build the mapping of the ip address and its location.
    the geo info is from Tencent.
    Note: the content of the Tencent's API return page is encoded by 'gb2312'.
    e.g. http://ip.qq.com/cgi-bin/searchip?searchip1=112.111.184.64
    '''
    def __init__(self, ip):
        '''
        Construction of location_ipdotcn class.
        '''
        self.ip = ip
        self.api_url = 'http://ip.qq.com/cgi-bin/searchip?searchip1=%s' % ip
    
    def get_geoinfo(self):
        urlobj = urllib2.urlopen(self.api_url)
        data = urlobj.read().decode('gb2312').encode('utf8')
        pattern = re.compile(r'该IP所在地为：<span>(.+)</span>')
        m = re.search(pattern, data)
        if m != None: 
            return m.group(1).split('&nbsp;')
        else:
            return None
        
    def get_region(self):
        print self.get_geoinfo()[0]
        return self.get_geoinfo()[0]
    
    def get_isp(self):
        print self.get_geoinfo()[1]
        return self.get_geoinfo()[1]

# FIXME: this class can't work correctly yet.
class location_ipdotcn():
    '''
    build the mapping of the ip address and its location.
    the geo info is from www.ip.cn
    '''
    def __init__(self, ip):
        '''
        Construction of location_ipdotcn class.
        '''
        self.ip = ip
        self.api_url = 'http://www.ip.cn/%s' % ip
        print self.api_url
    
    def get_geoinfo(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0'
        myheaders = {'User-Agent' : user_agent}
        req = urllib2.Request(self.api_url, headers=myheaders)
        urlobj = urllib2.urlopen(req)
        data = urlobj.read()
        print data
        myparser = MyHTMLParser()
        myparser.feed(data)

class MyHTMLParser(HTMLParser):
    '''
    build the subclass of HTMLParser.
    '''
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "     attr:", attr
    def handle_endtag(self, tag='span'):
        print "End tag  :", tag
    def handle_data(self, data):
        print "Data     :", data
    def handle_comment(self, data):
        print "Comment  :", data
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data
    
if __name__ == '__main__':
    ip = '110.84.0.129'
#    iploc = location_taobao(ip)
#    print iploc.get_geoinfo()
#    print iploc.get_country()
#    print iploc.get_region()
#    print iploc.get_city()
#    print iploc.get_isp()
    iploc = location_qq(ip)
#    iploc.get_geoinfo()
    iploc.get_region()
    iploc.get_isp()