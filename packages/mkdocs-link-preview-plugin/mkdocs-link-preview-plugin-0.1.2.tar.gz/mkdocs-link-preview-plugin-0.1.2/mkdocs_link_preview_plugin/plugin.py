from mkdocs.plugins import BasePlugin
from django.shortcuts import render

"""
A mkdocs plugin that support conversion from 
'obsidian syntax' to 'mkdocs-material syntax'
"""


class ObsidianSupportPlugin(BasePlugin):

    def on_page_markdown(self, markdown, page, config, files):
        ## apply conversions

        return render(None, 'polls/index.html', None)


