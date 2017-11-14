import requests
import sys

if sys.version > '3':
    import urllib.request as urllib2  
else: 
    import urllib2

wx_gw = 'https://way.jd.com/'

def wx_get_req(company, method, params):
    request_url = wx_gw + company + "/" + method
    return requests.get(request_url, params)

def wx_post_req(company, method, params, img=None):
    request_url = wx_gw + company + "/" + method
    if img :
        ret = file_get_contents(img)
        return requests.post(request_url, params=params, data=ret)
    else :
        return requests.post(request_url, params)

#img to str
def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib2.urlopen(filename).read()
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close( )
