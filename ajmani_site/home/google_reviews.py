from datetime import datetime, timedelta
import logging

import requests
from django.conf import settings
from django.utils import timezone

from home.models import GoogleReview, GoogleReviewFeed

logger = logging.getLogger(__name__)

SEARCH_TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
PLACE_DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"


def get_google_review_context(page):
    feed = GoogleReviewFeed.objects.first()

    if settings.GOOGLE_PLACES_API_KEY and page.google_reviews_query:
        try:
            feed = sync_google_reviews(page)
        except Exception as error:  # pragma: no cover - network integration fallback
            logger.warning("Google review sync failed: %s", error)

    if feed is None:
        return None, []

    reviews = list(feed.reviews.all()[:5])
    return feed, reviews


def sync_google_reviews(page):
    feed, _ = GoogleReviewFeed.objects.get_or_create(key="ajmani-homepage")
    sync_interval = timedelta(hours=settings.GOOGLE_REVIEWS_SYNC_INTERVAL_HOURS)
    now = timezone.now()

    if feed.last_synced_at and now - feed.last_synced_at < sync_interval and feed.reviews.exists():
        return feed

    place_id = page.google_place_id or feed.place_id or _resolve_place_id(page.google_reviews_query)
    if not place_id:
        return feed

    place_details = _fetch_place_details(place_id)
    review_items = place_details.get("reviews", [])
    review_ids = []

    feed.place_id = place_id
    feed.place_name = place_details.get("displayName", {}).get("text", "")
    feed.average_rating = place_details.get("rating") or 0
    feed.total_review_count = place_details.get("userRatingCount") or 0
    feed.google_maps_url = place_details.get("googleMapsUri") or page.google_maps_url or page.google_business_share_url
    feed.last_synced_at = now
    feed.sync_error = ""
    feed.save()

    for index, review in enumerate(review_items):
        review_name = review.get("name", f"{place_id}-{index}")
        author = review.get("authorAttribution", {}) or {}
        review_text = (review.get("text") or {}).get("text", "")
        published_at = review.get("publishTime")
        published_at_value = None
        if published_at:
            published_at_value = datetime.fromisoformat(
                published_at.replace("Z", "+00:00")
            )

        review_obj, _ = GoogleReview.objects.update_or_create(
            review_id=review_name,
            defaults={
                "feed": feed,
                "author_name": author.get("displayName", "Google reviewer"),
                "author_url": author.get("uri", ""),
                "author_photo_url": author.get("photoUri", ""),
                "rating": review.get("rating") or 0,
                "relative_publish_time_description": review.get("relativePublishTimeDescription", ""),
                "review_text": review_text,
                "review_url": review.get("googleMapsUri") or feed.google_maps_url,
                "published_at": published_at_value,
                "display_order": index,
            },
        )
        review_ids.append(review_obj.review_id)

    if review_ids:
        GoogleReview.objects.filter(feed=feed).exclude(review_id__in=review_ids).delete()

    return feed


def _resolve_place_id(query):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "places.id",
    }
    response = requests.post(
        SEARCH_TEXT_URL,
        headers=headers,
        json={"textQuery": query, "maxResultCount": 1},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    places = payload.get("places", [])
    if not places:
        return ""
    return places[0].get("id", "")


def _fetch_place_details(place_id):
    headers = {
        "X-Goog-Api-Key": settings.GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "displayName,rating,userRatingCount,reviews,"
            "googleMapsUri"
        ),
    }
    response = requests.get(
        PLACE_DETAILS_URL.format(place_id=place_id),
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
