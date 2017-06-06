from datetime import datetime

#from django.db import models
from django.contrib.gis.db import models


class OpenGraphObject(models.Model):

    def __str__(self):
        return self.url

    # Required attributes
    url = models.CharField('URL', max_length=200)
    pub_date = models.DateTimeField('Publication date')

    # Open graph data
    title = models.CharField('Title', max_length=200, blank=True)
    site_name = models.CharField('Site name', max_length=200, blank=True)
    author = models.CharField('Author', max_length=200, blank=True)
    description = models.CharField('Description', max_length=2000, blank=True)
    image = models.CharField('Image URL', max_length=1000, blank=True)

    # Outlet information
    outlet = models.CharField('Outlet', max_length=200, blank=True)
    ind_owned = models.BooleanField('Indigenous-owned', default=False)

    # Social media data
    shares_twitter = models.IntegerField('Twitter shares', default=0)
    shares_facebook = models.IntegerField('Facebook shares', default=0)

    # Flag for manual OGP update
    manual = models.BooleanField('Manually updated', default=False)


class Outlet(models.Model):

    def __str__(self):
        return self.outlet

    outlet = models.CharField('Outlet ID', max_length=200, blank=True)
    name = models.CharField('', max_length=200, blank=True)
    # Details
    names_other = models.CharField('Other names (comma-separated)', max_length=500, blank=True)
    ind_owned = models.BooleanField('Indigenous owned', default=False)
    class_type = models.CharField('Classification type', max_length=200, blank=True)
    class_subtype = models.CharField('Classification subcategory', max_length=200, blank=True)
    description = models.CharField('Description', max_length=2000, blank=True)
    # Contact
    phone_work = models.CharField('Phone (work)', max_length=200, blank=True)
    phone_mobile = models.CharField('Phone (mobile)', max_length=200, blank=True)
    email = models.CharField('Email', max_length=200, blank=True)
    # Media
    website = models.CharField('Website URL', max_length=200, blank=True)
    website_rss = models.CharField('Website RSS', max_length=200, blank=True)
    facebook_url = models.CharField('Facebook URL', max_length=200, blank=True)
    twitter_id_str = models.CharField('Twitter ID', max_length=200, blank=True)
    # Geospatial
    geometry = models.PointField(srid=4326, null=True)
    objects = models.GeoManager()
    #geojson = models.CharField('GeoJSON (serialized JSON)', max_length=10000, blank=True)
    # JSON
    #json = models.CharField('Full outlet (serialized JSON)', max_length=20000, blank=True)


class Tweet(models.Model):

    def __str__(self):
        return self.id_str

    id_str = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('Publication date', default=datetime.now)
    text = models.TextField('Tweet text', blank=True)
    screen_name = models.CharField('@screen_name', max_length=200, blank=True)
    user_name = models.CharField('User name', max_length=200, blank=True)
    user_img = models.CharField(max_length=200, blank=True)

    outlet = models.CharField('Outlet', max_length=200, blank=True)

    url = models.CharField('Link to tweet', max_length=200, blank=True)
    url_user = models.CharField('Link to user', max_length=200, blank=True)

    # Topics (tweet.features)
    topic_0 = models.CharField(max_length=140, blank=True)
    topic_1 = models.CharField(max_length=140, blank=True)
    topic_2 = models.CharField(max_length=140, blank=True)
    topic_3 = models.CharField(max_length=140, blank=True)
    topic_4 = models.CharField(max_length=140, blank=True)
    topic_5 = models.CharField(max_length=140, blank=True)
    topic_6 = models.CharField(max_length=140, blank=True)
    topic_7 = models.CharField(max_length=140, blank=True)
    topic_8 = models.CharField(max_length=140, blank=True)
    topic_9 = models.CharField(max_length=140, blank=True)
    topic_10 = models.CharField(max_length=140, blank=True)
    topic_11 = models.CharField(max_length=140, blank=True)
    topic_12 = models.CharField(max_length=140, blank=True)
    topic_13 = models.CharField(max_length=140, blank=True)
    topic_14 = models.CharField(max_length=140, blank=True)
    topic_15 = models.CharField(max_length=140, blank=True)


class TweetTopic(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField('Topic name', max_length=200)
    count = models.IntegerField('Number of tweets', default=0)
    enabled = models.BooleanField('Enabled', default=True)

    # Sentiment data
    sentiment_positive = models.FloatField(
        'Percentage of tweets with positive sentiment', default=0.0)
    sentiment_neutral = models.FloatField(
        'Percentage of tweets with neutral sentiment', default=0.0)
    sentiment_negative = models.FloatField(
        'Percentage of tweets with negative sentiment', default=0.0)
