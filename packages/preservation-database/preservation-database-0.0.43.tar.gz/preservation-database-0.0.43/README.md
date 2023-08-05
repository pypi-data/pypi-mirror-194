# Preservation Status Database Builder
Returns the preservation status of a Crossref DOI matched against mainstream digital preservation platforms.

![license](https://img.shields.io/gitlab/license/crossref/labs/preservation-database) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/preservation-database) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This application allows you to build a database of digital preservation sources and then to match a DOI against common digital preservation systems.

## Installation
The easiest install is via pip:
    
    pip install preservation-database

Then add "preservationdatabase" (no hyphen) to your list of INSTALLED_APPS.

## Usage

    export DJANGO_SETTINGS_MODULE=import_settings.settings

    Usage: python -m preservationdatabase.cli [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      import-all         Download and import all data (excluding HathiTrust)
      import-cariniana   Download and import data from Cariniana
      import-clockss     Download and import data from CLOCKSS
      import-hathi       Import data from HathiTrust (requires local file download)
      import-lockss      Download and import data from LOCKSS
      import-pkp         Download and import data from PKP's private LOCKSS network
      import-portico     Download and import data from Portico
      show-preservation  Determine whether a DOI is preserved

## Features
* Cariniana import.
* CLOCKSS import.
* HathiTrust import.
* LOCKSS import.
* PKP PLN import.
* Portico import.
* Crossref DOI lookup.

## First-Run Setup
First, copy example_settings.py to settings.py and check settings.py to ensure that the database you want to use is set correctly. The default is db.sqlite. You should carefully read and check all of settings.py.

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

Next, run the database build commands:

    python3 manage.py makemigrations
    python3 manage.py makemigrations preservation-database
    python3 manage.py migrate 

You should then have a working database into which you can import new preservation data.

# Credits
* [Django](https://www.djangoproject.com/) for the ORM.
* [Git](https://git-scm.com/) from Linus Torvalds _et al_.
* [.gitignore](https://github.com/github/gitignore) from Github.
* [Rich](https://github.com/Textualize/rich) from Textualize.

&copy; Crossref 2023