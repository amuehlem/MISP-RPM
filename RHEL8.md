**RHEL8 is officially End-of-life. Please don't install new hosts with RHEL8, use RHEL9 or RHEL10 instead**
**This instructions are for Red Hat 8 systems only, they were not checked on CentOS 8**

# Install MISP from RPM packages

## Installation instructions:

- install RHEL8 minimal system, install license
- update system to latest updates
- enable codeready-builder repository

```
subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms
```

## install epel, remi and misp repositories

```
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
dnf install https://rpms.remirepo.net/enterprise/remi-release-8.rpm
dnf install https://repo.misp-project.ch/yum/misp8/misp-release-latest.el8.noarch.rpm
```

For RHEL 8.4 EUS use the slightly older version of remi repo instead
```
dnf install https://rpms.remirepo.net/enterprise/8/remi/x86_64/remi-release-8.4-1.el8.remi.noarch.rpm
```

## install misp and misp-python-virtualenv
```
dnf install misp misp-python-virtualenv
```

## install MariaDB, if you want to use an external DB, only MariaDB-client is needed
```
dnf install MariaDB-client MariaDB-Server
```

## configuration
- configure mariadb to your needs

```
# enable mariadb startup
systemctl enable mariadb.service
systemctl start mariadb.service

# secure the installation, set a reasonable root password
mariadb-secure-installation

# install MISP DB schema
mariadb -u root -p [YOUR MYSQL PASSWORD]

# replace XXXXXXXXX with a reasonable password for misp
MariaDB [(none)]> create database misp;
MariaDB [(none)]> grant usage on *.* to misp@localhost identified by 'XXXXXXXXX';
MariaDB [(none)]> grant all privileges on misp.* to misp@localhost ;
MariaDB [(none)]> exit

cd /var/www/MISP

# Import the empty MySQL database from MYSQL.sql
mariadb -u misp -p misp < INSTALL/MYSQL.sql
```

- configure MISP

```
cd /var/www/MISP/app/Config
cp -a bootstrap.default.php bootstrap.php
cp -a database.default.php database.php
cp -a core.default.php core.php
cp -a config.default.php config.php

# set DB details in database.php, use your XXXXXXXXX password from above
# set baseurl in config.php
# set python_bin => '/var/www/cgi-bin/misp-virtualenv/bin/python3'

# set owner and selinux context
chown apache:apache /var/www/MISP/app/Config/config.php
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Config/config.php

# enable misp-workers at startup
systemctl enable misp-workers
systemctl start misp-workers
```

- configure php

all php settings are done in ```/etc/opt/remi/php74/php.ini```

- link php
```
ln -s /bin/php74 /bin/php
```

- start redis

```
# enable redis at startup
systemctl enable redis
systemctl start redis
```

- start httpd

```
# enable apache at startup
systemctl enable httpd
systemctl start httpd
```

```
# enable php-fpm at startup
systemctl enable php83-php-fpm
systemctl start php83-php-fpm
```

```
# enable supervisord at startup
systemctl enable --now supervisord
```


- open firewall

```
# open firewall for http and https
firewall-cmd --permanent --zone=public --add-service http
firewall-cmd --permanent --zone=public --add-service https
systemctl restart firewalld
```

## install and enable misp-modules
```
dnf install misp-modules
# enable misp-modules at startup
systemctl enable misp-modules
systemctl start misp-modules
```

- **reboot the host to make sure all services are started correctly**

