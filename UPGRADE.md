# Upgrading MISP
This RPMs are built without any requirements to use git to install or 
upgrade MISP. You'll only need access to the corresponding repository 
to get the latest version of MISP.

Upgrading MISP is straight forward, the newest RPMs will install the 
latest version of MISP on your servers.

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
- get rid of no longer neede software packages
- prevent missing DB schema upgrades

Disadvantages of a new installation:
- you need a 2nd host
- some downtime until the data are syncronized

recommended upgrade steps

* stop Apache Webserver and MariaDB
```
systemctl stop httpd
systemctl stop mariadb
```

* remove old MariaDB version (the db data will stay on the file system
```
rpm -e --nodeps MariaDB-client MariaDB-server MariaDB-shared MariaDB-common
```

* install the updated misp repo and remi repo config files
```
yum install https://certrepo.switch.ch/certrepo/misp/misp-release-1.1-1.el7.noarch.rpm
yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
```

* clean the yum cache
```
yum clean all
```

* make sure the file /etc/yum.repos.d/misp.repo points to the correct MariaDB version
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

* upgrade MISP
```
yum upgrade misp misp-python-virtualenv
```

* adjust python_bin in /var/www/MISP/app/Config/config.php
```
'python_bin' => '/var/www/cgi-bin/misp-virtualenv/bin/python3'
```

* remove old php version (e.g. 7.2.X)
```
rpm -e --nodeps php
```

* create a symlink from php74 to php
```
ln -s /bin/php74 /bin/php
```

* restart Apache webserver
```
systemctl start httpd
```

### References

MySQL Upgrade:
- To upgrade MySQL from 10.1 to 10.2 see [[https://mariadb.com/kb/en/upgrading-from-mariadb-101-to-mariadb-102/]]
- to upgrade MySQL from 10.2 to 10.3 see  [[https://mariadb.com/kb/en/upgrading-from-mariadb-102-to-mariadb-103/]]
