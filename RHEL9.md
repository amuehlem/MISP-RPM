# Install MISP from RPM packages

## Installation instructions:

- install RHEL9 or Rocky9 or similar minimal system, install license when needed
- update system to latest updates

## install epel, remi and misp repositories

```
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
dnf install https://rpms.remirepo.net/enterprise/remi-release-9.rpm
dnf install https://repo.misp-project.ch/yum/misp9/misp-release-latest.el9.noarch.rpm
```

## install misp and misp-python-virtualenv
```
dnf install misp misp-python-virtualenv
```

## install MariaDB, if you want to use an external DB, only MariaDB-client is needed
```
dnf install MariaDB-client MariaDB-server
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
mysql -u root -p [YOUR MYSQL PASSWORD]

# replace XXXXXXXXX with a reasonable password for misp
MariaDB [(none)]> create database misp;
MariaDB [(none)]> grant usage on *.* to misp@localhost identified by 'XXXXXXXXX';
MariaDB [(none)]> grant all privileges on misp.* to misp@localhost ;
MariaDB [(none)]> exit

cd /var/www/MISP

# Import the empty MySQL database from MYSQL.sql
mysql -u misp -p misp < INSTALL/MYSQL.sql
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
systemctl enable php74-php-fpm
systemctl start php74-php-fpm
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

