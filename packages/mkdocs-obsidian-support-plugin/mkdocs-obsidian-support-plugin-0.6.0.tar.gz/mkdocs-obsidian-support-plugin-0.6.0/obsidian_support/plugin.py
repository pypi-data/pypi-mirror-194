from mkdocs.plugins import BasePlugin

from obsidian_support.conversion.admonition import AdmonitionConvert
from obsidian_support.conversion.image_link import ImageLinkConvert
from obsidian_support.markdown_convert import markdown_convert

"""
A mkdocs plugin that support conversion from 
'obsidian syntax' to 'mkdocs-material syntax'
"""


class ObsidianSupportPlugin(BasePlugin):

    def on_page_markdown(self, markdown, page, config, files):
        ## apply conversions
        markdown = markdown_convert(markdown, AdmonitionConvert())
        markdown = markdown_convert(markdown, ImageLinkConvert())

        return markdown

