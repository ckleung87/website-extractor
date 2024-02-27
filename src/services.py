import requests
from logging import Logger, getLogger
from time import sleep
from bs4 import BeautifulSoup
from bs4.element import Tag
from models import Website, Page, Content, Paragraph, Link, Image
from utils import get_webpage_domain, get_webpage_path

class WebsiteExtractor():

    def __init__(self, url: str, logger: Logger = None, config: dict = {}):
        self.logger = logger if logger else getLogger('WebsiteExtractor')

        self._website = Website(url, get_webpage_domain(url))
        
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })

        self.recursive_level_limit = config.get('recursive_level_limit', 1)
        self.extract_page_sleep_sec = config.get('extract_page_sleep_sec', 0.1)

    @property
    def website(self):
        return self._website
             
    def _fetch_page_content(self, url):
        try:
            res = self._session.get(url)
            return res.text
        except Exception as e:
            return None
         
    def _extract_content(self, html_content: Tag):

        title = ''
        title_level = 6
        for heading in html_content.find_all(['h1', 'h2', 'h3','h4', 'h5', 'h6']):
            level = int(heading.name[1])
            if level < title_level:
                title_level = level
                title = heading.text

        content_ins = Content(title)

        # Extract <p> tag -> Paragraph
        for paragraph in html_content.find_all('p'):
            # filter out empty paragraph
            if len(paragraph.text.strip()) == 0 :
                continue
            content_ins.add_paragraph(Paragraph(paragraph.text))

        # Extract <a> tag -> Link
        for link in html_content.find_all('a'):
            url = link.get('href', None)
            if url:
                content_ins.add_link(Link(link.get_text(), url, get_webpage_domain(url), get_webpage_path(url)))

        # Extract <img> tag -> Image
        for img in html_content.find_all('img'):
            src = ''
            if img.has_attr('src') and img['src']:
                src = img['src']

            # overriden the src if it is lazy loading
            if img.has_attr('data-lazy-src') and img['data-lazy-src']:
                src = img['data-lazy-src']
            
            if src:
                content_ins.add_image(Image(src))

        # Extract div tag with image class -> Image
        for img in html_content('div', {'class':['image']}):
            src = ''
            if img.has_attr('data-bg') and img['data-bg']:
                src = img['data-bg']

            # overriden the src if it is lazy loading
            if img.has_attr('data-lazy-src') and img['data-lazy-src']:
                src = img['data-lazy-src']
            
            if src:
                content_ins.add_image(Image(src))

            
        return content_ins
    
    def _extract_page_link_content(self, domain:str, page: Page, recursive_level: int = 0):
        # Get page link which is in the same domain and not process before
        next_process_pages = set(filter(lambda l: (l.domain == domain), page.get_links()))
        self.logger.info(f'_extract_page_content complete: {len(next_process_pages)} more links - level={recursive_level}, url={page.url}')
        for l in next_process_pages:
            if self.website.has_page(l.url, l.path):
                continue

            self._extract_page_content(domain, l.url, recursive_level + 1)

    
    def _extract_page_content(self, domain:str, url: str, recursive_level:int = 0):
        self.logger.info(f'_extract_page_content start - level={recursive_level}, url={url}')
        if recursive_level > self.recursive_level_limit:
            self.logger.info(f'_extract_page_content complete: Reach Recursive Limit - level={recursive_level}, url={url}')
            return
        
        if self.website.has_page(url, get_webpage_path(url)):
            self.logger.info(f'_extract_page_content complete: Extracted Before - level={recursive_level}, url={url}')
            return
        
        html_content = self._fetch_page_content(url)
        if not html_content:
            self.logger.info(f'_extract_page_content complete: No Content - level={recursive_level}, url={url}')
            return

        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')

        page = Page(url, get_webpage_path(url))

        contents = body.find_all('div', {'class':['content','container']})
        for item in contents:
            item_class_set = set(item['class'])

            if item.parent and item.has_attr('class'):
                # filter out nested tag with the same class
                item_parent_class_set = set(item.parent['class'])
                if len(item_class_set.intersection(item_parent_class_set)) > 0:
                    continue

            ins = self._extract_content(item)
            if ins.has_content():
                page.add_content(ins)

        self.website.add_page(page)
        self._extract_page_link_content(domain, page, recursive_level)
        return
    
    def extract(self):
        self.logger.info(f'Extract Start: url={self.website.url}')
        self._extract_page_content(self.website.domain, self.website.url)
        self.logger.info(f'Extract Completed: url={self.website.url}')
        self.logger.info(self.website)