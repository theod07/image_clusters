import download_imgs as dl
# from download_imgs import has_src_url_file
# from download_imgs import get_src_urls
import database as db
# from database import vec_to_str
# from database import insert_prediction
from vgg16_model import model as nn
import psycopg2 as pg2




if __name__ == '__main__':
    # keypath = '/Users/wonder/rootkey.json'
    keypath = '/home/ubuntu/.rootkey.json'

    s3_conn = dl.connect_s3(keypath)
    bucket = s3_conn.get_bucket('ig_image_clusters')

    pg_conn = pg2.connect(user='postgres', password='admin', dbname='image_clusters')
    pg_cursor = pg_conn.cursor()

    # username = raw_input('give me a username: ')
    # 'year'
    usernames = ['oceana', 'paolatonight', 'patricknorton']

    for username in usernames:
        while dl.has_src_url_file(username):
            shortcodes = dl.get_shortcodes(username)
            src_urls = dl.get_src_urls(username)


            for (code,url) in zip(shortcodes, src_urls):
                dl.s3_save(username, url, bucket)
                pred = nn.predict(url)[0]
                pred_str = db.vec_to_str(pred)
                db.insert_prediction(username, code, url, pred_str, pg_conn)

    s3_conn.close()
