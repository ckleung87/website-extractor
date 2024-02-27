import os
import unittest
from unittest.mock import patch, Mock
import logging
from services import WebsiteExtractor

class WebsiteExtractorTest(unittest.TestCase):

    def setUp(self):


        ENV = 'TEST'
        SERVICE_NAME = os.getenv('SERVICE_NAME', 'UNKNOWN')
        VERSION = os.getenv('VERSION', '0.0.0')

        self.logger = logging.getLogger('app')

        log_formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s][{0}][{1}][{2}] %(message)s'.format(SERVICE_NAME, VERSION, ENV), '%Y-%m-%dT%H:%M:%S')
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

        self.logger.setLevel(logging.DEBUG)

    @patch('services.WebsiteExtractor._extract_page_link_content')
    @patch('services.WebsiteExtractor._fetch_page_content')
    def test_extract_mock_1(self, fetch_mock_fn, extract_link_mock_fn):
        # arrange
        url = 'mock_1_test'
        config = {
            'recursive_level_limit': 0,
            'extract_page_sleep_sec': 1,
        }
        # Mock _fetch_page_content return mock data
        with open('./mock/mock_1.html') as fp:
            fetch_mock_fn.return_value  = fp.read()

        extractor = WebsiteExtractor(url, self.logger, config)

        # action
        extractor.extract()

        # assert
        self.assertEqual(len(extractor.website.pages), 1)

        page = list(extractor.website.pages.values())[0]
        self.assertEqual(len(page.contents), 6)
        self.assertEqual(len(page.get_links()), 17)

        fetch_mock_fn.assert_called_once()
        extract_link_mock_fn.assert_called_once()

    @patch('services.WebsiteExtractor._extract_page_link_content')
    @patch('services.WebsiteExtractor._fetch_page_content')
    def test_extract_mock_2(self, fetch_mock_fn, extract_link_mock_fn):
        # arrange
        url = 'mock_2_test'
        config = {
            'recursive_level_limit': 0,
            'extract_page_sleep_sec': 1,
        }
        # Mock _fetch_page_content return mock data
        with open('./mock/mock_2.html') as fp:
            fetch_mock_fn.return_value  = fp.read()

        extractor = WebsiteExtractor(url, self.logger, config)

        # action
        extractor.extract()

        # assert
        self.assertEqual(len(extractor.website.pages), 1)

        page = list(extractor.website.pages.values())[0]
        self.assertEqual(len(page.contents), 6)
        self.assertEqual(len(page.get_links()), 12)

if __name__ == "__main__":
    unittest.main()