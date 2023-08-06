"""Classes and methods needed to publish posts on a Fediverse instance."""
import re
from typing import Final
from typing import List
from typing import Optional

import aiohttp
from feedparser import FeedParserDict
from minimal_activitypub.client_2_server import ActivityPub

from .collect import get_file
from .control import Configuration
from .control import PostRecorder


class Fediverse:
    """Helper class to publish posts on a fediverse instance from rss feed items."""

    def __init__(self, config: Configuration, post_recorder: PostRecorder) -> None:
        self.config = config
        self.post_recorder = post_recorder

    async def publish(self, items: List[FeedParserDict]) -> None:
        """Publish posts to fediverse instance from content in the items list.

        :param items: Rss feed items to post
        """
        async with aiohttp.ClientSession() as session:
            fediverse = ActivityPub(
                instance=self.config.fedi_instance,
                session=session,
                access_token=self.config.fedi_access_token,
            )
            await fediverse.determine_instance_type()
            await fediverse.verify_credentials()

            for item in items:
                if await self.post_recorder.duplicate_check(identifier=item.link):
                    continue

                await fediverse.verify_credentials()

                # Post media if media_thumbnail is present with a url
                media_ids = await Fediverse._post_media(fediverse=fediverse, item=item)

                if media_ids:
                    status = await fediverse.post_status(
                        status=f"{item.title}\n\n{item.link}",
                        media_ids=media_ids,
                    )

                    print(f"Posted {item.title} to Fediverse at\n{status['url']}")

                    await self.post_recorder.log_post(shared_url=item.link)

    @staticmethod
    async def _post_media(
        fediverse: ActivityPub,
        item: FeedParserDict,
    ) -> Optional[List[str]]:
        """Post media to fediverse instance and return media ID.

        :param fediverse: ActivityPub api instance
        :param item: Feed item to load media from
        :returns:
            None or List containing one string of the media id after upload
        """
        if media_url := Fediverse._determine_image_url(item):
            media_path, mime_type = await get_file(media_url)
            if media_path:
                with media_path.open(mode="rb") as thumbnail:
                    media = await fediverse.post_media(
                        file=thumbnail,
                        mime_type=mime_type,
                    )

                # Delete temporary file
                media_path.unlink()

                return [media["id"]]

        return None

    @staticmethod
    def _determine_image_url(item: FeedParserDict) -> Optional[str]:
        """Determine URL for article image.

        :param item: Item to determine an image URL for
        :returns:
            None or string with URL to article image
        """
        MEDIA_KEYS: Final[List[str]] = ["media_thumbnail", "media_content"]
        SUMMARY_REGEXS: Final[List[str]] = [
            "<img .*?src=.*? *?/>",
            'src=.*?".*?"',
            '".*?"',
        ]

        for media_key in MEDIA_KEYS:
            if item.get(media_key) and item.get(media_key)[0].get("url"):
                return str(item.get(media_key)[0].get("url"))

        if (url := item.get("summary")) and "<img" in url:
            for regex in SUMMARY_REGEXS:
                match = re.search(
                    pattern=regex,
                    string=url,
                    flags=re.IGNORECASE,
                )
                if not match or not (url := match.group()):
                    return None
            return str(url)[1:-1]

        if links := item.get("links"):
            for link in links:
                if (link_type := link.get("type")) and "image" in link_type:
                    return str(link.get("href"))

        return None
