PyramidDemo README
==================

Sample demonstration web application using Pyramid 
(http://www.pylonsproject.org/)

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_PyramidDemo_db development.ini

- mysql -u root -p -h <db-host> < pyramiddemo/script/initializedb.sql

- $VENV/bin/pserve development.ini

