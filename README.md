# MISP RPM
spec files to generate RPMs for MISP and it's dependencies. Uses a own compiled php version without FPM.

Building is a bit tricky, as the correct order of the dependencies is important.

## Building MISP
before the MISP RPM can be created, the following dependecies must be built (in this order)
* php
* php-pear
* php-pear-CommandLine
* php-pear-Crypt_GPG
* php-redis
* python-cybox
* python-stix
* python-mixbox
* python-pydeep
* python-pymisp
* python-lief (my current version doesn't work correctly, work in progress)
* misp

## MISP modules
Building the misp modules is even trickier, as a lot of dependencies must be built before the misp-modules RPM can be created. MISP modules rely on python3, so you can use the python 3.4 provided py CentOS or any newer python version.

* python34-pip
* python34-setuptools
* misp-stix-converter
* python34-libtaxii
* python34-lxml
* python34-six
* python34-python_dateutil
* python34-ordered_set
* python34-mixbox
* python34-cybox
* python34-stix
* python34-backports_abc
* python34-tornado
* python34-dnspython
* python34-chardet
* python34-nose
* python34-jsonschema
* python34-rdflib
* python34-beautifulsoup4
* python34-colorlog
* python34-argparse
* python34-pytz
* python34-isodate
* python34-pyparsing
* python34-redis
* python34-pygeoip
* python34-idna
* python34-urllib3
* python34-certifi
* python34-requests_cache
* python34-url_normalize
* python34-pillow
* python34-urlachriver
* python34-ez_setup
* python34-asnhistory
* python34-bs4
* python34-cabby
* python34-dateutils
* python34-firls
* python34-domaintools_api
* python34-ipasn_redis
* python34-orderedmultidict
* python34-passivetotal
* python34-olefile
* python34-pyaml
* python34-pypdns
* python34-pyeupi
* python34-pypssl
* python34-pytesseract
* python34-SPARQLWrapper
* python34-PyYAML
* python34-uwhois
* python34-uwhoisd
* python34-shodan
* python34-XlsxWriter
* python34-colorama
* python34-click
* python34-click_plugins
* python34-future
* python34-requests
* python34-pymisp
* misp-modules

