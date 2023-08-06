from json import JSONDecodeError
from typing import Iterable, Union, Tuple, Any

import js2py
from bs4 import BeautifulSoup
import logging
import json

from js2py.base import JsObjectWrapper
from js2py.internals.simplex import JsException
from Selector import Selector
from MetaSelector import  MetaSelector


class SoupPage:
    _soup = None
    _html = None

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'lxml')

    def find(self, needle):
        """Function to find identifier of given needle"""
        assert type(needle) == str, "can only find strings, %s given" % type(needle)
        '''
        if 'http' in needle:
            text_matches = self._soup.find_all(attrs={"src": needle})
            if len(text_matches) == 0:
                text_matches = self._soup.find_all(attrs={"href": needle})
                logging.debug("Matches for %s: %s", needle, text_matches)
                tag_matches = [p for p in text_matches if extract_soup_href(p) == needle]
            else:
                logging.debug("Matches for %s: %s", needle, text_matches)
                tag_matches = [p for p in text_matches if extract_soup_img(p) == needle]

        else:
            text_matches = self._soup.find_all(text=re.compile(needle))
            logging.debug("Matches for %s: %s", needle, text_matches)
            text_parents = (ns.parent for ns in text_matches)
            tag_matches = [p for p in text_parents if extract_soup_text(p) == needle]
        return [SoupNode(m) for m in tag_matches]
        '''

    def select(self, selector: Selector):
        if selector.is_css_selector:
            return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in
                    self._soup.select(selector.get_name)]
        else:
            # Select info based on Selector inputs
            if selector.get_attr is None:
                data = self._soup.find_all(selector.get_name)
            elif selector.get_name != '':
                data = self._soup.find_all(selector.get_name, selector.get_attr)
            else:
                data = self._soup.find_all(attrs=selector.get_attr)
            # If selector name is script, we need to take only json info
            if selector.get_name == 'script':
                temp = []
                for res in data:
                    try:
                        json_data = js2py.eval_js(res.text)
                        if json_data is not None and type(json_data) == JsObjectWrapper:
                            temp.append(json_data.to_dict())
                    except JsException as e:
                        pass
                return temp
            else:
                return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in data]

    def meta_select(self, selector: MetaSelector):
        return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in
                self._soup.find_all('meta', {'name': selector.get_name})]

