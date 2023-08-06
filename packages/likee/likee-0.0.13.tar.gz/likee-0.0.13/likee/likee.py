import json
import re

import config
import requests
import utils


class Likee:
    def __init__(self,link):
        if link.startswith("@"):
            self.link = f"https://likee.video/{link}/"
        else:
            self.link = link
        self._make_session()
    def _make_session(self):
        self.session = requests.Session()
        self.session.allow_redirects=True
    def _request(self, method, url, *args, **kwargs):

        if _headers := kwargs.get("headers"):
            kwargs.update({"headers":config.HEADERS.copy().update(_headers)})
        response = self.session.request(
            method,
            url,
            **kwargs)
        self.last_response = response
        return response
    def get_info(self):
        for _ in range(10):
            r = self._request("get", self.link)
            if match := re.search(r"<script>window\.data = (.*});", r.text):
                self.data = json.loads(match.group(1))
                break
            else:
                self._make_session()
                utils.small_delay()
        return self.data
    def get_video_info(self):
        r = self._request("post", "https://likee.video/official_website/VideoApi/getVideoInfo", **{"data":{"postIds":7016751439817917226},"headers":{"referer":self.link}})

