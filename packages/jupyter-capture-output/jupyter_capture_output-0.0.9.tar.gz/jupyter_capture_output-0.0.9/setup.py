# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_capture_output']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0', 'ipykernel>=5.0.0', 'ipython>=6.0.0']

setup_kwargs = {
    'name': 'jupyter-capture-output',
    'version': '0.0.9',
    'description': 'Capture output from JupyterLab',
    'long_description': '# jupyter-caputure-output\nA cell magic that captures jupyter cell output\n\n\n[![JupyterLight](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://octoframes.github.io/jupyter_capture_output/)  \n\n## Install\nRequires Python >=3.8\n```py\npip install jupyter_capture_output\n```\n\n\n## Example\n\nhttps://user-images.githubusercontent.com/44469195/199723257-ee428f53-d576-47be-93b9-d6ab98c46d8e.mov\n\n```py\nimport jupyter_capture_output\n```\n\n```py \n%%capture_text --path "foo.txt"\nprint("Hello World")\n```\n\n```py\nimport matplotlib.pyplot as plt\n```\n\n```py\n%%capture_img --path "foo.png bar.png"\nplt.plot([1,2],[10,20])\nplt.show()\nplt.plot([3,4],[-10,-20])\nplt.show()\n```\n\n```py\n%%capture_img  --path "foo.jpg bar.jpg" --compression 50\nplt.plot([1,2],[10,20], color = "r")\nplt.show()\nplt.plot([3,4],[-10,-20],color = "r")\nplt.show()\n```\n\n\n\nImplemented\n* `%%capture_text`  ->  to .txt file with text output\n* `%%capture_code`  ->  to .py file with cell content\n* `%%capture_img` -> to .png or .jpg with image output\n* `%%capture_video` -> to .mp4 file with the video output\n\n## Use cases\n\n* matplotlib, scipy, PIL , cv2, manim etc. have their own APIs to save images. With this package, one just have to learn one line of code and can use it to save all kind of image outputs made by different packages.\n\n* When tweaking plots, one can use this cell magic to track the process, so to say a visual version control system.\n\n* In context of Science, one can generate log files of experiments with this package. As the cell magic is always on the top of the cell, it\'s easy to see in which cells log files are generated and in which not.\n\n* This can be used to create sheet cheats, e.g. this [math-functions-cheat-sheet](https://kolibril13.github.io/plywood-gallery-functions/) website was generated from a jupyter notebook using a derivative of this capture package.\n\n* This package will also auto-generate the folder-tree of subdirectories for you.\n## Changelog\n\n\n### 0.0.9\n\n* support python 3.11\n### 0.0.8 \n*  Add `capture_code` magic. Because this is not cell output but cell content, it might be worth to think about renaming this project from `capture-output` to only `capture` or even `capture-content`.\n* `remove experimental_capture_video_first_last` and `experimental_video_thumbnail` again. This package is not the right place for that.\n\n### 0.0.7 \n\n* Add relative path support and automatically create paths if they don\'t exist yet.\n\nAdd some experimental magic, but this will likely be removed in future versions:\n* * `experimental_capture_video_first_last` captures video and extracts first and last frame from it. Useful for post-processing of videos in other video editors. Needs ffmpeg installed\n\n* `experimental_video_thumbnail` extracts video from the Jupyter cell output, and replaces it with an image thumbnail of the video -> useful for Version control. Needs matplotlib and ffmpeg installed\n### 0.0.6\n\nbetter regex in capture video\nchange example images to dogs\n\n### 0.0.5\n\nRemove debugging code\nAdd JupyterLiteDemo\n### 0.0.4\n\nAdd Text and Video capture cell magic\nupdate example\n\n### 0.0.3\n\nSetup automatic release action.\n\n### 0.0.2\n\nUpdate example\n\n### 0.0.1\n\nInitial release\n',
    'author': 'kolibril13',
    'author_email': '44469195+kolibril13@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.14',
}


setup(**setup_kwargs)
