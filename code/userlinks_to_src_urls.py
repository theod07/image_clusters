
def get_usernames(filename):
    '''
    INPUT: file of usernames, separated by newline
    OUTPUT: list of usernames
    '''
    with open(filename) as f:
        usernames = f.readlines()
    usernames = [name.split('\n')[0] for name in usernames if not name.startswith('#')]
    return set(usernames)

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

def main():
    for user in users:
    pass


if __name__ == '__main__':
    usernames = get_usernames('../data/most_popular.txt')
    main()
