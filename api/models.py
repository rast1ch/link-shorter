from django.db import models


class Link(models.Model):
    tocken = models.UUIDField(null=True)
    url_tocken = models.CharField(max_length=120, null=True)
    link_to = models.URLField()


class LinkUse(models.Model):
    link = models.ForeignKey(Link, related_name='jumps', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True)
