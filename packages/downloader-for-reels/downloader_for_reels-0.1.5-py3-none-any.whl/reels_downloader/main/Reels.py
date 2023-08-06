import aiohttp as aiohttp
from bs4 import BeautifulSoup

from ..common.model.ReelModel import ReelModel
from ..main.MediaInfo import MediaInfo


class Reels:

    def __init__(self, session_id: str):
        self.__session_id = session_id
        self.media_info = MediaInfo(session_id=session_id)

    async def get(self, reel_id: str) -> ReelModel | None:
        cookies = {
            "sessionid": self.__session_id,
            "mid": "Y9qARAAEAAFZ4_aUnQTGYLuaNswO"
        }
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(f"https://www.instagram.com/reel/{reel_id}/") as response:
                if response.status == 200:
                    raw_html = await response.text()
                    parser = BeautifulSoup(raw_html, "html.parser")
                    all_scripts = parser.find_all("script")
                    for script in all_scripts:
                        find_index = str(script.text).find("media_id")
                        # print(f"find_index: {find_index}")
                        if find_index != -1:
                            raw_media_id = script.text[find_index:find_index+50]
                            media_id = self.__parse_media_id(raw_media_id)
                            if media_id is not None:
                                return await self.media_info.get(media_id)


    @classmethod
    def __parse_media_id(cls, raw_media_id: str) -> int | None:
        try:
            media_id = raw_media_id.split('"')[2]
            return int(media_id)
        except Exception as e:
            return None
