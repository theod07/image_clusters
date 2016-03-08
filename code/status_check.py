
def read_log(fname):
    '''
    Read in a log file and return the result of each username.
    INPUT: fname of log
    OUTPUT: successful users scraped
            unsuccessful users scraped
            did_not_try directory for user existed previously
            other lines not caught
    '''
    success = []
    unsuccess = []
    did_not_try = []
    other = []

    f = open(fname, 'r')
    for line in f.readlines():
        if line.startswith('items written to'):
            success.append(line.split()[-1].split('_')[0])
        elif line.startswith('Sorry, this page isnt available'):
            unsuccess.append(line.split()[-1])
        elif line.startswith('directory already exists'):
            did_not_try.append(line.split()[-1])
        else:
            other.append(line)

    f.close()
    return success, unsuccess, did_not_try, other
