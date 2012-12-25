# LUGoNS wiki

A git based wiki.

# Start it:

./manage.py runserver [port]
./manage.py syncdb


# Dependencies

## TL;DR

- django: 1.4.1
- python markdown
- git

## Django version: 1.4.1

The project is written in Django 1.4.1 so it may not work in earlier versions. I tried with 1.3.x on Ubuntu 12.04 and it didn't work, so install django-1.4.x. You can get django-1.4.x source at official django site, or from ppa if you are using Ubuntu (ppa:dholbach/ppa in example) or install it with "pip".

## Django markdown template filter

We are (still) using "django.contrib.markup" for markdown-to-html conversion and you need python-markdown to get that working.

