# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['editor']
install_requires = \
['runs>=1.1.0,<2.0.0', 'xmod>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'editor',
    'version': '1.3.0',
    'description': '🖋 Open the default text editor 🖋',
    'long_description': "`editor` opens a text editor for an existing file, a new file, or a tempfile,\nblocks while the user edits text, then returns the results.\n\nYou can specify a command line that runs the editor, but usually you leave it\nempty - in that case, `editor` uses the  the command line from the environment\nvariable `VISUAL`, or if that's empty, the environment variable `EDITOR`, or if\n*that's* empty, either `Notepad` on Windows or `vi` elsewhere.\n\n### Example 1: Using a temporary file\n\nIf no filename is provided, a temporary file gets edited, and its contents\nreturned.\n\n\n    import editor\n\n    MESSAGE = 'Insert comments below this line\\n\\n'\n    comments = editor(text=MESSAGE)\n    # Pops up the default editor with a tempfile, containing MESSAGE\n\n### Example 2: Using a named file\n\nIf a filename is provided, then it gets edited!\n\n    import os\n\n    FILE = 'file.txt'\n    assert not os.path.exists(FILE)\n\n    comments = editor(text=MESSAGE, filename=FILE)\n    # Pops up an editor for new FILE containing MESSAGE, user edits\n\n    assert os.path.exists(FILE)\n\n    # You can edit an existing file too, and select your own editor.\n    comments2 = editor(filename=FILE, editor='emacs')\n\n\n### [API Documentation](https://rec.github.io/editor#editor--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
