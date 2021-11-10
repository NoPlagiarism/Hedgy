import aiohttp
from settings import Reddit


class SubredditNotFound(Exception):
    def __init__(self, subreddit):
        self.subreddit = subreddit

    def __str__(self):
        return f"{self.subreddit} not found."


class RedditAIO:
    GET_PAGE_URL = "https://www.reddit.com/r/{subreddit}/{listing}.json"

    class Listings:
        CONTROVERSIAL = "controversial"
        BEST = "best"
        HOT = "hot"
        NEW = "new"
        RANDOM = "random"
        RISING = "rising"
        TOP = "top"

    class TimeFrames:
        HOUR = "hour"
        DAY = "day"
        WEEK = "week"
        MONTH = "month"
        YEAR = "year"
        ALL = "all"

    def __init__(self, session=None):
        if session is None:
            session = aiohttp.ClientSession()
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    @staticmethod
    def _parse_args(**kwargs):
        for key in kwargs:
            if kwargs[key] is None:
                kwargs[key] = Reddit.__dict__.get('DEF_' + key.upper(), None)
        return kwargs

    async def get_raw_page(self, subreddit, listing=None, timeframe=None, limit=None, after=None):
        params = self._parse_args(listing=listing, timeframe=timeframe, limit=limit)
        listing = params.pop("listing")
        if after:
            params["after"] = after
        page = await self.session.get(self.GET_PAGE_URL.format(subreddit=subreddit, listing=listing),
                                      allow_redirects=True, params=params)
        if page.url.raw_path.startswith("/subreddits/search.json"):
            raise SubredditNotFound(subreddit)
        page_json = await page.json()
        return page_json

    async def get_raw_page_by_num(self, subreddit, num, listing=None, timeframe=None, limit=None):
        after = None
        for _ in range(num):
            page = await self.get_raw_page(subreddit, listing, timeframe, limit, after)
            after = page['data']['after']
        return page
