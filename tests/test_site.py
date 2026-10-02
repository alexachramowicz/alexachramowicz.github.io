"""Source-level portfolio regression checks; no third-party dependencies."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import os
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    """Collect HTML tags and attributes without opening a browser or following links."""
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        # HTMLParser calls this for each opening tag; comments are not collected.
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Read and parse the page once before running this class's tests."""
        cls.page = Page((ROOT / 'index.html').read_text(encoding='utf-8'))
        cls.ids = [attrs['id'] for _, attrs in cls.page.elements if 'id' in attrs]

    def assert_local_file(self, source, reference):
        """Check a local reference relative to its source file, including exact casing."""
        url = urlsplit(reference)
        if url.scheme or url.netloc or not url.path:
            return
        path = (ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else source.parent / unquote(url.path)
        path = Path(os.path.abspath(path))
        self.assertTrue(path.resolve().is_relative_to(ROOT), f'Asset escapes site root: {reference}')
        self.assertTrue(path.is_file(), f'Missing asset from {source.name}: {reference}')
        # Windows accepts mismatched casing; GitHub Pages runs on a case-sensitive filesystem.
        current = ROOT
        for part in path.relative_to(ROOT).parts:
            self.assertIn(part, [child.name for child in current.iterdir()], f'Incorrect asset casing: {reference}')
            current /= part

    def test_html_assets_exist_with_exact_casing(self):
        """Catch missing or incorrectly capitalized HTML images, scripts, and stylesheets."""
        for tag, attrs in self.page.elements:
            reference = attrs.get('src')
            if tag == 'link' and 'stylesheet' in attrs.get('rel', '').split():
                reference = attrs.get('href')
            if reference:
                with self.subTest(reference=reference):
                    self.assert_local_file(ROOT / 'index.html', reference)

    def test_css_assets_exist_with_exact_casing(self):
        """Check CSS url() assets, such as background images, relative to each stylesheet."""
        for source in (ROOT / 'styles').rglob('*.css'):
            css = re.sub(r'/\*.*?\*/', '', source.read_text(encoding='utf-8'), flags=re.S)
            for match in re.finditer(r'url\(\s*([\x27\x22]?)(.*?)\1\s*\)', css, re.S):
                reference = match.group(2).strip()
                with self.subTest(reference=reference):
                    self.assert_local_file(source, reference)

    def test_ids_are_unique(self):
        """Prevent ambiguous anchor targets and selectors by rejecting repeated HTML IDs."""
        duplicates = {key: count for key, count in Counter(self.ids).items() if count > 1}
        self.assertEqual({}, duplicates, f'Duplicate HTML IDs: {duplicates}')

    def test_internal_links_have_targets(self):
        """Check local linked files and same-page anchors; skip external websites."""
        for tag, attrs in self.page.elements:
            if tag != 'a':
                continue
            href = attrs.get('href', '')
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            if url.path:
                self.assert_local_file(ROOT / 'index.html', href)
            if url.fragment and url.path in ('', 'index.html', '/index.html'):
                with self.subTest(href=href):
                    self.assertIn(unquote(url.fragment), self.ids)

    def test_core_sections_and_navigation_remain_available(self):
        """Keep essential sections, their links, mobile metadata, and the stylesheet connected."""
        links = {attrs.get('href') for tag, attrs in self.page.elements if tag == 'a'}
        for section in ('profile', 'projects', 'contact'):
            with self.subTest(section=section):
                self.assertIn(section, self.ids)
                self.assertIn('#' + section, links)
        self.assertIn('about-para', self.ids)
        self.assertTrue(any(tag == 'meta' and attrs.get('name') == 'viewport'
                            for tag, attrs in self.page.elements), 'Missing mobile viewport metadata')
        self.assertTrue(any(tag == 'link' and attrs.get('href') == 'styles/main.css'
                            and 'stylesheet' in attrs.get('rel', '').split()
                            for tag, attrs in self.page.elements), 'Main stylesheet is disconnected')


if __name__ == '__main__':
    # Allows direct execution as well as discovery through python -m unittest.
    unittest.main()
