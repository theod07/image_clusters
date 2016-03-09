import threading
import selenium.webdriver as webdriver
import numpy as np
from time import strftime
import time
import os
import random
from selenium.common.exceptions import NoSuchElementException
import urllib

def get_usernames(filename):
    '''
    INPUT: file of usernames, separated by newline
    OUTPUT: list of usernames
    '''
    with open(filename) as f:
        usernames = f.readlines()
    usernames = [name.split('\n')[0] for name in usernames if not name.startswith('#')]
    return set(usernames)


def get_userlinks(username, driver, sleeptime=1, down_scrolls=200):
    '''
    '''
    url = 'http://instagram.com/'+username
    driver.get(url)
    try:
        driver.find_element_by_link_text('LOAD MORE').click()
    except NoSuchElementException:
        print 'Sorry, this page isnt available: ', username,

    for i in xrange(down_scrolls):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleeptime*random.random())

    a_tags = driver.find_elements_by_tag_name('a')

    good_links, bad_links = [], []
    for tag in a_tags:
        if tag.get_attribute('class') == '_8mlbc _t5r8b':
            good_links.append(tag.get_attribute('href'))
        else:
            # print ("Unable find class='_8mlbc _t5r8b' for tag %s" % tag)
            bad_links.append(tag.get_attribute('href'))
    return good_links, bad_links

def write_file(name, items, description):
    try:
        os.mkdir('../data/'+name)
    except OSError:
        print 'Directory already exists: ', name

    fname = name+'_'+description+'.txt'
    f = open( ('../data/'+name+'/'+fname), 'w')
    for item in items:
        f.write(item + '\n')
    f.close()
    print strftime('%Y%m%d.%H:%M:%s'), ' items written to ', fname
    return

def scrape_links(username, driver, sleeptime, down_scrolls):
    good_links, bad_links = get_userlinks(username, driver, sleeptime=sleeptime, down_scrolls=down_scrolls)
    write_file(username, good_links, 'gooduserlinks')
    # write_file(username, bad_links, 'baduserlinks')
    return

def get_data_reactids(urls, driver):
    ''' Takes a list of urls for each image and returns a list of data-reactid items
    '''
    reactids = []
    yes_ovg3g = 0
    for url in urls:
        driver.get(url)
        tags = driver.find_elements_by_class_name('_ovg3g')

        if len(tags) > 0:
            yes_ovg3g += 1
        else:
            print 'No _ovg3g ', url

        for tag in tags:
            reactids.append(tag.get_attribute('data-reactid'))

    print ( 'Successfully found %s reactids among %s urls' %(yes_ovg3g, len(urls)) )
    return reactids

def reactid_to_srcurl(reactids):
    '''
    convert reactid strings to img source url strings
    '''
    src_urls = []
    for reactid in reactids:
        current = reactid.replace('=1','.').replace('=2',':')
        chop_l = current.split('http')[1]
        chopped = chop_l.split('.jpg')[0]
        src_urls.append('http'+chopped+'.jpg')
    return src_urls

def thread_get_userlinks(usernames, driver, num_threads=3, down_scrolls=200, sleeptime=2):
        while len(usernames) > 0:
            threads = []

            if len(usernames) >= num_threads:
                subset = [usernames.pop() for i in range(num_threads)]
            else:
                subset = [usernames.pop() for name in usernames]

            print 'subset: ', subset
            for name in subset:
                try:
                    os.mkdir('../data/'+name)
                    print strftime('%Y%m%d.%H:%M:%s'), ' Pulling up IG profile for ', name
                    t = threading.Thread(target=scrape_links, args=(name, driver,  sleeptime, down_scrolls,))
                    t.start()
                    print strftime('%Y%m%d.%H:%M:%s'), 'Started thread for ', name
                    threads.append(t)
                except OSError:
                    print strftime('%Y%m%d.%H:%M:%s'), ' directory already exists for',name

            for thread in threads: thread.join()
            print strftime('%Y%m%d.%H:%M:%s'), 'Joined threads for ', subset

            print strftime('%Y%m%d.%H:%M:%s'), '#### Users Remaining #### ', len(usernames)
        return

def download_file(url, username):
    filename = username+'_'+url.split('/')[-1]
    save_location = '../data/'+username+'/img/'
    try:
        os.mkdir(save_location)
    except OSError:
        print 'directory exists for ', username
    urllib.urlretrieve(url, save_location+filename)
    print 'downloaded ', save_location+filename
    return

if __name__ == '__main__':
    usernames = get_usernames('../data/most_popular.txt')
    num_threads = 3
    down_scrolls = 0
    sleeptime = 2
    driver = webdriver.Firefox()

    user = 'kcrw'
    glinks, blinks = get_userlinks(user, driver, sleeptime=sleeptime, down_scrolls=down_scrolls)
    reactids = get_data_reactids(glinks[:5], driver)
    src_urls = reactid_to_srcurl(reactids)

    for url in src_urls:
        download_file(url, user)
    driver.close()
