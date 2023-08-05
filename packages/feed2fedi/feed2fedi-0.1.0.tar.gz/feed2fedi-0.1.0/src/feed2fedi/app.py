"""Main processing and main entry point methods for Feed2Fedi."""
import asyncio
from pathlib import Path

from . import DISPLAY_NAME
from . import __version__
from .collect import FeedReader
from .control import Configuration
from .control import PostRecorder
from .publish import Fediverse


async def main():
    """Read configuration and feeds, then make posts while avoiding duplicates."""
    print(f"Welcome to {DISPLAY_NAME} {__version__}")

    config = await Configuration.load_config(config_file_path=Path("config.ini"))
    config.save_config(config_file_path=Path("config.ini"))

    post_recorder = PostRecorder(history_db_path=config.cache_db_path)
    await post_recorder.db_init()
    await post_recorder.prune(max_age_in_days=config.cache_max_age)

    items = FeedReader(feeds=config.feeds).items

    fediverse = Fediverse(config=config, post_recorder=post_recorder)
    await fediverse.publish(items=items)

    await post_recorder.close_db()


def start_main() -> None:
    """Start processing, i.e. main entry point."""
    asyncio.run(main())
