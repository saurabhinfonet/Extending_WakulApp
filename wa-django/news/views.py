# Author : Elyas
# Contribution : Saurabh Sharma
# Views created for added features.

import json
import yaml
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
#from django.contrib.postgres.search import SearchVector

from el_pagination.decorators import page_template

from .models import Outlet, OpenGraphObject, Tweet, TweetTopic

@page_template('news/entry_list_page.html')  # just add this decorator
def news_feed(request, category='latest', template='news/index.html', extra_context=None):
    cat_str = str(category)

    if (cat_str == 'feed') or (cat_str == 'rss'):
        return rss(request, category)

    # Generate class tags for the page
    body_tags = 'news'
    body_tags += (' news-' + cat_str)
    # Generate the list of articles (process the category)
    if (cat_str == 'search'):
        q = request.GET.get('q', '')
        o = request.GET.get('o', '')
        if (q != ''):
            entries = OpenGraphObject.objects.order_by('-pub_date').filter(
                Q(url__search=q)
                | Q(title__search=q)
                | Q(site_name__search=q)
                | Q(author__search=q)
                | Q(description__search=q)
            )
            extra_context.update({'q': q})
            body_tags += (' news-search-' + q)
        elif (o != ''):
            entries = OpenGraphObject.objects.order_by('-pub_date').filter(outlet=o)
            extra_context.update({'o': o})
            body_tags += ( 'news-search-' + o)
        else:
            entries = None
    elif (cat_str == 'indigenous'):
        entries = OpenGraphObject.objects.filter(ind_owned=True).order_by('-pub_date')
    elif (cat_str == 'indigenous-trending'):
        entries = OpenGraphObject.objects.filter(ind_owned=True).order_by('-shares_twitter').filter(pub_date__gte=(datetime.now()-timedelta(days=28)))
    elif (cat_str == 'latest'):
        entries = OpenGraphObject.objects.order_by('-pub_date')
    elif (cat_str == 'trending'):
        entries = OpenGraphObject.objects.order_by('-shares_twitter').filter(pub_date__gte=(datetime.now()-timedelta(days=28)))
    else:
        entries = None
    # In the future, do future processing on parameters here
    # (e.g. ?descending=true etc.)

    # Other context
    extra_context.update(load_sidebars())
    # Generate context
    context = {
        'entries': entries,
        'body_tags': body_tags,
        'category': category
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

def rss(request, slug, category='latest'):
    return news_feed(request, category, template='news/rss.xml')

@page_template('news/tweet_list_page.html')  # just add this decorator
def twitter_topic(request, topic='', template='news/index.html', extra_context=None):
    topic_str = str(topic)

    # Generate class tags for the page
    body_tags = 'twitter ' + 'twitter-topic-' + topic_str
    # Generate the list of articles (process the category)
    if (topic_str != ''):
        entries = Tweet.objects.order_by('-pub_date').filter(
            Q(topic_0=topic_str) | Q(topic_1=topic_str)
            | Q(topic_2=topic_str) | Q(topic_3=topic_str)
            | Q(topic_4=topic_str) | Q(topic_5=topic_str)
            | Q(topic_6=topic_str) | Q(topic_7=topic_str)
            | Q(topic_8=topic_str) | Q(topic_9=topic_str)
            | Q(topic_10=topic_str) | Q(topic_11=topic_str)
            | Q(topic_12=topic_str) | Q(topic_13=topic_str)
            | Q(topic_14=topic_str) | Q(topic_15=topic_str)
        )
        tweet_topic = TweetTopic.objects.get(name=topic)
    else:
        entries = Tweet.objects.order_by('-pub_date')
        tweet_topic = None

    # Other context
    extra_context.update(load_sidebars())
    # Generate context
    context = {
        'entries': entries,
        'body_tags': body_tags,
        'topic': topic,
        'tweet_topic': tweet_topic
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
@page_template('news/entry_list_page.html')



# view created for sentimental analysis.html
def sentiment(request, template='news/sentimental_analysis.html', extra_context=None):

    # Other context
    extra_context.update(load_sidebars())
    context={}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)




def directory(request, outlet=None, template='news/directory.html'):
    context = {}
    # Generate class tags
    body_tags = 'directory'
    body_tags += (' directory-' + str(outlet))
    # List of outlets for the aside
    outlets = Outlet.objects.order_by('name')

    if outlet is not None:
        entry = Outlet.objects.get(outlet=outlet)
        context.update({'entry': entry})
        news_feed = OpenGraphObject.objects.filter(outlet=outlet).order_by('-pub_date')[:5]
        if news_feed:
            context.update({'news_feed': news_feed})
        tweets = Tweet.objects.filter(outlet=outlet).order_by('-pub_date')[:10]
        print(len(tweets))
        if tweets:
            context.update({'tweets': tweets})

    context.update({
        'outlets': outlets,
        'outlet': outlet,
        'body_tags': body_tags,
    })

    return render(request, template, context)





def about(request, template="news/about.html"):
    context = {
        'body_tags': 'about'
    }
    return render(request, template, context)




def training(request, template="news/blank.html"):
    context = {}
    return render(request, template, context)




# view created for first nation.html
def firstnation(request, template="news/first_nation.html", extra_context={}):
    
    context={}
    extra_context.update(load_sidebars())
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)




    
# map function modified
# view for interactive map 
def map(request, map_view=None, template="news/map.html", extra_context={}):

    outlets = []
    radios = []
    tweets = []
    articles = []
    if(map_view == 'radio'):
        outlets = Outlet.objects.filter(class_subtype='radio_station')
        radios = outlets
    if(map_view == 'tweet'):
        outlets = Outlet.objects.filter(class_subtype = 'twitter')
        tweets = outlets

    if(map_view == 'Article'):
        outlets = Outlet.objects.filter(class_subtype = 'blogs')
        articles = outlets
    
    # Other context
    extra_context.update(load_sidebars())
    # Generate context
    context = {
        'outlets': outlets,
        'radios': radios,
        'tweets': tweets,
        'news_feed': articles,
        'body_tags': 'map',
        'map_view': map_view.title()
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)




def load_sidebars():
    tweet_topics = TweetTopic.objects.order_by('-count').filter(enabled=True)[:15]
    latest_tweets = Tweet.objects.order_by('-pub_date')[:4]
    outlets = get_outlets()
    extra_context = {
        'tweet_topics': tweet_topics,
        'latest_tweets': latest_tweets,
        'article_outlets': outlets
    }
    return extra_context

def get_outlets():
    outlets = [
        {'id':'','name':''},
        {'id':'1deadlynation','name':'1 Deadly Nation'},
        {'id':'abc_indigenous','name':'ABC Indigenous'},
        {'id':'aboriginal_message','name':'Aboriginal Message'},
        {'id':'allan_clarke','name':'Allan Clarke'},
        {'id':'anangu_lands_paper_tracker','name':'The Anangu Lands Paper Tracker'},
        {'id':'ascensionmag','name':'Ascension Magazine'},
        {'id':'atsiphj_aad','name':'Australian Aboriginal Directory'},
        {'id':'atsiphj_aanews','name':'Australian Aboriginal News and Media Issues'},
        {'id':'awaken','name':'Awaken'},
        {'id':'awaye','name':'Awaye!'},
        {'id':'black_thoughts_live_here','name':'Black Thoughts Live Here'},
        {'id':'black_white_and_rainbow','name':'Black White and Rainbow'},
        {'id':'caama','name':'CAAMA Radio'},
        {'id':'capemagazine','name':'Cape Magazine'},
        {'id':'croakey','name':'Croakey'},
        {'id':'firstnationstelegraph','name':'First Nations Telegraph'},
        {'id':'generationone','name':'GenerationOne'},
        {'id':'ilc_unsw','name':'Indigenous Law Centre'},
        {'id':'indigenous_gov_au','name':'indigenous.gov.au'},
        {'id':'indigenousx','name':'Indigenous X'},
        {'id':'jack_latimore','name':'Jack Latimore'},
        {'id':'koorimail','name':'Koori Mail'},
        {'id':'kooriradio','name':'Koori Radio'},
        {'id':'lets_talk','name':"""Let's Talk"""},
        {'id':'living_black','name':'Living Black'},
        {'id':'naaja','name':'North Australian Aboriginal Justice Agency'},
        {'id':'nasca','name':'National Aboriginal Sporting Chance Academy'},
        {'id':'nganampa_wangka','name':'Nganampa Wangka'},
        {'id':'nintione','name':'Ninti One'},
        {'id':'nirs','name':'National Indigenous Radio Service'},
        {'id':'nit','name':'National Indigenous Times'},
        {'id':'noongarradio','name':'Noongar Radio'},
        {'id':'nunga_wangga','name':'Nunga Wangga'},
        {'id':'nyunggablack','name':'Nyungga Black'},
        {'id':'solidarity_online','name':'Solidarity Online'},
        {'id':'speaking_out','name':'Speaking Out'},
        {'id':'thekooriwoman','name':'The Koori Woman'},
        {'id':'thestringer','name':'The Stringer'}
    ]
    return outlets

def get_radio_outlets():
    outlets = [
        {
            'id': '3knd',
            'name': '3KND',
            'name_long': '3 Kool n Deadly',
            'freq': '1503AM',
            'lat': -37.7415712,
            'lng': 145.00220,
            'stream': 'http://freezone.iinet.net.au/include/radio/playlists/75.m3u'
        },
        {
            'id': '4k1g',
            'name': '4K1G',
            'name_long': '4K1G FM',
            'freq': '107.1FM',
            'lat': -19.2615483,
            'lng': 146.813286,
            'stream': 'http://radio.securenetsystems.net/radio_player_large.cfm?stationCallSign=41KGFM'
        },
        {
            'id': '4mw',
            'name': '4MW',
            'name_long': '4 Meriba Wakai',
            'freq': '1260AM',
            'lat': -10.5842467,
            'lng': 142.2192314,
            'stream': ''
        },
        {
            'id': 'bbm987',
            'name': 'BBM',
            'name_long': 'Bumma Bippera Media',
            'freq': '98.7FM',
            'lat': -16.9337614,
            'lng': 145.7652356,
            'stream': 'http://198.74.51.37:9984/listen.pls'
        },
        {
            'id': 'goolarri',
            'name': '6GME',
            'name_long': 'Radio Goolarri',
            'freq': '99.7FM',
            'lat': -17.9639,
            'lng': 122.2215,
            'stream': 'http://listen.shoutcast.com/radiogoolarri.m3u'
        },
        {
            'id': 'mob_fm',
            'name': '4MOB',
            'name_long': 'MOB FM',
            'freq': '100.9FM',
            'lat': -20.7204358,
            'lng': 139.4925398,
            'stream': ''
        },
        {
            'id': 'noongarradio',
            'name': 'Noongar',
            'name_long': 'Noongar Radio',
            'freq': '100.9FM',
            'lat': -31.94629,
            'lng': 115.86434,
            'stream': 'http://streaming.noongarradio.com/listen.pls'
        },
        {
            'id': 'radio_4us',
            'name': '4US',
            'name_long': 'Radio 4US',
            'freq': '100.7FM',
            'lat': -23.3790772,
            'lng': 150.510016,
            'stream': ''
        },
        {
            'id': 'radioskidrow',
            'name': '2RSR',
            'name_long': 'Radio Skid Row',
            'freq': '88.9FM',
            'lat': -33.9016536,
            'lng': 151.1620334,
            'stream': 'http://www.radioskidrow.org/mono32.asx'
        },
        {
            'id': 'warringarriradio',
            'name': '6WR',
            'name_long': 'Warringarri Radio',
            'freq': '693AM',
            'lat': -15.7621208,
            'lng': 128.7376571,
            'stream': 'http://s20.myradiostream.com:12938/listen.m3u'
        }
    ]
    return outlets
