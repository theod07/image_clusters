import pandas as pd
import numpy as np
import cPickle
import download_imgs as dl
import random
import os
from time import strftime
from vgg16_model import model as nn
import time

def rand_samp(items, k=100):
    if len(items) <= k:
        return items
    else:
        return random.sample(items, k)

def has_predictions_pkl(user):
    fname = '{}_predictions.pkl'.format(user)
    if fname in os.listdir('../pickles/'.format(user)):
        return True
    return False

def load_pkl(user):
    fname = '../pickles/{}_predictions.pkl'.format(user)
    df = pd.read_pickle(fname)
    print 'columns in df for {}: {}'.format(user, df.columns)
    # desired_cols = set(['username', 'shortcode', 'src_url', 'prediction'])
    # cur_cols = set(df.columns)
    # new_cols = desired_cols - cur_cols
    # while new_cols:
    #     df['{}'.format(new_cols.pop())] = 'null'
    return df


if __name__ == '__main__':

    # users = ['year', 'oceana', 'paolatonight', 'patricknorton']
    # users = ['jamieoliver', 'solar', 'trey5', 'worthwhilestyle', 'toppeopleworld', 'nycmayorsoffice', 'jessicaalba', 'toms', 'walaad', 'starbucks', 'warbyparker', 'theultimateclub', 'victoriassecret', 'jeremymcgrath2', 'julian_wilson', 'wired', 'taylorswift', 'skinart_mag', 'theroxy', 'twheat', 'laurenconrad', 'letthelordbewithyou', 'nickkristof']

 #    users = ['0y0m',
 # '10terra',
 # '1d.legendary.updates',
 # '1direct_news',
 # '1raqen',
 # '433',
 # '49ers',
 # '5onedirection',
 # '9gag',
 # 'ASOS',
 # 'EXAMPLE_instagramtop50',
 # 'EXAMPLE_taylorswift',
 # 'GAP',
 # '_samie_krasivie_',
 # '_voguevariety',
 # '_wcwson',
 # 'aceofspaceskingz',
 # 'adidas',
 # 'adidasfootball',
 # 'adidasoriginals',
 # 'alexsydneymagic',
 # 'aliciakeys',
 # 'allpaparazzi',
 # 'alukoyanov',
 # 'alwefaq',
 # 'amazing_pretty',
 # 'amberrose',
 # 'andersoncooper',
 # 'andresiniesta8',
 # 'animestagram',
 # 'anitta',
 # 'aol',
 # 'arab.iq',
 # 'arianagrande',
 # 'arishapiro',
 # 'artem_klyushin',
 # 'ashleyrparker',
 # 'avantiksco',
 # 'ayutingting92',
 # 'badgalriri',
 # 'bahrain_gallery',
 # 'bahrainstore',
 # 'balleralert',
 # 'barackobama',
 # 'barbershopconnect',
 # 'barcelonacitizen',
 # 'beautifulworldgroup',
 # 'beauty_edit_max',
 # 'bellathorne',
 # 'benandjerrys',
 # 'bergdorfs',
 # 'beybleedblue',
 # 'beyonce',
 # 'bigfeetsneaks',
 # 'bmdc27',
 # 'bobbyfresh',
 # 'boniver',
 # 'bonobos',
 # 'bortnikovrussia',
 # 'bowerswilkins',
 # 'brianstelter',
 # 'brooklynbowl',
 # 'brumarquezine',
 # 'brutalcactus',
 # 'buffalosabres',
 # 'burberry',
 # 'buyph',
 # 'cafe.of.paris',
 # 'caiocastro',
 # 'camerondallas',
 # 'caradelevigne',
 # 'carmeloanthony',
 # 'celtics',
 # 'champagnepapi',
 # 'chanelofficial',
 # 'channingtatum',
 # 'charitywater',
 # 'charlesdharapak',
 # 'chicagobulls',
 # 'chow',
 # 'chrisbrownofficial',
 # 'ciara',
 # 'cintageshop',
 # 'cirquedusoleil',
 # 'clint_dempsey',
 # 'cnnireport',
 # 'codysimpson',
 # 'convergence',
 # 'converse',
 # 'corybooker',
 # 'crazyhumor',
 # 'cristiano',
 # 'cultofmac',
 # 'curvaceousboutique',
 # 'cute1dfacts',
 # 'dallasmavs',
 # 'danbilzerian',
 # 'danecook',
 # 'daradaily',
 # 'darenta.ru',
 # 'davidbeckham',
 # 'davidluiz_4',
 # 'ddlovato',
 # 'deftonesband',
 # 'del_records_oficial',
 # 'dogfishbeer',
 # 'donlemoncnn',
 # 'donnakarandkny',
 # 'dress_varietyii',
 # 'dudubarina',
 # 'dunkindonuts',
 # 'dwyanewade',
 # 'ebaybahrain',
 # 'efrboy',
 # 'eggsformylegs',
 # 'elliegoulding',
 # 'elnuevodiariord',
 # 'emil_valentino',
 # 'erinandrews',
 # 'exopassion',
 # 'eyemediaa',
 # 'faceb008',
 # 'facebo08',
 # 'fashion_creative_love',
 # 'fashionbeautydisplay',
 # 'fashionchurch',
 # 'fashiontimeig',
 # 'favoritmusic',
 # 'fcbarcelona',
 # 'fcbnews1',
 # 'feedprojects',
 # 'ferggotti',
 # 'fitness_elites',
 # 'floydmayweather',
 # 'fogasa',
 # 'foodzie',
 # 'foofighters',
 # 'forever21',
 # 'fotogasm',
 # 'freedom_clothes',
 # 'frostingprince',
 # 'ft0ppz',
 # 'funsubstance',
 # 'futbolsport',
 # 'gandjfurches',
 # 'garethbale11',
 # 'gemibears',
 # 'generalelectric',
 # 'giftbuddy',
 # 'giggstage',
 # 'gigihadid',
 # 'girlscar',
 # 'gizzyboyy',
 # 'glamherous',
 # 'golddigginaccessories',
 # 'google_3qi',
 # 'gopro',
 # 'gothiphop',
 # 'gradient',
 # 'gucci',
 # 'gymclassheroes',
 # 'hangarang',
 # 'harajsa',
 # 'harrystyles',
 # 'highlinenyc',


    users = ['highonlifeco',
 'hlween.online',
 'hm',
 'hoodnews',
 'howulivinjpiven',
 'howuseeit',
 'hudabeauty',
 'i_queens',
 'iamzlatanibrahimovic',
 'ideal',
 'ig_fitsporation',
 'igsg',
 'igtoppicture',
 'iimpulsive',
 'iloveustyles',
 'ilya_sinus',
 'imchasingdreamz',
 'independent',
 'indonesia_olshop',
 'indotravellers.co',
 'instagram',
 'instagrambrasil',
 'instagramtop50',
 'instahaiku',
 'internetpoet',
 'iq.instgram',
 'iraq.al_70ob',
 'iraqeen',
 'iraqeen_handsom',
 'iraqi_friends',
 'iraqis_coffee',
 'iraqzz',
 'itsashbenzo',
 'ivetesangalo',
 'ivmikspb',
 'izdato_eng',
 'izykloset',
 'jamesrodriguez10',
 'jaybling',
 'jennydeluxe',
 'jimmiejohnson',
 'jimmyfallon',
 'jlo',
 'johnkingcnn',
 'justinbieber',
 'justintimberlake',
 'k_chugunkin',
 'kaka',
 'karaswisher',
 'karimbenzema',
 'katespadeny',
 'katyperry',
 'kazabby',
 'kcchiefs',
 'kcrw',
 'keepsy',
 'kekospobkk',
 'kellyslater',
 'kendalljenner',
 'kevinhart4real',
 'kevinjonas',
 'keysik',
 'khaliduk32',
 'khloekardashian',
 'kicks4sale',
 'kidfella',
 'kimkardashian',
 'kingjames',
 'kissup_boutique',
 'kokoulin',
 'kourtneykardash',
 'kreayshawn',
 'krisjenner',
 'kuntseva_a',
 'kyliejenner',
 'ladygaga',
 'lakers',
 'larrysgumdrop',
 'laudyacynthiabella',
 'leomessi',
 'letsloveonedirection',
 'levisbrasil',
 'lewishamilton',
 'like_3raqi',
 'linecook',
 'linkinpark',
 'livepainter',
 'lmao.clipss',
 'lootone_japan',
 'louisvuitton',
 'lucyhale',
 'luissuarez9',
 'makegirlz',
 'maluma',
 'manchesterunited',
 'manrepeller',
 'mansour_mall',
 'marcelotwelve',
 'marcjacobsintl',
 'marinaruybarbosa',
 'markhoppus',
 'markusprell',
 'marshanskiy',
 'matthewjennings',
 'mbiaggi',
 'mchammer',
 'meetthepress',
 'mercihouse',
 'mexicotravel',
 'mfj57',
 'miamiheat',
 'mike_tyson',
 'miketyson',
 'mileycyrus',
 'milwaukeebucks',
 'mistercap',
 'mittromney',
 'mobeye_vision',
 'modelisy',
 'moriderisa',
 'most_popular.txt',
 'mtv',
 'myhusbandtrue',
 'nailsvideos',
 'nancyloo',
 'nasa',
 'nasagoddard',
 'natgeo',
 'nationalpost',
 'nba',
 'nbcnews',
 'negin_mirsalehi',
 'netofernandez7',
 'new_brand1',
 'newtgingrich',
 'newyork_show',
 'neymarjr',
 'ngakakkocak',
 'nhl',
 'nhlbruins',
 'niallhoran',
 'nickbilton',
 'nickiminaj',
 'nickster2k',
 'nike',
 'nikefootball',
 'niksidorkin',
 'nonghairstylist3245',
 'norahodonnell',
 'npr',
 'nyknicks',
 'nylonmag',
 'nyrangers',
 'ochocinco',
 'official_1d_updates',
 'officialbiebernews',
 'okcthunder',
 'onedirection',
 'onedirection_1d_',
 'oprahwinfrey',
 'opry',
 'oscarprgirl',
 'ourbitches',
 'paniexx_shop',
 'parislemon',
 'patriots',
 'phenom',
 'philadelphiaeagles',
 'photogeekdom',
 'photojojo',
 'platinaline',
 'popeater',
 'postagram',
 'princessyahrini',
 'promoteshop5bath',
 'proud_3ra8ii',
 'puma',
 'q8booth',
 'questlove',
 'rainyseasonshop',
 'rapjuggernaut',
 'realmadrid',
 'red',
 'redbull',
 'reemteam',
 'repostapp',
 'reuters',
 'robertdobbsarmy',
 'ronaldinhooficial',
 'rotana.1',
 'rrharisov.life',
 'ryanseacrest',
 'sacramentokings',
 'sanasaeed2u',
 'savannahguthrie',
 'scobleizer',
 'selenagomez',
 'sellkixcity',
 'sellsneakershere',
 'serenawilliams',
 'shabab.insta',
 'shaketudinho',
 'shakira',
 'shawnjohnson',
 'shaym',
 'sheiva_h',
 'shlat_ta7shesh',
 'shopjeen',
 'smsaruae',
 'snoopdogg',
 'souljaboytellem',
 'starmagicphils',
 'stressedouthams',
 'stumptowncoffee',
 'stylelist',
 'surftudo',
 'svvaplife',
 'sweetyberryz',
 'tags.funny',
 'tatawerneck',
 'the_jest3r',
 'theaccessoryqueen_mrsdds',
 'theellenshow',
 'thegrammys',
 'thekatvond',
 'thekillertruth',
 'theone4you',
 'theonion',
 'therealbigboi',
 'therock',
 'theshins',
 'thinkinglikeamillionaire',
 'tobsangson0865355999',
 'todayshow',
 'tonyhawk',
 'tonytalkofny',
 'tpolamalu',
 'train',
 'travispastrana',
 'trendiest',
 'treysongz',
 'tru_chadd',
 'tvtoos',
 'tyrabanks',
 'univerity_of_baghdad1',
 'urbanoutfitters',
 'uselected',
 'vanessahudgens',
 'veuveclicquot',
 'vh1',
 'victoriabeckham',
 'vindiesel',
 'wakeupandmakeup',
 'warpedtour',
 'washingtonpost',
 'wholefoodsmarket',
 'wouter38',
 'wow.lmao',
 'yellow',
 'youngthegiant',
 'zacefron',
 'zachking',
 'zalezakaofficial',
 'zara',
 'zefron',
 'zendaya',
 'zooeydeschanel']

    # for user in users:
    #     if has_predictions_pkl(user):
    #         df1 = load_pkl(user)
    #         print 'previous df shape: {}'.format(df1.shape)
    #
    #         all_src_urls = set(dl.get_src_urls(user))
    #         cur_src_urls = set(df1.src_url)
    #         src_urls_toadd = all_src_urls - cur_src_urls
    #         df2 = pd.Series(list(src_urls_toadd))
    #         merged_df = pd.concat([df1, df2], axis=0)
    #
    #         print 'new df shape: {}'.format(merged_df.shape)
    #         fname = '../pickles/{}_predictions.pkl'.format(user)
    #         merged_df.to_pickle(fname)
    #         print 'len(all_src_urls): {}'.format(len(all_src_urls))


    for user in users:
        try:
            src_urls = dl.get_src_urls(user)
            src_urls_samp = rand_samp(src_urls)
            preds = []

            for url in src_urls_samp:
                #simulate a prediction
                # pred = np.random.rand(1000)
                pred = nn.predict(url)[0]
                preds.append(pred)
                time.sleep(20 + 3*random.random())

            df = pd.DataFrame(zip(src_urls_samp, preds), columns=['src_url','prediction'])
            fname = '../pickles/{}_predictions.pkl'.format(user)
            df.to_pickle(fname)
            with open('../logs/log_dataframe.txt', 'ab') as f:
                f.write('{} dataframe saved to {}\n'.format(strftime('%Y%m%d.%H:%M:%s'), fname))
            print '{} dataframe saved to {}\n'.format(strftime('%Y%m%d.%H:%M:%s'), fname)


        except:
            with open('../logs/log_dataframe.txt', 'ab') as f:
                f.write('{} {} Failed'.format(strftime('%Y%m%d.%H:%M:%s'),user))
            print '{} {} Failed'.format(strftime('%Y%m%d.%H:%M:%s'), user)
