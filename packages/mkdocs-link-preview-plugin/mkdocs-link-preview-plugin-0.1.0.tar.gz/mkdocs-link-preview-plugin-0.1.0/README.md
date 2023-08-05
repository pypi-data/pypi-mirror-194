# mkdocs-obsidian-support-plugin
---
Plugin for [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) provide external link preview.

[![PyPI](https://img.shields.io/pypi/v/mkdocs-link-preview-plugin)](https://pypi.org/project/mkdocs-link-preview-plugin/)
[![GitHub](https://img.shields.io/github/license/ndy2/mkdocs-link-preview-plugin)](https://github.com/ndy2/mkdocs-link-preview-plugin/blob/main/LICENSE.md)

```text
pip install mkdocs-link-preview-plugin
```

## Usage
Activate the plugin in mkdocs.yml 
```yaml
plugins:
  - link-preview
```

## Feature
It converts below codeblock syntax to preview-html based on [The Open Graph Protocol](https://ogp.me/).

````
```preview
https://github.com/ndy2/mkdocs-link-preview-plugin
```
````



