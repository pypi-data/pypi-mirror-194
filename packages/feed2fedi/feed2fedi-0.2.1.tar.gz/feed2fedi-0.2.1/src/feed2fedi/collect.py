"""Classes and methods to collect information needed by Feed2Fedi to make posts on Fediverse instance."""
import asyncio
import os
import re
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from urllib.parse import urlsplit

import aiohttp
import feedparser


class FeedReader:
    """Instances hold feed items for RSS/Atom feeds passed during instanciation."""

    def __init__(self, feeds: List[str]) -> None:
        self.items: List[feedparser.util.FeedParserDict] = []
        for feed in feeds:
            feed_info = feedparser.parse(feed)
            self.items.extend(feed_info.entries)


async def get_file(
    img_url: str,
) -> Tuple[Optional[Path], Optional[str]]:
    """Save a file located at img_url to a file located at filepath.

    :param img_url: url of imgur image to download

    :returns:
        Tuple containing:
            file_path (string): path to downloaded image or None if no image was downloaded
            mime_type (string): mimetype as returned from URL
    """
    image_file_path, mime_type = await determine_filename(img_url=img_url)

    chunk_size = 64 * 1024
    try:
        if not image_file_path:
            return None, None

        async with aiohttp.ClientSession(raise_for_status=True) as client:
            with image_file_path.open(mode="wb") as file_out:
                response = await client.get(url=img_url)
                async for data_chunk in response.content.iter_chunked(chunk_size):
                    file_out.write(data_chunk)
            await asyncio.sleep(0)  # allow client session to close before continuing

        return image_file_path, mime_type

    except aiohttp.ClientError as save_image_error:
        print(
            "collect.py - get_file(...) -> None - download failed with: %s"
            % save_image_error,
        )
        return None, None


async def determine_filename(img_url: str) -> Tuple[Optional[Path], Optional[str]]:
    """Determine suitable filename for an image based on URL.

    :param img_url: URL to image to determine a file name for.
    :returns:
        Tuple with Path or None for file name and mime-type or None
    """
    # First check if URL starts with http:// or https://
    regex = r"^https?://"
    match = re.search(regex, img_url, flags=0)
    if not match:
        print("Post link is not a full link: %s" % img_url)
        return None, None

    # Acceptable image formats
    image_formats = (
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
        "video/mp4",
    )

    # Determine mime type of linked media
    try:
        async with aiohttp.ClientSession(
            raise_for_status=True,
            read_timeout=30,
        ) as client:
            response = await client.head(url=img_url)
            headers = response.headers
            content_type = headers.get("content-type", None)

    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError) as error:
        print("Error while opening URL: %s " % error)
        return None, None

    if content_type not in image_formats:
        print("URL does not point to a valid image file: %s" % img_url)
        return None, None

    # URL appears to be an image, so determine filename
    file_name = os.path.basename(urlsplit(img_url).path)

    return Path(file_name), content_type
