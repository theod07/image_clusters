import threading
import selenium.webdriver as webdriver
import numpy as np
from time import strftime
import time
import os
import random
from selenium.common.exceptions import NoSuchElementException


def get_usernames(filename):
    '''
    INPUT: file of usernames, separated by newline
    OUTPUT: list of usernames
    '''
    with open(filename) as f:
        usernames = f.readlines()
    usernames = [name.split('\n')[0] for name in usernames if not name.startswith('#')]
    return list(set(usernames))


def get_userlinks(username, sleeptime=1, down_scrolls=200):
    '''
    '''
    url = 'http://instagram.com/'+username
    driver = webdriver.Firefox()
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
    driver.close()
    return good_links, bad_links

def write_file(name, items, description):
    fname = name+'_'+description+'.txt'
    f = open( ('../data/'+name+'/'+fname), 'w')
    for item in items:
        f.write(item + '\n')
    f.close()
    print strftime('%Y%m%d.%H:%M:%s'), ' items written to ', fname
    return

def scrape_links(username, sleeptime, down_scrolls):
    good_links, bad_links = get_userlinks(username, sleeptime=sleeptime, down_scrolls=down_scrolls)
    write_file(username, good_links, 'gooduserlinks')
    # write_file(username, bad_links, 'baduserlinks')
    return

def get_data_reactids(urls):
    ''' Takes a list of urls for each image and returns a list of data-reactid items
    '''
    reactids = []
    has_ovg3g = 0
    for url in urls:
        driver = webdriver.Firefox()
        driver.get(url)
        tags = driver.find_elements_by_class_name('_ovg3g')

        if len(tags) > 0:
            yes_ovg3g += 1
        else:
            print 'No _ovg3g ', link

        for tag in tags:
            reactids.append(tag.get_attribute('data-reactid'))

        driver.close()
        print ( 'Successfully found %s reactids among %s urls' %(has_ovg3g, len(urls)) )
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

if __name__ == '__main__':
    usernames = get_usernames('../data/most_popular.txt')
    num_threads = 3
    down_scrolls = 200
    pause = 2

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
                t = threading.Thread(target=scrape_links, args=(name, pause, down_scrolls,))
                t.start()
                print strftime('%Y%m%d.%H:%M:%s'), 'Started thread for ', name
                threads.append(t)
            except OSError:
                print strftime('%Y%m%d.%H:%M:%s'), ' directory already exists for',name

        for thread in threads: thread.join()
        print strftime('%Y%m%d.%H:%M:%s'), 'Joined threads for ', subset

        print strftime('%Y%m%d.%H:%M:%s'), '#### Users Remaining #### ', len(usernames)
