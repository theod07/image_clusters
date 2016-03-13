import selenium.webdriver as webdriver
import time
import random
from time import strftime
import os
from string import ascii_lowercase as alphabet
import threading

def get_users(filename):
    '''
    INPUT: file of users, separated by newline
    OUTPUT: list of users
    '''
    with open(filename, 'r') as f:
        users = f.readlines()
    users = [name.split('\n')[0] for name in users if not name.startswith('#')]
    return users

def get_data_reactids(urls, driver, sleeptime=2):
    '''
    Takes a list of urls for each image and returns a list of data-reactid items
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

        time.sleep(sleeptime*random.random())

    print ( 'Successfully found %s reactids among %s urls'
                                                    %(yes_ovg3g, len(urls)) )
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

def write_file(username, items, description):
    try:
        os.mkdir('../data/'+username)
    except OSError:
        print 'Directory already exists: ', username

        fname = username+'_'+description+'.txt'
        f = open( ('../data/'+username+'/'+fname), 'a')
        for item in items:
            f.write(item + '\n')
        f.close()
        print strftime('%Y%m%d.%H:%M:%s'), ' items written to ', fname
    return

def has_gooduserlinks_file(username):
    '''
    check whether a given user already has ***_gooduserlinks.txt file
    '''
    loc = '../data/'+username+'/'
    try:
        for item in os.listdir(loc):
            if item.endswith('gooduserlinks.txt'):
                return True
    except:
        print False
    return False

def has_src_url_file(user):
    '''
    return True if user already has src_url.txt file
    '''
    path = '../data/'
    if user not in os.listdir(path):
        return False

    path = '../data/'+user+'/'
    for file in os.listdir(path):
        if 'src_url' in file:
            return True
    return False


def get_gooduserlinks(username):
    loc = '../data/'+username+'/'
    fname = loc + username + '_gooduserlinks.txt'
    with open(fname, 'r') as f:
        lines = f.readlines()
    links = [line.split('\n')[0] for line in lines]
    return links

def get_src_urls(username, driver):
    '''
    create a file containing src_urls for given username
    '''
    if has_src_url_file(username):
        print '{} already has src_urls.txt file'.format(username)
        return

    if has_gooduserlinks_file(username):
        try:
            print 'getting gooduserlinks'
            gooduserlinks = get_gooduserlinks(username)
            print 'getting reactids'
            reactids = get_data_reactids(gooduserlinks, driver, sleeptime=.2)
            print 'getting src_urls'
            src_urls = reactid_to_srcurl(reactids)
            print 'writing to file'
            write_file(username, src_urls, 'src_urls')
            with open('../data/log_get_userlinks.txt', 'a') as f:
                f.write('Succeed get src_urls for '+username+ '\n')
        except:
            with open('../data/log_get_userlinks.txt', 'a') as f:
                f.write('Fail get src_urls for '+username+ '\n')

        print 'attempted username: ', username
    else:
        print 'No gooduserlinks file for ', username


def thread_get_src_urls(users, num_threads=3):
    print 'Threading get_src_urls for {}'.format(users)
    failed = []

    while len(users) > 0:
        threads = []

        if len(users) >= num_threads:
            subset = [users.pop() for i in range(num_threads)]
        else:
            subset = [users.pop() for user in users]

        for user in subset:
            try:
                print 'enter try statement'
                driver = webdriver.Firefox()
                print 'attempting thread for user {}'.format(user)
                t = threading.Thread(target=get_src_urls, args=(username, driver,))
                print 'thread created for user {}'.format(user)
                t.start()
                print strftime('%Y%m%d.%H:%M:%s'), 'Started thread get_src_urls({})'.format(user)
                threads.append(t)
                print 'thread appended to list for user {}'.format(user)
                driver.close()
            except:
                driver.close()
                failed.append(user)
                print strftime('%Y%m%d.%H:%M:%s'), ' Failed for {}'.format(user)
        for thread in threads: thread.join()

    print 'failed users: {}'.format(failed)
    print strftime('%Y%m%d.%H:%M:%s'), 'Joined threads for {}'.format(subset)

if __name__ == '__main__':

    # username = raw_input('Give me a username to go through:  ')
    # driver = webdriver.Firefox()
    # get_src_urls(username, driver)
    # driver.close()

    all_users = get_users('../data/most_popular.txt')
    letter = raw_input('give me a letter: ')
    users = [user for user in all_users if user.lower().startswith(letter)]
    driver = webdriver.Firefox()
    for user in users:
        get_src_urls(user, driver)
    driver.close()
