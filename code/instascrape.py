import threading
import selenium.webdriver as webdriver
import numpy as np
from time import strftime
import time
import os
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
        time.sleep(sleeptime)

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

def scrape_func(username, sleeptime, down_scrolls):
    good_links, bad_links = get_userlinks(username, sleeptime=sleeptime, down_scrolls=down_scrolls)
    write_file(username, good_links, 'gooduserlinks')
    # write_file(username, bad_links, 'baduserlinks')
    return

def find_replace(url):
    '''
    =1 --> period
    =2 --> colon
    '''

    pass

if __name__ == '__main__':
    print 'looks like the program entered MAIN correctly..'
    usernames = get_usernames('../data/most_popular.txt')
    num_threads = 2
    print 'len(usernames): ', len(usernames)

    while len(usernames) > 450:
        threads = []
        subset = [usernames.pop() for i in range(num_threads)]
        print 'len(usernames): ', len(usernames)
        print 'subset: ', subset
        for name in subset:
            try:
                os.mkdir('../data/'+name)
                print strftime('%Y%m%d.%H:%M:%s'), ' Pulling up IG profile for ', name
                t = threading.Thread(target=scrape_func, args=(name, 2, 10,))
                t.start()
                print 'Started thread for ', name
                threads.append(t)
            except OSError:
                print strftime('%Y%m%d.%H:%M:%s'), ' directory already exists for',name

        for thread in threads: thread.join()
        print 'Joined threads for ', subset

    # i = 0
    # while
    #     threads = []
    #     for name in usernames[:10]:
    #         t = threading.Thread(target=scrape_threaded, args=(name, sleeptime=1, down_scrolls=2))
    #         threads.append(t)
    #
    #     for thread in threads: thread.start()
    #     for thread in threads: thread.join()
