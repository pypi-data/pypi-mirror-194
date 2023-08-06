"""Classes and methods to control how Feed2Fedi works."""
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Final
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import aiohttp
import aiosqlite
import arrow
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError

from . import DISPLAY_NAME
from . import FILE_ENCODING
from . import POST_RECORDER_SQLITE_DB
from . import WEBSITE

# Constants for use with config-parser
CACHE_DB_PATH_DEFAULT: Final[str] = "./cache.sqlite"
CACHE_DB_PATH_OPTION: Final[str] = "db-path"
CACHE_MAX_AGE_DEFAULT_30_DAYS: Final[str] = "30"
CACHE_MAX_AGE_OPTION: Final[str] = "max-age"
CACHE_SECTION: Final[str] = "Cache"
FEDIVERSE_ACCESS_TOKEN_OPTION: Final[str] = "access-token"
FEDIVERSE_INSTANCE_OPTION: Final[str] = "instance"
FEDIVERSE_SECTION: Final[str] = "Fediverse"
FEEDS_SECTION: Final[str] = "Feeds"

ConfigClass = TypeVar("ConfigClass", bound="Configuration")
PR = TypeVar("PR", bound="PostRecorder")


@dataclass
class Configuration:
    """Dataclass to hold configuration settings for Feed2Fedi."""

    feeds: List[str]
    fedi_instance: str
    fedi_access_token: str
    cache_max_age: int
    cache_db_path: str

    @classmethod
    async def load_config(
        cls: Type[ConfigClass], config_file_path: Path
    ) -> ConfigClass:
        """Load configuration values from file and create Configuration instance.

        :param config_file_path: File name to load configuration values from
        :returns:
            Configuration instance with values loaded from file_name
        """
        parser = ConfigParser()

        if not config_file_path.exists():
            config_file_path.touch()

        with config_file_path.open(mode="r", encoding=FILE_ENCODING) as config_file:
            parser.read_file(f=config_file)

        parsed_feeds: List[str] = []
        if parser.has_section(section=FEEDS_SECTION):
            for _key, feed in parser.items(section=FEEDS_SECTION):
                parsed_feeds.append(feed)
        else:
            parsed_feeds.append("http://feedparser.org/docs/examples/rss20.xml")

        instance = parser.get(
            section=FEDIVERSE_SECTION,
            option=FEDIVERSE_INSTANCE_OPTION,
            fallback=None,
        )
        access_token = parser.get(
            section=FEDIVERSE_SECTION,
            option=FEDIVERSE_ACCESS_TOKEN_OPTION,
            fallback=None,
        )

        if not instance:
            instance = Configuration._get_instance()
        if not access_token:
            access_token = await Configuration._get_access_token(instance=instance)

        cache_max_age = int(
            parser.get(
                section=CACHE_SECTION,
                option=CACHE_MAX_AGE_OPTION,
                fallback=CACHE_MAX_AGE_DEFAULT_30_DAYS,
            )
        )
        cache_db_path = parser.get(
            section=CACHE_SECTION,
            option=CACHE_DB_PATH_OPTION,
            fallback=CACHE_DB_PATH_DEFAULT,
        )

        return cls(
            feeds=parsed_feeds,
            fedi_instance=instance,
            fedi_access_token=access_token,
            cache_max_age=cache_max_age,
            cache_db_path=cache_db_path,
        )

    def save_config(self, config_file_path: Path) -> None:
        """Save Configuration to file.

        :param config_file_path: File name to save Configuration to
        """
        parser = ConfigParser()

        Configuration._add_cache_section(
            parser=parser,
            max_age=self.cache_max_age,
            db_path=self.cache_db_path,
        )
        Configuration._add_feeds_section(
            parser=parser,
            feeds=self.feeds,
        )
        Configuration._add_fediverse_section(
            parser=parser,
            instance=self.fedi_instance,
            access_token=self.fedi_access_token,
        )

        with config_file_path.open(mode="w", encoding=FILE_ENCODING) as config_file:
            parser.write(fp=config_file, space_around_delimiters=True)

    @staticmethod
    def _add_feeds_section(parser: ConfigParser, feeds: List[str]) -> None:
        """Add Feeds section to config parser.

        :param parser: ConfigParser to add the Feeds section to
        :param feeds: List of feed urls to add to Feeds section
        """
        parser.add_section(section=FEEDS_SECTION)
        feed_number = 1
        for feed in feeds:
            parser.set(section=FEEDS_SECTION, option=f"feed{feed_number}", value=feed)
            feed_number += 1

    @staticmethod
    def _add_cache_section(parser: ConfigParser, max_age: int, db_path: str) -> None:
        """Add Cache section to config parser.

        :param parser: ConfigParser to add the Feeds section to
        :param max_age: Max age in days to keep items in cache db
        :param db_path: path and file name for cache db
        """
        parser.add_section(section=CACHE_SECTION)
        parser.set(
            section=CACHE_SECTION, option=CACHE_MAX_AGE_OPTION, value=str(max_age)
        )
        parser.set(section=CACHE_SECTION, option=CACHE_DB_PATH_OPTION, value=db_path)

    @staticmethod
    def _add_fediverse_section(
        parser: ConfigParser,
        instance: str,
        access_token: str,
    ) -> None:
        """Add Fediverse section to config parser.

        :param parser: ConfigParser to add the fediverse section to
        :param instance:  URL of fediverse instance.
        :param access_token: Access_token for authenticating at fediverse instance
        """
        parser.add_section(section=FEDIVERSE_SECTION)
        parser.set(
            section=FEDIVERSE_SECTION, option=FEDIVERSE_INSTANCE_OPTION, value=instance
        )
        parser.set(
            section=FEDIVERSE_SECTION,
            option=FEDIVERSE_ACCESS_TOKEN_OPTION,
            value=access_token,
        )

    @staticmethod
    def _get_instance() -> str:
        """Get instance URL from user.

        :returns:
            URL of fediverse instance.
        """
        instance = input("[...] Please enter the URL for the instance to connect to: ")
        return instance

    @staticmethod
    async def _get_access_token(instance: str) -> str:
        """Get access token from fediverse instance.

        :param instance: URL to fediverse instance
        :returns:
            Access token
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Create app
                client_id, client_secret = await ActivityPub.create_app(
                    instance_url=instance,
                    session=session,
                    user_agent=DISPLAY_NAME,
                    client_website=WEBSITE,
                )

                # Get Authorization Code / URL
                authorization_request_url = (
                    await ActivityPub.generate_authorization_url(
                        instance_url=instance,
                        client_id=client_id,
                        user_agent=DISPLAY_NAME,
                    )
                )
                print(
                    f"Please go to the following URL and follow the instructions:\n"
                    f"{authorization_request_url}"
                )
                authorization_code = input(
                    "[...] Please enter the authorization code: "
                )

                # Validate authorization code and get access token
                access_token = await ActivityPub.validate_authorization_code(
                    session=session,
                    instance_url=instance,
                    authorization_code=authorization_code,
                    client_id=client_id,
                    client_secret=client_secret,
                )

        except ActivityPubError as error:
            print(f"! Error when setting up Fediverse connection: {error}")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

        return str(access_token)


class PostRecorder:
    """Record posts, check for duplicates, and deletes old records of posts."""

    LAST_POST_TS: Final[str] = "last-post-timestamp"

    def __init__(
        self: PR, history_db_path: str = f"./{POST_RECORDER_SQLITE_DB}"
    ) -> None:
        """Initialise PostRecord instance.

        :param history_db_dir: Location where history db should be stored. Default to current directory (.)
        """
        self.history_db_file = history_db_path
        self.history_db: Optional[aiosqlite.Connection] = None

    async def db_init(self: PR) -> None:
        """Initialise DB connection and tables if necessary."""
        self.history_db = await aiosqlite.connect(database=self.history_db_file)
        # Make sure DB tables exist
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS share "
            "(url TEXT PRIMARY KEY, shared_ts INT) "
            "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "CREATE INDEX IF NOT EXISTS index_ts ON share(shared_ts)"
        )
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS settings "
            "(key TEXT PRIMARY KEY, value) "
            "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (:key, :value)",
            {"key": PostRecorder.LAST_POST_TS, "value": 0},
        )
        await self.history_db.commit()

    async def duplicate_check(self: PR, identifier: str) -> bool:
        """Check identifier can be found in log file of content posted to
        Mastodon.

        :param identifier:
                Any identifier we want to make sure has not already been posted.
                This can be id of reddit post, url of media attachment file to be
                posted, or checksum of media attachment file.

        :returns:
                False if "identifier" is not in log of content already posted to
                Mastodon
                True if "identifier" has been found in log of content.
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        # check for Shared URL
        cursor = await self.history_db.execute(
            "SELECT * FROM share where url=:url", {"url": identifier}
        )
        if await cursor.fetchone():
            return True

        return False

    async def log_post(
        self: PR,
        shared_url: str,
    ) -> None:
        """Log details about reddit posts that have been published.

        :param reddit_id:
                Id of post on reddit that was published to Mastodon
        :param shared_url:
                URL of media attachment that was shared on Mastodon
        :param check_sum:
                Checksum of media attachment that was shared on Mastodon.
                This enables checking for duplicate media even if file has been renamed.
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        timestamp = arrow.utcnow().timestamp()
        await self.history_db.execute(
            "INSERT INTO share (url, shared_ts) VALUES (?, ?)",
            (
                shared_url,
                timestamp,
            ),
        )
        await self.history_db.commit()

    async def get_setting(
        self: PR,
        key: str,
    ) -> Any:
        """Retrieve a setting from database.

        :param key: Key to setting stored in DB

        :return: Value of setting. This could be an int, str, or float
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        cursor = await self.history_db.execute(
            "SELECT value FROM settings WHERE key=:key",
            {"key": key},
        )
        row = await cursor.fetchone()
        if row is None:
            return None

        return row[0]

    async def save_setting(
        self: PR,
        key: str,
        value: Union[int, str, float],
    ) -> None:
        """Save a setting to database.

        :param key: Key to setting stored in DB
        :param value: Value to store as a setting

        :return: None
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        await self.history_db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (:key, :value)",
            {"key": key, "value": value},
        )

        await self.history_db.commit()

    async def prune(self, max_age_in_days: int) -> None:
        """Prune entries from db that are older than max_age_in_days.

        :param max_age_in_days: Maximum age of records to keep in DB
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        max_age_ts = arrow.utcnow().shift(days=-max_age_in_days).timestamp()
        await self.history_db.execute(
            "DELETE FROM share WHERE shared_ts<:max_age_ts",
            {"max_age_ts": max_age_ts},
        )
        await self.history_db.commit()

    async def close_db(self: PR) -> None:
        """Close db connection."""
        if self.history_db:
            await self.history_db.close()

    async def import_urls(self, url_file: Path) -> None:
        """Import URLS from for example the cache.db of feed2toot.

        :param url_file: File path containing one URL per line
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        line_count = 0
        with url_file.open(mode="r", encoding=FILE_ENCODING) as import_file:
            while entry := import_file.readline():
                await self.log_post(shared_url=entry)
                line_count += 1

        print(f"Imported {line_count} urls")
