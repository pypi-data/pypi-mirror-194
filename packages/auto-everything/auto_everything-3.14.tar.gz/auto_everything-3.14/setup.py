# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_everything', 'auto_everything.x11']

package_data = \
{'': ['*'], 'auto_everything.x11': ['example/*']}

install_requires = \
['fire>=0.5.0,<0.6.0', 'psutil>=5.9.4,<6.0.0']

entry_points = \
{'console_scripts': ['hi = auto_everything.terminal:_hi']}

setup_kwargs = {
    'name': 'auto-everything',
    'version': '3.14',
    'description': 'do automate things on Linux',
    'long_description': '# auto_everything\n\nLinux automation\n\n#### Donation\n\n[<img src="https://github.com/yingshaoxo/yingshaoxo/raw/master/become_a_patron_button.png" width="200">](https://www.patreon.com/bePatron?u=45200693)\n\n#### Installation (For Python >= 3.10)\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3\npoetry add auto_everything\n\nor\n\nsudo pip3 install auto_everything\n```\n\n> Full Installation: `poetry install --with all`\n\n#### Installation (For 3.5 <= Python < 3.10)\n\n```bash\npoetry add auto_everything==3.9\n\nor\n\nsudo pip3 install auto_everything==3.9\n```\n\n#### Magic\n\n```bash\ncurl -sSL https://github.com/yingshaoxo/auto_everything/raw/master/env_setup.sh | bash\n\nwget -O - https://github.com/yingshaoxo/auto_everything/raw/master/example/install_YouCompleteMe.py | python3\n```\n\n#### Docs\n\nhttps://yingshaoxo.github.io/auto_everything\n\n---\n\n## Basic API\n\n#### Import\n\n```python\nfrom auto_everything.terminal import Terminal\nt = Terminal()\n```\n\n#### Run a command and get reply\n\n```python\nreply = t.run_command(\'uname -a\')\nprint(reply)\n```\n\n#### Run commands and get direct screen output\n\n```python\ncommands = """\nsudo apt update\nuname -a\n"""\nt.run(commands)\n```\n\n#### Run a program\n\n```python\nt.run_program(\'firefox\')\n```\n\n#### Run a python script\n\n```python\nt.run_py(\'your_file.py\')\n```\n\n#### Run a bash script\n\n```python\nt.run_sh(\'your_file.sh\')\n```\n\n#### Detect if a program or script is running\n\n```python\nstatus = t.is_running(\'terminal\')\nprint(status)\n```\n\n#### Kill it\n\n```python\nt.kill(\'terminal\')\n```\n\n---\n\n## For simplify Python development\n\n#### Import\n\n```python\nfrom auto_everything.python import Python\npy = Python()\n```\n\n#### Turn `Python Class` into a `Command Line Program`\n\n```python\npy.fire(your_class_name)\n```\n\n#### Make it `global executable`:\n\n```python\npy.make_it_global_runnable(executable_name="Tools")\n```\n\n#### Example\n\nLet\'s assume you have a file named `Tools.py`:\n\n```python\nfrom auto_everything.base import Python\npy = Python()\n\nclass Tools():\n    def push(self, comment):\n        t.run(\'git add .\')\n        t.run(\'git commit -m "{}"\'.format(comment))\n        t.run(\'git push origin\')\n\n    def pull(self):\n        t.run("""\ngit fetch --all\ngit reset --hard origin/master\n""")\n\n    def undo(self):\n        t.run("""\ngit reset --mixed HEAD~1\n""")\n\n    def reset(self):\n        t.run("""\ngit reset --hard HEAD^\n""")\n\n    def hi(self):\n        print("Hi, Python!")\n\npy.fire(Tools)\npy.make_it_global_runnable(executable_name="MyTools")\n```\n\nAfter the first running of this script by `python3 Tools.py hi`, you would be able to use `MyTools` to run this script at anywhere within your machine:\n\n```bash\nyingshaoxo@pop-os:~$ MyTools hi\nHi, Python!\n\n```\n\n---\n\n## Others\n\n#### Web automation\n\n```python\nfrom auto_everything.web import Selenium\nfrom time import sleep\n\nmy_selenium = Selenium("https://www.google.com", headless=False)\nd = my_selenium.driver\n\n# get input box\nxpath = \'//*[@id="lst-ib"]\'\nelements = my_selenium.wait_until_exists(xpath)\n\n# text inputing\nelements[0].send_keys(\'\\b\' * 20, "yingshaoxo")\n\n# click search button\nelements = my_selenium.wait_until_exists(\'//input[@value="Google Search"]\')\nif len(elements):\n    elements[0].click() # d.execute_script("arguments[0].click();", elements[0])\n\n# exit\nsleep(30)\nd.quit()\n```\n\n#### Simpler IO\n\n```python\nfrom auto_everything.base import IO\nio = IO()\n\nio.write("hi.txt", "Hello, world!")\nprint(io.read("hi.txt"))\n\nio.append("hi.txt", "\\n\\nI\'m yingshaoxo.")\nprint(io.read("hi.txt"))\n```\n\n#### Quick File Operation\n\n```python\nfrom auto_everything.disk import Disk\nfrom pprint import pprint\ndisk = Disk()\n\nfiles = disk.get_files(".")\nfiles = disk.sort_files_by_time(files)\npprint(files)\n```\n\n#### Easy Store\n\n```python\nfrom auto_everything.disk import Store\nstore = Store("test")\n\nstore.set("author", "yingshaoxo")\nstore.set("author", {"email": "yingshaoxo@gmail.com", "name": "yingshaoxo"})\nprint(store.get_items())\n\nprint(store.has_key("author"))\nprint(store.get("author", ""))\nprint(store.get("whatever", default_value="alsjdasdfasdfsakfla"))\n\nstore.reset()\nprint(store.get_items())\n```\n',
    'author': 'yingshaoxo',
    'author_email': 'yingshaoxo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
