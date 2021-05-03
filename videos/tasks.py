from datetime import datetime, timedelta

from celery import current_app
from constants import VIDEO_FETCH_INTERVAL
from models import YoutubeVideos
from youtube import Youtube


celery_app = current_app._get_current_object()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender):
    sender.add_periodic_task(
        {"second": '*/{}'.format(VIDEO_FETCH_INTERVAL)},
        fetch_latest_videos.s(),
        name="send_signal_helpful_email",
    )


@celery_app.task
def fetch_latest_videos():
    now_time = datetime.utcnow()
    publish_after = now_time-timedelta(seconds=VIDEO_FETCH_INTERVAL)
    publish_before = now_time
    search = 'corona'
    obj = Youtube()
    res = obj.search_youtube_videos(search, publish_after, publish_before)
    model_obj = []

    while True:
        next_page_token = res.get('nextPageToken')
        items = res.get("items")
        for each in items:
            published_at = each.get("snippet", {}).get('publishedAt')
            title = each.get("snippet", {}).get('title')
            description = each.get("snippet", {}).get('description')
            url = each.get("snippet", {}).get('thumbnails', {}).get('default', {}).get("url")
            model_obj.append(YoutubeVideos(title=title, description=description, published_at=published_at, url=url))

        if not next_page_token:
            break
        res = obj.search_youtube_videos(search, publish_after, publish_before, next_page_token)

    if model_obj:
        YoutubeVideos.objects.bulk_create(model_obj)

