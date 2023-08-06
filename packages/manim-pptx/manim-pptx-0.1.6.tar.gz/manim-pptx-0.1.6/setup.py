# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_pptx']

package_data = \
{'': ['*']}

install_requires = \
['lxml', 'manim', 'python-pptx']

setup_kwargs = {
    'name': 'manim-pptx',
    'version': '0.1.6',
    'description': '',
    'long_description': '# MANIM-PPTX\n\nA Manim addon which exports the video as a powerpoint\n\n## Table of Contents\n\n-  [Installation](#installation)\n-  [Usage](#usage)\n    -  [Example](#example)\n-  [Contributing](#contributing)\n-  [Credit](#credit)\n\n## Installation\n\n> ``pip install manim-pptx``\n\n## Usage\n\nTo export as pptx make your scene class inherit from `PPTXScene`\n\nYou can then call `self.endSlide()` to add all animations since the last `endSlide()`.\n\nThe `endSlide` method has also two arguments:\n\n- `loop` - loops the whole Slide.\n- `autonext` - automatically advances to the next slide when the current slide is done animating\n- `notes` - notes which should be displayed on the created Slide\n- `shownextnotes` - show the notes of the next slide in the notes of the current slide\n\n### Example\n\n```python\nfrom manim_pptx import *\nfrom manim import *\n\nclass TestScene(PPTXScene):\n    def construct(self):\n\n        t = Tex("Hello World!")\n        self.play(Write(t, run_time=2))\n        self.endSlide()\n        \n        c = Circle(radius=3)\n        self.play(Create(c))\n        d = Dot()\n        d.move_to(c.get_start())\n        self.play(Write(d))\n        self.endSlide(autonext=True, shownextnotes=True)\n\n        self.play(MoveAlongPath(d, c))\n        self.endSlide(loop=True, notes="Next Animation displays Bye")\n\n        self.play(*[FadeOut(m) for m in self.mobjects])\n\n        t2 = Tex("Bye!")\n        self.play(Write(t2, run_time=1))\n        self.endSlide()\n```\n\n## Contribution\n\nFeel free to contribute and create pull requests.\n\n## Credit\nCredit to both [manim-presentation](https://github.com/galatolofederico/manim-presentation) and [manim-pptx](https://github.com/yoshiask/manim-pptx) where i stole some good ideas and a bit of code',
    'author': 'RythenGlyth',
    'author_email': 'rythenglyth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
