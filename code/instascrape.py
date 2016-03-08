import threading
import selenium.webdriver as webdriver
import numpy as np
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
        print 'Sorry, this page isnt available: ', user

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
    f = open( ('../data/'+fname), 'w')
    for item in items:
        f.write(item + '\n')
    f.close()
    print 'items written to ', fname
    return

def scrape_func(username, sleeptime, down_scrolls):
    good_links, bad_links = get_userlinks(username, sleeptime=sleeptime, down_scrolls=down_scrolls)
    write_file(username, good_links, 'gooduserlinks')
    write_file(username, bad_links, 'baduserlinks')
    return

def find_replace(url):
    '''
    =1 --> period
    =2 --> colon
    '''

    pass

if __name__ == '__main__':
    usernames = get_usernames('../data/most_popular.txt')
    for name in usernames:
        try:
            os.mkdir('../data/'+name)
            print 'Pulling up IG profile for ', name
            scrape_func(name, sleeptime=1.2, down_scrolls=300)

        except OSError:
            print 'directory already exists for',name

    # i = 0
    # while
    #     threads = []
    #     for name in usernames[:10]:
    #         t = threading.Thread(target=scrape_threaded, args=(name, sleeptime=1, down_scrolls=2))
    #         threads.append(t)
    #
    #     for thread in threads: thread.start()
    #     for thread in threads: thread.join()
