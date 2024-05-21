# Upgrading MISP
This RPMs are built without any requirements to use git to install or 
upgrade MISP. You'll only need access to the corresponding repository 
to get the latest version of MISP.

Upgrading MISP is straight forward, the newest RPMs will install the 
latest version of MISP on your servers.

## Upgrading to new repository URL
in May 2024 the repository URL moved to a new host. This might need some manual interaction on the MISP server.

Remove the current misp-release
``` rpm -e --nodeps misp-release```

Install the current misp-release 

EL8: ```yum install https://repo.misp-project.ch/yum/misp8/misp-release-1.1-1.el8.noarch.rpm```

EL9: ```dnf install https://repo.misp-project.ch/yum/misp9/misp-release-1.1-1.el9.noarch.rpm```

This will also install the new GPG Key

## Upgrading MariaDB
The MariaDB upgrade process doesn't allow to just install a new version over an existing version. The old version must manually be removed.

```
systemctl stop mariadb
rpm -e --nodeps MariaDB-server
dnf install MariaDB-server
systemctl start mariadb
mariadb-upgrade -u root -p
```

## Upgrading from a version before 2.4.145 to 2.4.145 or later
In version 2.4.145, the MISP RPM changes quite a bit. Instead of installing 
a lot of python36 modules, all python dependencies for MISP and PyMISP will 
be installed into a python virtual environment which is provided as a
RPM package in the same repository.

* We now use the PHP packages provided from [Remi Repo](https://rpms.remirepo.net/)
instead of compiling them our self.
* The MySQL version changes from version 10.1 to 10.3.

In general you can upgrade to version 2.4.145 without any problems
but you might consider to install MISP 2.4.145 on a freshly installed host
and migrate the data via a sync or export in MISP. Please be aware of the 
MySQL upgrade process described below.

Advantages of a new installation:
- get rid of all previous problems and start on a fresh host
- get rid of no longer needed software packages
- prevent missing DB schema upgrades

Disadvantages of a new installation:
- you need a 2nd host
- some downtime until the data are synchronized

recommended upgrade steps

* stop Apache web server and MariaDB
```
systemctl stop httpd
systemctl stop mariadb
```

* remove old MariaDB version (the db data will stay on the file system
```
rpm -e --nodeps MariaDB-client MariaDB-server MariaDB-shared MariaDB-common
```

* install the updated MISP repo and remi repo config files
```
yum install https://certrepo.switch.ch/certrepo/misp/misp-release-1.1-2.el7.noarch.rpm
yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
```

* clean the yum cache
```
yum clean all
```

* make sure the file /etc/yum.repos.d/misp.repo points to the correct MariaDB version, check if a misp.repo.rpmnew needs to be moved to misp.repo
```
[mariadb]
name=mariadb
baseurl=http://yum.mariadb.org/10.3/centos7-amd64/
enabled=1
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
```

* install new MariaDB version
```
yum install --enablerepo=misp MariaDB-server MariaDB-client
```

* start MariaDB
```
systemctl start mariadb
systemctl enable mariadb
```

* upgrade the databases (might take a while), you'll need the database root account password
```
mysql_upgrade -uroot -p
```

* upgrade MISP, make sure misp-python-virtualenv is installed as dependency
```
yum upgrade misp
```

* adjust python_bin in /var/www/MISP/app/Config/config.php
```
'python_bin' => '/var/www/cgi-bin/misp-virtualenv/bin/python3'
```

* check MISP config for new settings, compare your config.php with config.php.default in ```/var/www/MISP/app/Config```

* remove old php version (e.g. 7.2.X)
```
rpm -e --nodeps php
```

* create a symlink from php74 to php
```
ln -s /bin/php74 /bin/php
```

* check php settings in /etc/opt/remi/php74/php.ini

* restart Apache web server
```
systemctl start httpd
```

### References

MySQL Upgrade:
- To upgrade MySQL from 10.1 to 10.2 see [[https://mariadb.com/kb/en/upgrading-from-mariadb-101-to-mariadb-102/]]
- to upgrade MySQL from 10.2 to 10.3 see  [[https://mariadb.com/kb/en/upgrading-from-mariadb-102-to-mariadb-103/]]
