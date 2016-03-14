import psycopg2 as pg2
import vgg16_model.model

def vec_to_str(vec):
    '''
    return string format of vector to insert into postgres
    '''
    strs = ['{:.30f}'.format(v) for v in vec]
    output = "{" + ', '.join(strs) + "}"
    return output

def insert_prediction(url, pred_str):
    query = '''INSERT INTO predictions (src_url, prediction) values ('{}', '{}' );'''.format(url, pred_str)
    # c.execute('''insert into test_table (src_url, prediction) values ('aa', {});'''.format(v1))
    c.execute(query)
    conn.commit()
    return

if __name__ == '__main__':
    conn = pg2.connect(user='postgres', password='admin', dbname='image_clusters')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM predictions;')
    print ('SELECT COUNT()*) FROM predictions;')
    c.fetchall()
    # query = '''INSERT INTO predictions (src_url, prediction) values ({}, {});'''
    # query1 = query.format("'a'", vec_to_str(probs[0][0][:5]))
    # query2 = query.format("'b'", vec_to_str(probs[1][0][:5]))
    # c.execute(query1)
    # c.execute('select * from predictions;')
    # c.execute(query2)
    # c.execute('select * from predictions;')


    with open('../../data/EXAMPLE_taylorswift/EXAMPLE_taylorswift_src_urls.txt', 'r') as f:
        lines = f.readlines()
        image_urls = [line.split('\n')[0] for line in lines]

    sample_size = 2
    urls = image_urls[:sample_size]
    while len(urls) > 0:
        url = urls.pop()
        print 'url: {}'.format(url)
        pred = model.predict(url)[0]
        print 'type(pred): ', type(pred)
        print
        pred_str = vec_to_str(pred)
        insert_prediction(url, pred_str)

    c.execute('select * from predictions;')
    c.fetchall()
    c.close()
    conn.close()
