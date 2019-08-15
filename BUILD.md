# Building the RPMs

Before the MISP RPM can be created, the following dependencies must be built (in this order)
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

* python36-pip
* python36-setuptools
* misp-stix-converter
* python36-libtaxii
* python36-lxml
* python36-six
* python36-python_dateutil
* python36-ordered_set
* python36-mixbox
* python36-cybox
* python36-stix
* python36-backports_abc
* python36-tornado
* python36-dnspython
* python36-chardet
* python36-nose
* python36-jsonschema
* python36-rdflib
* python36-beautifulsoup4
* python36-colorlog
* python36-argparse
* python36-pytz
* python36-isodate
* python36-pyparsing
* python36-redis
* python36-pygeoip
* python36-idna
* python36-urllib3
* python36-certifi
* python36-requests_cache
* python36-url_normalize
* python36-pillow
* python36-urlachriver
* python36-ez_setup
* python36-asnhistory
* python36-cabby
* python36-dateutils
* python36-furl
* python36-domaintools_api
* python36-ipasn_redis
* python36-orderedmultidict
* python36-passivetotal
* python36-olefile
* python36-pyaml
* python36-pypdns
* python36-pyeupi
* python36-pypssl
* python36-pytesseract
* python36-SPARQLWrapper
* python36-PyYAML
* python36-uwhois
* python36-shodan
* python36-XlsxWriter
* python36-colorama
* python36-click
* python36-click_plugins
* python36-future
* python36-requests
* python36-pymisp
* misp-modules
