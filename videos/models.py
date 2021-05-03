from django.db import models


class Auditable(models.Model):
    created_by = models.CharField(max_length=100, default='admin', null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    updated_by = models.CharField(max_length=100, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class YoutubeVideos(Auditable):
    title = models.CharField(max_length=2000, blank=False, null=False, db_index=True)
    description = models.CharField(max_length=2000, blank=False, null=False, db_index=True)
    published_at = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=100, blank=False, null=False)
