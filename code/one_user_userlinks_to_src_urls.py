
def get_data_reactids(username, urls, driver, sleeptime=2):
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



if __name__ == '__main__':
    '''
    create a file containing src_urls for EXAMPLE_taylorswift
    '''
    with open('../data/EXAMPLE_taylorswift/EXAMPLE_taylorswift_gooduserlinks.txt', 'r') as f:
        userlinks = f.readlines()

    driver = webdriver.Firefox()
    reactids = get_data_reactids(userlinks, driver, sleeptime=1.5)
    src_urls = reactid_to_srcurl(reactids)
    write_file('EXAMPLE_taylorswift', src_urls, 'src_urls')
