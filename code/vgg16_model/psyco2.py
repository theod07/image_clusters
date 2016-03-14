import psycopg2 as pg2

def vec_to_str(vec):
    '''
    return string format of vector to insert into postgres
    '''
    strs = ['{:.30f}'.format(v) for v in vec]
    output = "'{" + ','.join(strs) + "}'"
    return output

def add_prediction_to_db(url, pred_str):
    query = '''INSERT INTO predictions (src_url, prediction) values ({}, {});'''.format(url, pred_str)
    cursor.execute(query)
    return

if __name__ == '__main__':
    # conn = pg2.connect(user='postgres', password='admin', dbname='image_clusters')
    # c = conn.cursor()
    # c.execute('select * from predictions;')
    # query = '''INSERT INTO predictions (src_url, prediction) values ({}, {});'''
    # query1 = query.format("'a'", vec_to_str(probs[0][0][:5]))
    # query2 = query.format("'b'", vec_to_str(probs[1][0][:5]))
    # c.execute(query1)
    # c.execute('select * from predictions;')
    # c.execute(query2)
    # c.execute('select * from predictions;')
