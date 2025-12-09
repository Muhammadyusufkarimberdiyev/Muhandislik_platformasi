# sitemaps.py (yangi fayl yarating)
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['muhandislik.uz','www.muhandislik.uz','muhandislik','muhandis'],'robototexnika'  # sizning URL nomlaringiz
    
    def location(self, item):
        return reverse(item)