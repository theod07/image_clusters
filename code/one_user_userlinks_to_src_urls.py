import selenium.webdriver as webdriver
import time
import random
from time import strftime
import os

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

def has_userlinks_file(username):
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

if __name__ == '__main__':
    '''
    create a file containing src_urls for given usernames
    '''
    # with open('../data/EXAMPLE_instagramtop50/EXAMPLE_instagramtop50_gooduserlinks.txt', 'r') as f:
    #     userlinks = f.readlines()

    username = raw_input('Give me a username to go through:  ')

    driver = webdriver.Firefox()

    try:
        reactids = get_data_reactids(userlinks, driver, sleeptime=.2)
        src_urls = reactid_to_srcurl(reactids)
        write_file('EXAMPLE_instagramtop50', src_urls, 'src_urls')
        with open('../data/log_get_userlinks.txt', 'a') as f:
            f.write('Succeed get src_urls for '+username+ '\n')
        driver.close()
    except:
        with open('../data/log_get_userlinks.txt', 'a') as f:
            f.write('Fail get src_urls for '+username+ '\n')
        driver.close()

    print 'attempted username: ', username
