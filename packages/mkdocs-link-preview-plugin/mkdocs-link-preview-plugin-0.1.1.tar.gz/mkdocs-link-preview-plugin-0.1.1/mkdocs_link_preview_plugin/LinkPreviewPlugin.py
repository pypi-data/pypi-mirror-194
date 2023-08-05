from mkdocs.plugins import BasePlugin

"""
A mkdocs plugin that support conversion from 
'obsidian syntax' to 'mkdocs-material syntax'
"""


class ObsidianSupportPlugin(BasePlugin):

    def on_page_markdown(self, markdown, page, config, files):
        ## apply conversions
        return "i eat all"


