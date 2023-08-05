"""Classes and methods needed to publish posts on a Fediverse instance."""
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

                media_ids: Optional[List[str]] = None

                # Post media if media_thumbnail is present with a url
                if item.get("media_thumbnail") and item.get("media_thumbnail")[0].get(
                    "url"
                ):
                    media_path, mime_type = await get_file(
                        item.get("media_thumbnail")[0].get("url")
                    )
                    if media_path:
                        with media_path.open(mode="rb") as thumbnail:
                            media = await fediverse.post_media(
                                file=thumbnail,
                                mime_type=mime_type,
                            )
                            media_ids = [media["id"]]

                        # Delete temporary file
                        media_path.unlink()

                status = await fediverse.post_status(
                    status=f"{item.title}\n\n{item.link}",
                    media_ids=media_ids,
                )

                print(f"Posted {item.title} to Fediverse at\n{status['url']}")

                await self.post_recorder.log_post(shared_url=item.link)
