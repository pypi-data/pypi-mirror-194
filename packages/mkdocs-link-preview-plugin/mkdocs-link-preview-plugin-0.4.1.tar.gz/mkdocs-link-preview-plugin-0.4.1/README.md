# mkdocs-obsidian-support-plugin
---
Plugin for [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) provide external link preview.

[![PyPI](https://img.shields.io/pypi/v/mkdocs-link-preview-plugin)](https://pypi.org/project/mkdocs-link-preview-plugin/)

```text
pip install beautifulsoup4
pip install mkdocs-link-preview-plugin
```

It requires beautifulsoup4 for crawling the open grapth protocol metadata.

## Usage
Activate the plugin in mkdocs.yml 
```yaml
plugins:
  - link-preview
  
extra_css:
  - path/to/link-preview.css
```

## Feature
It converts below codeblock syntax to preview-html based on [The Open Graph Protocol](https://ogp.me/).

````
```preview
https://github.com/ndy2/mkdocs-link-preview-plugin
```
````

rendered as

![image](https://user-images.githubusercontent.com/67302707/221235406-38958e37-2031-4f65-828f-ef41cfa2395a.png)

with default css configuration.

- super simple demo link - https://ndy2.github.io/mkdocs-link-preview-plugin/

### Inspired by
- https://github.com/dhamaniasad/obsidian-rich-links



