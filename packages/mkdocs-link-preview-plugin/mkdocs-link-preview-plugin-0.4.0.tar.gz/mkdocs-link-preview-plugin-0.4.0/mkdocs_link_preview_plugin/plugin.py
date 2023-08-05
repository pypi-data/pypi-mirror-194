import re
import pkgutil

from mkdocs.plugins import BasePlugin

from mkdocs_link_preview_plugin.opengraph import OpenGraph


class LinkPreviewPlugin(BasePlugin):
    PREVIEW_CODEBLOCK_PATTERN = re.compile("```preview\n(?P<content>[\\s\\S]+?)\n```")

    def __init__(self):
        self.opengraph = OpenGraph()
        self.url_pattern = re.compile(
            "^((http|https)?://)?(?P<host>[a-zA-Z0-9./?:@\\-_=#]+\\.[a-zA-Z]{2,6})[a-zA-Z0-9.&/?:@\\-_=#가-힇]*$")
        self.fallback_template = None
        self.preview_template = None

    def on_config(self, config):
        self.preview_template = pkgutil.get_data(__name__, "resources/preview.html").decode('utf-8')
        self.fallback_template = pkgutil.get_data(__name__, "resources/fallback.html").decode('utf-8')
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
                line = line.replace(" ", "")
                if line[0] == "-" or line[0] == "*":
                    line = line[1:]
                try:
                    soup = self.opengraph.get_page(line)
                    preview_html = self.preview_template
                    link = line

                    image_url = self.opengraph.get_og_image(soup)
                    title = self.opengraph.get_og_site_name(soup)
                    description = self.opengraph.get_og_description(soup)

                    if image_url is None:
                        image_url = ""
                    if title is None:
                        title = ""
                    if description is None:
                        description = ""

                    preview_html = preview_html.replace("{{ link }}", link)
                    preview_html = preview_html.replace("{{ image-url }}", image_url)
                    preview_html = preview_html.replace("{{ title }}", title)
                    preview_html = preview_html.replace("{{ description }}", description)
                    preview_htmls += preview_html

                ## open graph metadata not found
                except:
                    url_match = self.url_pattern.match(line)
                    if url_match:
                        title = url_match.group('host')
                    else:
                        title = "no url provided"
                    fallback_html = self.fallback_template
                    fallback_html = fallback_html.replace("{{ link }}", line)
                    fallback_html = fallback_html.replace("{{ title }}", title)

                    preview_htmls += fallback_html

            converted_markdown += markdown[index:start]
            converted_markdown += preview_htmls
            index = end + 1

        converted_markdown += markdown[index:len(markdown)]
        return converted_markdown
