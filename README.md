serpy
=====

Serpy provides a library and command line tool for querying search engines.

Status
------

Serpy is currently in a pre-release status, the library and commandline APIs
will likely change.

Installation
------------


- Option 1. Install using requirements.txt

  ```
  echo '-e git+git@github.com:dwoz/serpy.git#egg=serpy' >> requirements.txt
  pip install -r requirements.txt
  ```


- Option 2. Install directly with pip

  `pip install -e git+git@github.com:dwoz/serpy.git#egg=serpy`



- Option 3. Install using the setup.py file


  ```
  git clone git@github.com:dwoz/serpy.git
  cd serpy
  virtualenv venv --python=python3
  source venv/bin/activate
  python setup.py develop
  ```
