<h1 align="center"> Django Blog </h1>

Witryna internetowa aplikacji Blog.

## Spis treści
* [Informacje](#informacje)
* [Technologie](#technologie)
* [Instalacja](#instalacja)
* [Użycie](#użycie)
* [Status projektu](#status)
* [Licencja](#licencja)

## Informacje
[![Build Status](https://app.travis-ci.com/Lioheart/DjangoBlog.svg?branch=master)](https://app.travis-ci.com/Lioheart/DjangoBlog)
[![Django CI](https://github.com/Lioheart/DjangoBlog/actions/workflows/django.yml/badge.svg)](https://github.com/Lioheart/DjangoBlog/actions/workflows/django.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Lioheart/DjangoBlog.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Lioheart/DjangoBlog/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Lioheart/DjangoBlog.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Lioheart/DjangoBlog/context:python)

Aplikacja ta zawiera podstawowe modele bloga, widoki, szablony i adresy URL przeznaczone do wyświetlania postów.
Zawiera także obsługę ORM i konfigurację witryny administracyjnej.
	
## Technologie
Projekt jest tworzony z wykorzystaniem technologii:
* Django
	
## Setup
Aby uruchomić projekt, wykonaj poniższe polecenia:

```
$ git clone https://github.com/Lioheart/DjangoBlog.git
$ cd DjangoBlog
# pip install virtualenv
$ python -m venv venv
$ virtualenv venv
$ source venv/bin/activate              - Linux and Mac
# Set-ExecutionPolicy RemoteSigned      - Windows
$ venv\Scripts\activate                 - Windows
# Set-ExecutionPolicy Restricted        - Windows
$ pip install -r requirements.txt
```

## Użycie
Uruchom program za pomocą komendy: `python run.py` 

## Status
Projekt przykładowy.

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Lioheart/DjangoBlog)
![GitHub repo size](https://img.shields.io/github/repo-size/Lioheart/DjangoBlog)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Lioheart/DjangoBlog/master)

## Licencja
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div>Icons from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>