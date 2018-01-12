# MISP-RPM

Install MISP from RPM packages

build instructions:

- install centos minimal system
- disable selinux
- update system to last updates
- install and enable epel repository
- add misp-release repo

## installation steps
currently the RPMs are provided in an repository which you have to install first
```
yum install https://certrepo.switch.ch/certrepo/misp/misp-release-1.0-2.el7.noarch.rpm
```

- install misp

```
yum install php php-mysql php-opcache misp misp-modules
```

- configure mariadb

```

# enable mariadb startup
systemctl enable mariadb.service
systemctl start mariadb.service
# secure the installation, set a reasonable password
mysql_secure_installation
# install MISP db schema
mysql -u root -p

MariaDB [(none)]> create database misp;
MariaDB [(none)]> grant usage on *.* to misp@localhost identified by 'XXXXXXXXX';
MariaDB [(none)]> grant all privileges on misp.* to misp@localhost ;
MariaDB [(none)]> exit

cd /var/www/MISP

# Import the empty MySQL database from MYSQL.sql
mysql -u misp -p misp < INSTALL/MYSQL.sql
```

- configure misp

```
cd /var/www/MISP/app/Config
cp -a bootstrap.default.php bootstrap.php
cp -a database.default.php database.php
cp -a core.default.php core.php
cp -a config.default.php config.php

# set DB details in database.php
# set baseurl in config.php
chown apache:apache /var/www/MISP/app/Config/config.php
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Config/config.php
# enable workers at startup
# add to /etc/rc.local
su -s /bin/bash apache -c '/var/www/MISP/app/Console/worker/start.sh'
chmod +x /etc/rc.local
```

- start redis

```
systemctl enable redis
systemctl start redis
```

- start httpd

```
# enable apache at startup
systemctl enable httpd
systemctl start httpd
```

- open firewall

```
firewall-cmd --permanent --zone=public --add-service http
firewall-cmd --permanent --zone=public --add-service https
systemctl restart firewalld
```

- enable misp-modules
```
# enable misp-modules at startup
systemctl enable misp-modules
systemctl start misp-modules
```
