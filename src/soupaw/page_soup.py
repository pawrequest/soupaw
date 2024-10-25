from __future__ import annotations

from aiohttp import ClientSession
import bs4

from scrapaw.get_soup import response_


class TagSoup(bs4.Tag):
    """
    Inject from_bs4 classmethod and select_text / select_link util funcs into BeautifulSoup
    PageSoup subclass injects from url classmethod
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_bs4_tag(cls, bs4_tag: bs4.Tag) -> TagSoup:
        return cls(bs4_tag.prettify(), "html.parser")

    def select_text(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs).text.strip()

    def select_link(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs)["href"]



class PageSoup(TagSoup):
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> PageSoup:
        html = await response_(url, http_session)
        return cls(url, html, "html.parser")
