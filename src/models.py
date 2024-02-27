from uuid import uuid4
from typing import Set, List
class Image():
    def __init__(self, src: str):
        self._src = src

    
    
    @property
    def src(self):
        return self._src
        
    def to_string(self):
        return f'{self.src}'
    
    def __str__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.src)

    
class Link():
    def __init__(self, title: str, url: str, domain: str, path: str):
        self._title = title
        self._url = url
        self._domain = domain
        self._path = path
    
    @property
    def title(self):
        return self._title
    
    @property
    def url(self):
        return self._url
    
    @property
    def domain(self):
        return self._domain
    
    @property
    def path(self):
        return self._path
    
    def to_string(self):
        return f'{self.title} -> {self.url}'
    
    def __str__(self):
        return self.to_string()
    
    def __hash__(self):
        return hash(self.url)
    
class Paragraph():
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def to_string(self):
        return f'{self.value}'
    
    def __str__(self):
        return self.to_string()
    
    def __hash__(self):
        return hash(self.value)


class Content():
    def __init__(self, title: str):
        self._title = title
        if title:
            self._u_id = title
        else:
            self._u_id = uuid4()
    
        self._paragraphs = {}
        self._links = {}
        self._images = {}

    @property
    def u_id(self):
        return self._u_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def paragraphs(self):
        return self._paragraphs
    
    def add_paragraph(self, paragraph: str):
        self._paragraphs[hash(paragraph)] = paragraph

    @property
    def links(self):
        return self._links
    
    def add_link(self, link: Link):
        self._links[hash(link)] = link

    def get_links(self) -> List[Link]:
        return self._links.values()

    @property
    def images(self):
        return self._images
    
    def add_image(self, image: Image):
        self._images[hash(image)] = image

    def has_content(self):
        return len(self.paragraphs) > 0 or len(self.links) > 0 or len(self.images) > 0 
    
    def to_string(self):
        out_str_arr = ['\r\n\tContent:']
        out_str_arr.append(f'\t\ttitle: {self.title}')
        out_str_arr.append(f'\t\tparagraphs:')
        for paragraph in self.paragraphs.values():
            out_str_arr.append(f'\t\t\t{paragraph.to_string()}')
        
        out_str_arr.append(f'\t\tlinks:')
        for link in self.links.values():
            out_str_arr.append(f'\t\t\t{link.to_string()}')

        out_str_arr.append(f'\t\timages')
        for image in self.images.values():
            out_str_arr.append(f'\t\t\t{image.to_string()}')
        return '\r\n'.join(out_str_arr)
    
    def __str__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.u_id)

class Page():
    def __init__(self, url:str, path: str):
        self._url = url
        self._path = path
        self._contents = {}

    @property
    def url(self):
        return self._url
    
    @property
    def path(self):
        return self._path
    
    @property
    def contents(self):
        return self._contents

    def add_content(self, content: Content):
        self._contents[hash(content)] = content

    def get_links(self) -> List[Link]:
        links = set()

        # Return unique Links
        for content in self.contents.values():
            links |= set(content.get_links())
        return list(links)

    def to_string(self):
        out_str_arr = ['\r\nPage:']
        out_str_arr.append(f'url: {self.url}')
        out_str_arr.append(f'path: {self.path}')
        for item in self._contents.values():
            out_str_arr.append(item.to_string())
        return '\r\n'.join(out_str_arr)
    
    def __str__(self):
        return self.to_string()
    
    def __hash__(self):
        return hash(self.url)

class Website():
    def __init__(self, url: str, domain: str):
        self._url = url
        self._domain = domain
        self._pages = {}

    @property
    def url(self):
        return self._url
    
    @property
    def domain(self):
        return self._domain

    @property
    def pages(self):
        return self._pages

    def add_page(self, page: Page):
        if page.path in self._pages:
            raise ValueError(f'Page exsist, path={page.path}')

        self._pages[hash(page)] = page

    def has_page(self, url: str, path: str):
        return Page(url, path) in self._pages

    def to_string(self):
        out_str_arr = ['==========Website============']
        out_str_arr.append(f'url: {self.url}')
        out_str_arr.append(f'domain: {self.domain}')
        for page in self.pages.values():
            out_str_arr.append(page.to_string())
        return '\r\n'.join(out_str_arr)

    def __str__(self):
        return self.to_string()


