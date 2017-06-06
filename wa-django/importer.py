import os
import sys
import time
import datetime
import json
import yaml

import couchdb


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wakulapp.settings")

import django
django.setup()

from news.models import OpenGraphObject, Tweet, TweetTopic, Outlet

def update_article_shares():
    article_urls = {}
    try:
        #was originally 'tweets/article_urls'
        for row in db_tweets_urls.view('tweets/article_urls', wrapper=None, group=True):
            article_urls.update({row.key: row.value})
    except:
        return

    for o in OpenGraphObject.objects.all():
        try:
            if (str(o)) in article_urls:
                o.shares_twitter = int(article_urls[str(o)])
                o.save(update_fields=["shares_twitter"])
        except:
            pass
    print("update article shares complete")
    return

def fetch_new_articles():
    current_articles = []
    for o in OpenGraphObject.objects.all():
        try:
            current_articles.append(str(o))
        except:
            pass

    timerange = str(int(time.time() - 60*60*24*days))
    articles = []
    try:
        for row in db_articles.view('articles/opengraph', wrapper=None, descending='true',
                           endkey=timerange):
            articles.append(row.value)
    except:
        return

    article_urls = {}
    try:
        #was originally 'tweets/article_urls'
        for row in db_tweets_urls.view('tweets/article_urls', wrapper=None, group=True):
            article_urls.update({row.key: row.value})
    except Exception as e:
        print(str(e))
        return

    for a in articles:
        if a['og']['url'] not in current_articles:
            # Attributes
            url = a['og']['url']
            pub_date = datetime.datetime.fromtimestamp(int(a['wa']['publish_time']))
            try:
                title = a['og']['title']
            except KeyError:
                title = ''
            try:
                site_name = a['og']['site_name']
            except KeyError:
                site_name = ''
            try:
                author = a['article']['author']['username']
            except KeyError:
                author = ''
            try:
                description = a['og']['description']
            except KeyError:
                description = ''
            try:
                if 'image' in a['og']:
                    if isinstance(a['og']['image'], dict):
                        image = a['og']['image']['content']
                    else:
                        image = a['og']['image']
            except KeyError:
                image = ''
            try:
                outlet = a['wa']['outlet']
            except KeyError:
                outlet = ''
            try:
                ol = db_outlets.get(outlet)
                ind_owned = ol['classification']['ind_ownership']
            except:
                ind_owned = False
            try:
                shares_twitter = article_urls[url]
            except KeyError:
                shares_twitter = 0

            try:
                # Store new OG Object
                new_article = OpenGraphObject(
                    url=url,
                    pub_date=pub_date,
                    title=title,
                    site_name=site_name,
                    author=author,
                    description=description,
                    image=image,
                    outlet=outlet,
                    ind_owned=ind_owned,
                    shares_twitter=shares_twitter
                )
                new_article.save()
            except:
                pass

def update_outlets():
    try:
        # Retrieve outlets in CouchDB
        for row in couch['outlets'].view(
            '_all_docs',
            wrapper=None
        ):
            try:
                if (str(row.key).startswith('_') is False):
                    outlet_couchdb = dict(couch['outlets'].get(row.key))
                    try:
                        outlet = Outlet.objects.get(outlet=outlet_couchdb['_id'])
                    except Exception as e:
                        outlet = Outlet(outlet=outlet_couchdb['_id'])
                    # Outlet.name and Outlet.names_other
                    try:
                        name = outlet_couchdb['name']   
                        print(name)
                        if isinstance(name, str):
                            outlet.name = name
                        if isinstance(name, list):
                            outlet.name = name.pop(0)
                            outlet.names_other = ','.join(name)
                    except:
                        pass
                    # Outlet.ind_owned
                    try:
                        outlet.ind_owned = outlet_couchdb['classification']['ind_ownership']
                    except:
                        pass
                    # Outlet.class_type
                    try:
                        outlet.class_type = outlet_couchdb['classification']['type']
                    except:
                        pass
                    # Outlet.class_subtype
                    try:
                        outlet.class_subtype = outlet_couchdb['classification']['subcategory']
                    except:
                        pass
                    # Outlet.description
                    try:
                        outlet.description = outlet_couchdb['notes']
                    except:
                        pass
                    # Outlet.phone_work
                    try:
                        outlet.phone_work = outlet_couchdb['contacts']['phone_work']
                    except:
                        pass
                    # Outlet.phone_mobile
                    try:
                        outlet.phone_mobile = outlet_couchdb['contacts']['phone_mobile']
                    except:
                        pass
                    # Outlet.email
                    try:
                        outlet.email = outlet_couchdb['contacts']['email']
                    except:
                        pass
                    # Outlet.website
                    try:
                        outlet.website = outlet_couchdb['website']['url']
                    except:
                        pass
                    # Outlet.website_rss
                    try:
                        outlet.website_rss = outlet_couchdb['website']['rss']
                    except:
                        pass
                    # Outlet.facebook_url
                    try:
                        outlet.facebook_url = outlet_couchdb['facebook']['url']
                    except:
                        pass
                    # Outlet.twitter_id_str
                    try:
                        outlet.twitter_id_str = outlet_couchdb['twitter']['id_str']
                    except:
                        pass
                    # Outlet.geometry
                    try:
                        outlet.geometry = 'POINT({lat} {lng})'.format(
                            lat=outlet_couchdb['place']['geometry']['coordinates'][0],
                            lng=outlet_couchdb['place']['geometry']['coordinates'][1],
                        )
                    except:
                        pass
                    outlet.save()
            except:
                pass
    except:
        return None

def update_topics():
    def get_sentiment(name):
        map_fun = '''function(doc) {
          for (var i = 0; i < doc.features.length; i++) {
            if (doc.features[i] == "''' + name + '''") {
              emit(doc.sentiment.sentiment, 1);
            }
          }
        }'''
        reduce_fun = '''_sum'''
        count_positive = 0.0
        count_neutral = 0.0
        count_negative = 0.0
        for row in couch['tweets'].query(map_fun, reduce_fun=reduce_fun,
            language='javascript', wrapper=None, group=True):
            if (row.key == 'positive'):
                count_positive = float(row.value)
            elif (row.key == 'neutral'):
                count_neutral = float(row.value)
            elif (row.key == 'negative'):
                count_negative = float(row.value)

        total = float(count_positive + count_neutral + count_negative)
        sentiment_positive = (count_positive / total)*100
        sentiment_neutral = (count_neutral / total)*100
        sentiment_negative = (count_negative / total)*100

        return sentiment_positive, sentiment_neutral, sentiment_negative

    # Download topics from CouchDB
    minimum = 100
    topics = {}
    try:
        for row in couch['tweets'].view(
            'tweets/topics',
            wrapper=None,
            group=True
        ):
            topics.update({row.key: row.value})
    except Exception as e:
        print(str(e))
        return
    tweet_topics = []
    for t in sorted(topics, key=topics.get, reverse=True):
        if (int(topics[t]) >= minimum):
            tweet_topics.append({t: topics[t]})

    # Iterate through topics in Django
    for t in TweetTopic.objects.all():
        if (str(t)) not in topics:
            t.delete()

    for t in tweet_topics:
        for name in t:
            try:
                current_topic = TweetTopic.objects.get(name=str(name))
                print('Updating topic: ' + name)
            except Exception as e:
                current_topic = TweetTopic(name=name)
                print('Creating new topic: ' + name)
            current_topic.count = t[name]
            current_topic.sentiment_positive, current_topic.sentiment_neutral, current_topic.sentiment_negative = get_sentiment(name)
            current_topic.save()


def update_tweets(fast=False):
    try:
        for row in couch['tweets'].iterview(
            '_all_docs',
            batch=1000,
            wrapper=None,
            descending=True
        ):
            if (str(row.key).startswith('_') is False):
                try:
                    new_tweet = Tweet.objects.get(id_str=str(row.key))
                    print("Tweet already in postgresql")
                    if fast is True:
                        return
                except:
                    print("Storing new tweet: " + str(row.key))
                    tweet = dict(couch['tweets'].get(row.key))
                    pub_date = datetime.datetime.fromtimestamp(int(tweet['wa']['time']))
                    if 'url_outlet' in tweet['wa']:
                        outlet = tweet['wa']['url_outlet']
                    else:
                        outlet = ''

                    # create urls
                    url = 'https://twitter.com/{screen_name}/status/{id_str}'.format(
                        screen_name = tweet['user']['screen_name'],
                        id_str = tweet['id_str']
                    )
                    url_user = 'https://twitter.com/{screen_name}'.format(
                        screen_name = tweet['user']['screen_name']
                    )
                    # create topics
                    topics = []
                    for i in range(0,16):
                        try:
                            topics.append(tweet['features'][i])
                        except:
                            topics.append('')

                    new_tweet = Tweet(
                        id_str=tweet['id_str'],
                        pub_date=pub_date,
                        text=tweet['text'],
                        screen_name=tweet['user']['screen_name'],
                        user_name=tweet['user']['name'],
                        user_img=tweet['user']['profile_image_url_https'],
                        outlet=outlet,
                        url=url,
                        url_user=url_user,
                        topic_0=topics[0],
                        topic_1=topics[1],
                        topic_2=topics[2],
                        topic_3=topics[3],
                        topic_4=topics[4],
                        topic_5=topics[5],
                        topic_6=topics[6],
                        topic_7=topics[7],
                        topic_8=topics[8],
                        topic_9=topics[9],
                        topic_10=topics[10],
                        topic_11=topics[11],
                        topic_12=topics[12],
                        topic_13=topics[13],
                        topic_14=topics[14],
                        topic_15=topics[15]
                    )
                    new_tweet.save()
    except Exception as e:
        print(str(e))

def delete_articles():
    for o in OpenGraphObject.objects.all():
        o.delete()

def update_couchdb_articles():

    for o in OpenGraphObject.objects.filter(manual=True):
        print("Updating article: " + str(o.url))
        article = dict(couch['articles'].get(str(o.url)))
        article['ogp']['manual'] = True
        article['ogp']['og']['title'] = o.title
        article['ogp']['og']['description'] = o.description
        article['ogp']['og']['image'] = o.image
        couch['articles'].save(article)
    # So basically - if OGP in Django is diff from CouchDB, update CouchDB doc
    # But obv restrict this to certain attributes
    # Also need a way of flagging the CouchDB doc that it has been manually
    # updated (set article['ogp']['manual'] = True)
    return None

# Parse config.yaml
with open('config.yaml', 'r') as stream:
    args = yaml.load(stream)

protocol = 'http'
login = args['couchdb']['login']
password = args['couchdb']['password']
ip = args['couchdb']['ip_address']
port = str(args['couchdb']['port'])

url = '{protocol}://{login}:{password}@{ip}:{port}/'.format(
    protocol = protocol,
    login = login,
    password = password,
    ip = ip,
    port = port
)
couch = couchdb.Server(url)

db_articles = couch['articles']
db_tweets = couch['tweets']
db_tweets_urls = couch['tweets_urls']
db_outlets = couch['outlets']
days = 365*4


update_outlets()

while True:
    try:
        update_topics()
    except:
        pass
    try:
        update_tweets(fast=True)
    except:
        pass
    try:
        update_article_shares()
    except:
        pass
    try:
        fetch_new_articles()
    except:
        pass
