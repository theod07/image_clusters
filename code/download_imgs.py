import urllib
import threading
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import urllib2
import json

# url = 'https://scontent-iad3-1.cdninstagram.com/t51.2885-15/e35/12783439_227038377646495_165023836_n.jpg'
# title = 'test_image_'
# urllib.urlretrieve(url, filename='./'+title+'.jpg')

def connect_s3(key_path):
    with open(key_path, 'r') as f:
        creds = json.load(f)
        KEY = creds['AWSAccessKeyId']
        SECRET_KEY = creds['AWSSecretKey']
    conn = S3Connection(KEY, SECRET_KEY)
    return conn

def has_src_url_file(username):
    '''
    return True if username already has src_url.txt file
    '''
    path = '../data/'
    if username not in os.listdir(path):
        print 'Cannot find dir for {}'.format(username)
        return False

    path = '../data/{}/'.format(username)
    for file in os.listdir(path):
        if 'src_url' in file:
            return True
    print 'No src_urls.txt file for user {}'.format(username)
    return False

def read_src_urls(username):
    '''
    check whether user has src_url.txt file

    '''
    user_path = '../data/{}/'.format(username)
    fname = '{}{}_src_urls.txt'.format(user_path, username)
    with open(fname, 'r') as f:
        lines = f.readlines()
    urls = [l.split('\n')[0] for l in lines]
    return urls

def local_save(url, save_path):
    fname = url.split('/')[-1]
    try:
        os.mkdir(save_path)
        urllib.urlretrieve(url, save_path+fname)
        print 'file saved to : ', save_path+fname
    except OSError:
        urllib.urlretrieve(url, save_path+fname)
        print 'file saved to : ', save_path+fname
    return

def s3_save(username, url, bucket):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    title= url.split('/')[-1]
    fname = '{}_{}'.format(username, title)

    k = Key(bucket)
    k.name = fname
    info = k.set_contents_from_string(response.read(), {'Content-Type' : response.info().gettype()})
    return info



if __name__ == '__main__':
    '''
    read in src_urls from file
    connect to s3
    for each url:
        download file
    '''

    # conn = S3Connection(MYAWSID, MYAWSSECRET)

    keypath = '/Users/wonder/rootkey.json'
    conn = connect_s3(keypath)
    bucket = conn.get_bucket('ig_image_clusters')

    username = raw_input('give me a username: ')
    while has_src_url_file(username):
        src_urls = read_src_urls(username)

        for url in src_urls:
            # download_file_local(url, save_path)
            # print 'url: {}'.format(url)
            s3_save(username, url, bucket)

    conn.close()
