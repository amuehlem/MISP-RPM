#!/bin/bash

su -s /bin/bash apache -c '/var/www/MISP/app/Console/worker/start.sh'
