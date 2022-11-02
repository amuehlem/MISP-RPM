# MISP Configuration

This document lists some best practices regarding configuring your MISP installation when using the provided RPM packages.

## Apache and PHP
### Redis Sessions get blocked
 * ```/etc/opt/remi/php74/php.ini```
```
session.save_handler = redis
session.save_path = "tcp://127.0.0.1:6379"
```

* ```/etc/httpd/conf.d/php74-php.conf```
comment out this two lines
```
php_value session.save_handler "files"
php_value session.save_path    "/var/opt/remi/php74/lib/php/session"
```
