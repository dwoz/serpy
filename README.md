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

Usage
-----

```
serpy --driver chrome --limit 10 "what is the secret of life"
0 https://www.goodreads.com/quotes/tag/secret-of-life Quotes About Secret Of Life (24 quotes) - Goodreads
1 https://www.elitedaily.com/life/10-of-lifes-secrets-that-no-one-wants-you-let-it-in-on/620865 10 Of Life's Secrets That No One Wants To Let You In On - Elite Daily
2 https://www.goodreads.com/quotes/tag/secret-of-life Quotes About Secret Of Life (24 quotes) - Goodreads
3 https://www.brainpickings.org/2011/12/02/steve-jobs-1995-life-failure/ The Secret of Life from Steve Jobs in 46 Seconds – Brain Pickings
4 https://www.youtube.com/watch?v=iZ8so-ld-l0 The Secret of Life - Alan Watts - YouTube
5 https://www.pbs.org/newshour/health/the-pub-where-the-secret-of-life-was-first-announced The Day Scientists Discovered the 'Secret of Life' | PBS NewsHour
6 http://highexistence.com/life-secrets-and-tips/ 50 Life Secrets and Tips | High Existence
7 https://www.newyorker.com/tech/elements/the-secret-life-of-secrets The Secret Life of Secrets | The New Yorker
8 https://www.edx.org/course/introduction-biology-secret-life-mitx-7-00x-6 Introduction to Biology - The Secret of Life | edX
9 https://www.theguardian.com/commentisfree/series/the-secret-life The secret life | Commentisfree | The Guardian
10 https://www.forbes.com/sites/panosmourdoukoutas/2012/11/03/beyond-the-secret-change-your-life-in-five-simple-steps/ Beyond The Secret: Change Your Life in Five Simple Steps - Forbes
```
