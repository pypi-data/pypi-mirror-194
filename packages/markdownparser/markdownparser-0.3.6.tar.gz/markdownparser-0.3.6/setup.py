# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdownparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'markdownparser',
    'version': '0.3.6',
    'description': '',
    'long_description': '# MarkdownParser\n\nMarkdownParser 是一个 Markdown 语法解析器,用于实现md到html标签的转换\n\n## 安装\n\n```bash\npip install markdownparser\n```\n\n## 快速使用\n\n```python\nimport MarkdownParser\n\nhtml = MarkdownParser.parse(\'# Hello World!\')\nprint(html)\n\n#<div class=\'markdown-body\'><h1>Hello World!</h1></div>\n```\n\n其他接口函数\n\n- `parseFile(file_name:str)->str`: 解析文件\n\n接口类\n\n- `Markdown`\n\n  使用类创建对象后可以利用 `self.preprocess_parser` `self.block_parser` `self.tree_parser` 控制解析过程\n\n  其中Block类属性见[base_class.py](MarkdownParser/base_class.py),可以通过调用block.info()函数查看树的结构\n\n  tree可以通过内部toHTML()方法得到HTML元素\n\n## 测试\n\n您可以使用 `test.py` 测试Markdown解析是否正确\n\n```bash\npython test.py <FILE_NAME>\n\n# python test.py ./testfiles/test1.md\n# python test.py README.md\n```\n\n运行会生成index.html, 使用浏览器打开生成的index.html即可与您的Markdown编辑器的预期渲染结果对比\n\n![20230218202400](https://raw.githubusercontent.com/learner-lu/picbed/master/20230218202400.png)\n\n## 实现思路\n\n[Markdown解析器的代码实现](https://www.bilibili.com/video/BV1LA411X7X3)\n\n您可通过取消 [core.py](./MarkdownParser/core.py) 注释来获取树的结构\n\n```python\ndef parse(self, text: str) -> str:\n\n    # 去除空行/注释/html标签\n    lines = self.preprocess_parser(text)\n    # print(lines)\n    # 逐行解析,得到一颗未优化的树\n    root = self.block_parser(lines)\n    # root.info()\n    # 优化,得到正确的markdown解析树\n    tree = self.tree_parser(root)\n    # tree.info()\n    # 输出到屏幕 / 导出html文件\n    return tree.toHTML()\n```\n\n## 不支持\n\n- 四个空格变为代码段\n- [^1]的引用方式\n- Setext 形式的标题\n- 上标 / 下标 / 下划线\n- TOC与锚点\n\n  锚点的添加通常和目录的跳转有关,而目录树的生成可以考虑解析tree的根Block的所有子HashHeaderBlock来构建.\n  \n  因为跳转的功能是js实现,锚点id的加入也会影响html结构,所以暂不支持\n\n## 补充说明\n\n- 生成的结果如下 `<div class=\'markdown-body\'>markdown内容</div>`\n- 代码段会根据语言加入一个类名便于后期高亮,例如 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`\n- 如果您想添加对[Mermaid](https://mermaid.js.org/)的支持, 您可参考[mermaid plugin](https://mermaid.js.org/intro/n00b-gettingStarted.html#_2-using-mermaid-plugins)在您的html页面 `<body>` 末尾添加如下 `<script>`\n\n  ```html\n  <script type="module">\n    const codeBlocks = document.querySelectorAll(\'.language-mermaid\');\n    codeBlocks.forEach(codeBlock => {\n        codeBlock.classList.remove(\'language-mermaid\');\n        codeBlock.classList.add(\'mermaid\');\n    });\n    import mermaid from \'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs\';\n    mermaid.initialize({ startOnLoad: true });\n  </script>\n  ```\n\n  > **请注意**, 由于本Markdown解析器的CodeBlock解析得到的类名为 `language-mermaid`, 而mermaid插件支持的类名格式为`mermaid`, 所以代码中手动修改了 `language-mermaid` 的类名\n\n- 如果您想添加对Latex数学公式的支持, 可以在html页面 `<body>` 末尾添加如下 `<script>`\n\n  ```html\n  <script>\n      MathJax = {\n        tex: {\n          inlineMath: [[\'$\', \'$\'], [\'\\\\(\', \'\\\\)\']]\n        }\n      };\n      </script>\n  <script id="MathJax-script" async\n  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">\n  </script>\n  ```\n\n  注意,这里仅支持\n\n## 相关参考\n\n- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)\n- [Mermaid API](https://mermaid.js.org/intro/#mermaid-api)\n- [MathJax](https://docs.mathjax.org/en/latest/web/start.html)',
    'author': 'luzhixing12345',
    'author_email': 'luzhixing12345@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luzhixing12345/MarkdownParser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
