import download_imgs as dl
# from download_imgs import has_src_url_file
# from download_imgs import read_src_urls
import database as db
# from database import vec_to_str
# from database import insert_prediction
from vgg16_model import model as nn




if __name__ == '__main__':
    # keypath = '/Users/wonder/rootkey.json'
    keypath = '/home/ubuntu/.rootkey.json'

    s3_conn = dl.connect_s3(keypath)
    bucket = s3_conn.get_bucket('ig_image_clusters')

    pg_conn = pg2.connect(user='postgres', password='admin', dbname='image_clusters')
    pg_cursor = pg_conn.cursor()

    username = raw_input('give me a username: ')

    while dl.has_src_url_file(username):
        src_urls = dl.read_src_urls(username)

        for url in src_urls:
            dl.s3_save(username, url, bucket)
            pred = nn.predict(url)[0]
            pred_str = db.vec_to_str(pred)
            db.insert_prediction(url, pred_str, pg_cursor)

    s3_conn.close()
