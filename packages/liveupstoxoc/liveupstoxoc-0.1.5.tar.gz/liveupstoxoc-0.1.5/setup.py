# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'liveupstoxoc',         # How you named your package folder (MyLib)
  packages = ['liveupstoxoc'],   # Chose the same as "name"
  version = '0.1.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'To scrape live optionschain data from upstox for free (without api)', 
  long_description=long_description,
  long_description_content_type='text/markdown',  # Give a short description about your library
  author = 'Niraj Munot',                   # Type in your name
  author_email = 'nirajmunot28@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/MaticAlgos',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MaticAlgos/liveupstoxoc/archive/refs/tags/0.1.5.tar.gz',    # I explain this later on
  keywords = ['upstox', 'optionschain', 'liveoptionschain', "NSE", "openinterest"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'beautifulsoup4',
          "pandas"
          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
