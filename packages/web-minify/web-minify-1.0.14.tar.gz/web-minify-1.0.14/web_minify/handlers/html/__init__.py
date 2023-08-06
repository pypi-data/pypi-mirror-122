#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML Minifier functions for CSS-HTML-JS-Minify."""

import re
import logging

from .html import html_minify

logger = logging.getLogger(__name__)


class Handler:
    """HTML handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["html", "htm"]

    @classmethod
    def name(self):
        return "html"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return html_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
