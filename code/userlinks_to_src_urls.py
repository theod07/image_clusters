import selenium.webdriver as webdriver
import time
import random
from time import strftime
import os
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

def get_data_reactids(user, urls, driver, sleeptime=2):
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

def userlinks_to_src_urls(user):
    batchsize = 25
    print 'Inside userlinks_to_src_urls', user
    fn_read = '../data/'+user+'/'+user+'_gooduserlinks.txt'
    f = open('../data/'+user+'/'+user+'_src_urls.txt', 'a')
    try:
        userlinks = read_vals(fn_read)
        userlinks = [l.split('\n')[0] for l in userlinks]
        # userlinks = [l.split('\n')[0] for l in userlinks]
        driver = webdriver.Firefox()

        while len(userlinks) > 0:
            if len(userlinks) >= batchsize:
                batch = [userlinks.pop() for i in xrange(batchsize)]
            else:
                batch = [userlinks.pop() for i in userlinks]
            print 'len(batch): ', len(batch)
            print 'len(userlinks): ', len(userlinks)
            reactids = get_data_reactids(batch, driver)
            src_urls = reactid_to_srcurl(reactids)

            [f.write(url+'\n') for url in src_urls]
            # write_file(user, src_urls, 'src_urls')
    except IOError:
        print 'No file: ', fn_read
    f.close()
    driver.close()

def write_file(user, items, description):
    try:
        os.mkdir('../data/'+user)
    except OSError:
        print 'Directory already exists: ', user

        fname = user+'_'+description+'.txt'
        f = open( ('../data/'+user+'/'+fname), 'a')
        for item in items:
            f.write(item + '\n')
            f.close()
            print strftime('%Y%m%d.%H:%M:%s'), ' items written to ', fname
            return

def read_vals(fname):
    with open(fname, 'r') as f:
        vals = f.readlines()
        return vals

def thread_get_src_urls(users, num_threads=3, sleeptime=3):
    inv_users = []

    while len(users) > 0:
        threads = []

        if len(users) >= num_threads:
            subset = [users.pop() for i in range(num_threads)]
        else:
            subset = [users.pop() for user in users]

        print 'subset: ', subset

        for name in subset:
            if has_src_url_file(name):
                try:
                    t = threading.Thread(target=userlinks_to_src_urls, args=(name,))
                    t.start()
                    print strftime('%Y%m%d.%H:%M:%s'), 'Started thread for ', name
                    threads.append(t)
                except:
                    inv_users.append(name)
                    print strftime('%Y%m%d.%H:%M:%s'), ' Problem with ', name

        print '### threads: ', threads
        for thread in threads: thread.join()
        print strftime('%Y%m%d.%H:%M:%s'), 'Joined threads for ', subset

        print strftime('%Y%m%d.%H:%M:%s'), '#### Users Remaining #### ', len(users)
    return

def has_src_url_file(user):
    '''
    return True if user already has src_url.txt file
    '''
    path = '../data/'
    if user not in os.listdir(path):
        return False

    path = '../data/'+user+'/'
    if 'src_url' in os.listdir(path):
        return False
    return True

if __name__ == '__main__':
    num_threads = 3
    users = sorted(get_users('../data/most_popular.txt'))

    while len(users) > 0:
        if len(users) > 0:
            subset = [users.pop() for i in xrange(num_threads)]
        else:
            subset = [users.pop() for user in users]

        for user in users:
            if has_src_url_file(user):
                # skip if user already has src_url.txt file
                print '{} {} already has src_url.txt file'.format(strftime('%Y%m%d.%H:%M:%s'), user)
            else:

    # sleeptime = num_threads + 3
    # while len(users) > 0:
    #     if len(users) >= num_threads:
    #         batch_users = [users.pop() for i in range(num_threads)]
    #     else:
    #         batch_users = [users.pop() for i in users]
    #
    #     thread_get_src_urls(batch_users, num_threads=num_threads, sleeptime=sleeptime)
