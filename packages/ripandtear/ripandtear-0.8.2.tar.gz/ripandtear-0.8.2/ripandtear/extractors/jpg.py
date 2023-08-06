import asyncio
import httpx
import logging
import re

from bs4 import BeautifulSoup
from datetime import datetime

from ripandtear.extractors.common import Common
from ripandtear.utils.custom_types import UrlDictionary
from ripandtear.utils import rat_info
from ripandtear.utils.tracker import Tracker

log = logging.getLogger(__name__)

sem = asyncio.Semaphore(6)

# 'https://simp4.jpg.church/1206x2208_bb3d16221cfbf54df75b3d2b6618b5e7.jpg'
re_direct_image_link = re.compile(
    r"(https?://)(\w+\.)?((jpg|pixl)\.(church|fish|li))(/|/images/)([\w\/]+/)([\w\-_\(\)\.]+)\.(\w+)")

# 'https://jpg.fish/img/1206x2208-bb3d16221cfbf54df75b3d2b6618b5e7.TmmoSd'
re_image_page = re.compile(
    r"(https?://)(\w+\.)?((jpg|pixl)\.(church|fish|li))(/(img|image)/)([\w\-_\(\)\.]+)\.(\w+)")

# 'https://jpg.fish/a/finn.Hu6qp'
re_album_page = re.compile(
    r"(https?://)(\w+\.)?((jpg|pixl)\.(church|fish|li))(/(a|album)/)([\w\-_\(\)\.]+)")


class Jpg(Common):

    def __init__(self):
        self.tracker = Tracker.getInstance()

    async def run(self, url_dictionary: UrlDictionary) -> None:

        log.debug("Finding regex match")

        if re_album_page.match(url_dictionary['url']):
            log.debug("Found jpg album")
            await self.album_page(url_dictionary)

        elif re_image_page.match(url_dictionary['url']):
            log.debug("Found jpg image page")
            await self.image_page(url_dictionary)

        elif re_direct_image_link.match(url_dictionary['url']):
            log.debug("Found jpg image link")
            await self.direct_image_link(url_dictionary)

        else:
            log.info(f"No regex match found for link: {url_dictionary['url']}")
            await self.common_failed_attempt(url_dictionary.copy())

    async def call(self, url):

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=None, follow_redirects=True)

        except Exception:
            log.exception(f"Problem getting response: {url}")

        return response

    async def seek_date(self, response: httpx.Response) -> str:

        last_modified_date = datetime.strptime(response.headers.get(
            'last-modified'), "%a, %d %b %Y %H:%M:%S %Z")

        return last_modified_date.strftime('%Y-%m-%d+%H%%3A%M%%3A%S')

    async def direct_image_link(self, url_dictionary: UrlDictionary) -> None:

        async with sem:
            log.debug("Sending request to direct image link")

            # replace .md in the url to get the full size image instead of the
            # thumbnail

            url_dictionary['url'] = url_dictionary['url'].replace(".md", "")

            response = await self.call(url_dictionary['url'])

            # print(response.headers)
            url_dictionary['name'] = re_direct_image_link.match(
                url_dictionary['url']).group(8)
            url_dictionary['extension'] = response.headers.get('content-type')
            url_dictionary['url_to_download'] = url_dictionary['url']
            url_dictionary['file_size'] = response.headers.get(
                'content-length')
            url_dictionary['filename'] = self.common_filename_creator(
                url_dictionary)

            # print(url_dictionary)
            # await self.common_file_downloader(url_dictionary.copy())
            await self.tracker.add_url_dictionary(url_dictionary.copy())
            await self.common_advance_search_count(url_dictionary.copy())

    async def image_page(self, url_dictionary: UrlDictionary) -> None:

        response = await self.call(url_dictionary['url'])

        soup = BeautifulSoup(response.text, 'html.parser')
        image_container = soup.find('div', {'id': 'image-viewer-container'})
        image_link = image_container.find('img')

        url = image_link['src']
        url = url.replace(".md", "")
        url_dictionary['url'] = url

        # print(url_dictionary)
        await self.run(url_dictionary.copy())

    async def album_page(self, url_dictionary: UrlDictionary) -> None:

        url = url_dictionary['url']

        if url[-1] == '/':
            url = url[:-1]

        page = 1
        album_url = f"{url}/?sort=date_desc&page={page}"

        saved_links = []
        while True:

            log.info(f"Starting pass number {page}")
            log.info(f"Number of links found: {len(saved_links)}")

            response = await self.call(album_url)

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('div', {"class": "list-item"})

            if len(table) == 1:
                for link in table:
                    saved_links.append(link.find('img')['src'])
                log.info("Found page with only 1 image. Breaking loop")
                break

            for link in table:
                # print(link)
                saved_links.append(link.find('img')['src'])

            ids = [id['data-id'] for id in table]
            last_image_id = ids[-1]

            last_image_response = await self.call(saved_links[-1])
            seek_date = await self.seek_date(last_image_response)

            page += 1
            album_url = f"{url}/?sort=date_desc&page={page}&seek={seek_date}.{last_image_id}"

        saved_links = set(saved_links)

        log.debug(f"Total number of links found: {len(saved_links)}")

        tasks = []
        already_downloaded_urls = rat_info.get_downloaded_urls()
        log.debug("Attempting download of untracked links")
        for url in saved_links:
            url = url.replace(".md", "")

            if url in already_downloaded_urls and url_dictionary['download'] is True:
                continue

            else:
                url_dictionary['url'] = url
                tasks.append(asyncio.create_task(
                    self.run(url_dictionary.copy())))

        await asyncio.gather(*tasks)
