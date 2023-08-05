import re

from mkdocs.plugins import BasePlugin

from mkdocs_link_preview_plugin.opengraph import OpenGraph


class LinkPreviewPlugin(BasePlugin):
    PREVIEW_CODEBLOCK_PATTERN = re.compile("```preview\n(?P<content>[\\s\\S]+?)\n```")

    def __init__(self):
        self.opengraph = OpenGraph()
        self.preview_template = None

    def on_config(self, config):
        template_file = open("mkdocs_link_preview_plugin/template/preview.html", 'r')
        self.preview_template = template_file.read()
        template_file.close()
        return config

    def on_page_markdown(self, markdown, page, config, files):
        converted_markdown = ""
        index = 0
        for preview in self.PREVIEW_CODEBLOCK_PATTERN.finditer(markdown):
            start = preview.start()
            end = preview.end() - 1

            content = preview.group("content")
            lines = content.splitlines()

            preview_htmls = ""
            for line in lines:
                line.replace(" ", "")
                if line[0] == "-" or line[0] == "*":
                    line = line[1:]
                soup = self.opengraph.get_page(line)

                print("line : ")
                print(line)

                preview_html = self.preview_template
                preview_html = preview_html.replace("{{ link }}", line)
                preview_html = preview_html.replace("{{ image-url }}", self.opengraph.get_og_image(soup))
                preview_html = preview_html.replace("{{ title }}", self.opengraph.get_og_site_name(soup))
                preview_html = preview_html.replace("{{ description }}", self.opengraph.get_og_description(soup))

                preview_htmls += preview_html

            converted_markdown += markdown[index:start]
            converted_markdown += preview_htmls
            index = end + 1

        converted_markdown += markdown[index:len(markdown)]
        return converted_markdown
