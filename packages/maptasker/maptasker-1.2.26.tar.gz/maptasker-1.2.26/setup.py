# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maptasker', 'maptasker.src']

package_data = \
{'': ['*']}

install_requires = \
['ctkcolorpicker>=0.3.0,<0.4.0',
 'customtkinter>=5.1.2,<6.0.0',
 'pillow>=9.4.0,<10.0.0']

entry_points = \
{'console_scripts': ['maptasker = maptasker.main:main']}

setup_kwargs = {
    'name': 'maptasker',
    'version': '1.2.26',
    'description': "Utility to display your Android 'Tasker' configuration on your MAC.",
    'long_description': '# MapTasker\n## Display the Tasker Project/Profile/Task/Scene hierarchy on a MAC based on Tasker\'s backup.xml\n\nThis is an application in support of [Tasker](https://tasker.joaoapps.com/) that is intended to run on a MAC.\n \nI found that my Tasker Projects/Profiles/Tasks/Scenes were becoming unmanageable, so I wrote a Python program for my MAC to provide an indented list of my entire configuration based on my Tasker backup XML file that I save to my Google Drive.\n \nA portion/example of the results can be found at https://imgur.com/a/KIR7Vep.\n \n### Program Dependencies\n-\tPython version v3.10 or higher and Tkinter (not included with Python 3.10 from \'brew\')            \n\n\n    python 3.10: `brew install python3.10`          \n    Tkinter:     `brew install python-tk@3.10`           \n     \n-\tTasker full or partial backup.xml (anyname.xml…you will be prompted to locate and identify your Tasker backup xml file) on your MAC, created by Tasker version 5 or version 6. \n\n\n### Installation\n\n- Install maptasker by entering the following command into Terminal:    \n \n\n     `pip install maptasker`          \n    \n- From the GitHub \'Code\' pull-down menu, select \'Download ZIP\', save it into a new directory (e.g. /your_id/maptasker) and uncompress it into that directory.\n\n\n### Usage \n\n- Ensure the dependencies are already installed.\n- Open a terminal window and change to the directory into which the zip file was uncompressed\n- From this directory, enter the command:\n\n\n     `maptasker (runtime options...se below)` \n \n (see below for runtime options)\n \nProgram out: the file “MapTasker.html” will be written to your runtime/current folder, which will be opened in your default browser as a new tab.\n \nRuntime: `maptasker -option1 -option2` ...\n\n### Runtime options \n \n    `-h` for help.  Also refer to HELP.md for more details,  \n    `-detail 0` for silent mode (no Action details except for first Action on unnamed Tasks),  \n    `-detail 1` to display Action list if Task onl is unnamed or anonymous (default),   \n    `-detail 2` to display Action list names for *all* Tasks,    \n    `-detail 3` to display Action list names with *all* parameters for all Tasks,    \n    `-e` to display \'everything\': Profile \'conditions\', TaskerNet info and full Task (action) details    \n    `-g` to get arguments from the GUI rather than via the command line,   \n    \n    The following three arguments are exclusive.  Use one only:\n\n    `-project \'name of project\'` to display a single Project, its Profiles and Tasks only,    \n    `-profile \'profile name\'` to display a single Profile and its Tasks only,    \n    `-task \'task name\'` to display a single Task only (forces option -d2),   \n        \n        \n    `-taskernet` to display any TaskerNet share details,    \n    `-conditions` to display a Profile\'s and Task\'s condition(s),   \n    `-c(type) color_name`  define a specific color to \'type\', where \'type\' is *one* of the following:\n\n      \'Project\' \'Profile\' \'Task\' \'Action\' \'DisabledProfile\' \'UnknownTask\' \n      \'DisabledAction\' \'ActionCondition\' \'ProfileCondition\' \'LauncherTask\' \n      \'Background\' \'ActionLabel\' \'Bullets\' \'TaskerNetInfo\'\n                \n      Example color options: -cTask Green -cBackground Black cProfile 19c8ff   \n\n    `-ch` color help: display all valid colors".     \n\n    The following two arguments are exclusive.  Use one only:\n\n    `-s`  save these settings for later reuse.    \n    `-r`  restore previously saved settings. \n\nSample output with runtime option \'-detail 0\':\n\n<img src="/documentation_images/display_level-d0.png" width="400"/>\n\nSample output with runtime option \'-detail 1\':\n\n<img src="/documentation_images/display_level-d1.png" width="400"/>\n\nSample output with runtime option \'-detail 2\':\n\n<img src="/documentation_images/display_level-d2.png" width="400"/>\n\nSample output with runtime options \'-detail 3 -profcon\':\n\n<img src="/documentation_images/display_level-d3.png" width="400"/>\n\nExample runtime options: \n    \n    \'maptasker -detail 3 -conditions -taskernet -s\'\n        (show full detail including Profile/Task \'conditions\' and TaskerNet \n         information, and save the settings)\n\nExample using GUI: \n    \n    \'maptasker -g\'\n\nAlternatively, see *config.py* for user-customizable options.  Make user-specific changes in this file and save it rather than specifying them as arguments or via the GUI.\n\n\n### To Do List (in no particular order)\n[] Catch up with recent Tasker changes in the 6.1.n code base additions\n\n[] Optionally, display Task and Profile properties\n\n[] Complete insertion of Python docstrings\n\n[] Save settings via standard ini file so it can be modified\n\n\n',
    'author': 'Michael Rubin',
    'author_email': 'mikrubin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mctinker/Map-Tasker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
