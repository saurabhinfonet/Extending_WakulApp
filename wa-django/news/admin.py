from django.contrib import admin

from .models import OpenGraphObject, Outlet, TweetTopic
from .models import Tweet

# Register your models here.

@admin.register(OpenGraphObject)
class OpenGraphObjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_filter = ('manual','pub_date')
    search_fields = ['url', 'outlet']

admin.site.register(Outlet)
admin.site.register(Tweet)
admin.site.register(TweetTopic)
