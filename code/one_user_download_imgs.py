import urllib
import threading
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import urllib2
import json

# request = urllib2.Request('http://www.google.com/images/srpr/logo3w.png')
# response = urllib2.urlopen(request)
#
# conn = S3Connection(MYAWSID, MYAWSSECRET)
# bucket = conn.create_bucket('MyBucket')
# k = Key(bucket)
# k.name = "logo3w"
# k.set_contents_from_string(response.read(), {'Content-Type' : response.info().gettype()
#
#
#
# url = 'https://scontent-iad3-1.cdninstagram.com/t51.2885-15/e35/12783439_227038377646495_165023836_n.jpg'
# title = 'test_image_'
# urllib.urlretrieve(url, filename='./'+title+'.jpg')

def connect_s3():
    with open('/Users/wonder/rootkey.json', 'r') as f:
        creds = json.load(f)
        KEY = creds['AWSAccessKeyId']
        SECRET_KEY = creds['AWSSecretKey']
    conn = S3Connection(KEY, SECRET_KEY)
    return conn

def download_file_local(url, save_dir):
    filename = url.split('/')[-1]
    try:
        os.mkdir(save_dir)
        urllib.urlretrieve(url, save_dir+filename)
        print 'file saved to : ', save_dir+filename
    except OSError:
        urllib.urlretrieve(url, save_dir+filename)
        print 'file saved to : ', save_dir+filename
    return

def download_file_s3():
    pass

def read_src_urls(username):
    pass


if __name__ == '__main__':

    '''
    read in src_urls from file
    connect to s3
    for each url:
        download file
    '''
    username = 'EXAMPLE_taylorswift'
    user_dir = '../data/'+username
    save_dir = user_dir + '/img/'
    with open(user_dir+'/'+username+'_src_urls.txt', 'r') as f:
        lines = f.readlines()
        src_urls = [l.split('\n')[0] for l in lines]

    for url in src_urls:
        download_file_local(url, save_dir)

    # conn = connect_s3()
