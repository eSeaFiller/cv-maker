# -*- coding: utf-8 -*-
"""把 src/source.html 和 pdf.js 打包成根目录那个可以直接双击打开的 cv-maker.html。

source.html 是正文片段（没有 doctype / <html> / <head>），这里负责两件事：
  1. 把 pdf.js 内联进去 —— 工具要在断网、file:// 下也能解析 PDF，就不能留外部依赖；
  2. 包上 doctype 和 head。

用法：python3 src/build.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ANCHOR = '<script>\n(function(){\n  "use strict";'

HEADER = ('<!--\n  CV Maker — 简历制作器\n  Copyright (c) 2026 XuJianghao\n  Released under the MIT License — https://github.com/eSeaFiller/cv-maker\n  内联的 pdf.js 版权归 Mozilla Foundation 所有，遵循 Apache License 2.0。\n-->\n')


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    src = read(os.path.join(HERE, "source.html"))
    worker = read(os.path.join(HERE, "pdfjs", "pdf.worker.min.js"))
    main_js = read(os.path.join(HERE, "pdfjs", "pdf.min.js"))

    # 内联的脚本里出现 </script 会提前关掉标签，打包前先确认没有
    assert "</script" not in worker and "</script" not in main_js
    assert ANCHOR in src, "source.html 里找不到脚本锚点，检查它有没有被改过"

    libs = (
        "<script>/* pdf.js 3.11.174 worker (inlined; runs on the main thread) */\n"
        + worker
        + "\n</script>\n<script>/* pdf.js 3.11.174 */\n"
        + main_js
        + "\n</script>\n"
    )
    body = src.replace(ANCHOR, libs + ANCHOR, 1)

    page = (
        '<!doctype html>\n' + HEADER +
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )

    out = os.path.join(ROOT, "cv-maker.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("built %s (%.1f MB)" % (out, len(page.encode("utf-8")) / 1048576))


if __name__ == "__main__":
    main()
