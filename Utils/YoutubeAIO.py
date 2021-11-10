import aiohttp
import random


def parse_args(kwargs):
    params = dict()
    for k, v in kwargs.items():
        if '_' in k:
            k = "".join(list(map(str.capitalize, k.split('_'))))
            k = k[0].lower() + k[1:]
        params[k] = v
    return params


class YoutubeDataApi:
    """Access data from the YouTube Data API using aiohttp
    Usage:
    async with YoutubeDataApi as yt:
        # Do whatever u want
    """
    def __init__(self, key, session=None, api_ver=3):
        self.key = key
        self.api_ver = api_ver
        self.api_url = "https://www.googleapis.com/youtube/v{}/".format(self.api_ver)

        if session is None:
            session = aiohttp.ClientSession()
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_playlist(self, part=('id', 'contentDetails'), get_all_items=False, **kwargs):
        """Get info about first playlist found by usual youtube data api params, unless get_all_items is True"""
        kwargs = parse_args(kwargs)
        part = ','.join(part)
        kwargs['part'] = part
        kwargs['key'] = self.key
        res = await self.session.get(self.api_url + "playlists", params=kwargs)
        json_res = await res.json()
        if get_all_items and json_res['items']:
            return json_res['items']
        if json_res['items']:
            return json_res['items'][0]
        return False

    async def random_from_playlist(self, playlist_info):
        """Get a random video from playlist"""
        item_id = random.randint(0, playlist_info["contentDetails"]["itemCount"]-1)
        items_url = self.api_url + "playlistItems"
        params = {"maxResults": 50, "part": "id,contentDetails", "playlistId": playlist_info['id'],
                  'key': self.key}
        items_raw = await self.session.get(items_url, params=params)
        items = await items_raw.json()
        for page_num in range(item_id // 50):
            params['pageToken'] = items['nextPageToken']
            items_raw = await self.session.get(items_url, params=params)
            items = await items_raw.json()
        return items['items'][item_id // 50 + item_id % 50]
