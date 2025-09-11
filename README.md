# MISP RPM
Installing MISP on Red Hat / CentOS base systems is a bit difficult, as they provide either older
versions like PHP (e.g. 5.6), or the newer versions are installed into different paths on the systems.

We know, with our RPMs we break a number of rules for Red Hat based systems, but on the same time they simplify
the process of getting MISP running on RHEL systems. From our tests we got very good results to operate
MISP on RHEL servers without any big issues. So if you can profit from our work, please feel free to do so!

## Architecture
The idea is to install minimal CentOS or Red Hat system and enable the provided repository on it. Combining MISP
with other PHP applications might work, but was not the intention for this project. The intended setup
is to just use MISP on this server.

## Summary
We provide the following components as RPMs

* misp
* required python modules as a virtual environment
  * pymisp
* misp-modules with required submodules in a virtual environment

Requirements:
* php8 (will be installed from external remi repository)
* mariadb or postgresql (can be installed from external mariadb repository)

With our RPMs there's no need to use git to install MISP and you don't need to install anything from github.com. All you
need is to be able to include our repository on your systems. MariaDB will be installed from the official mariadb repository,
PHP and PHP modules will be installed from [Remirepo](https://rpms.remirepo.net/)

## Updates
### Sep 11
- update to 2.5.21

### Aug 28
- update to 2.5.19 and 2.5.20
- python3.12 is now used for RHEL8/9/10
- Many thanks to [Guillaume Rousse](https://github.com/guillomovitch) for helping bringing together misp25.spec

### Aug 9
- update to 2.5.18

### Aug 5
- update to 2.5.17
- update to 2.4.215

### Jul 15
- update to 2.5.16
- update to 2.4.214

### Jun 22
- update to 2.5.15
- update to 2.4.213

### Jun 16
- update to 2.5.14
- including jakub-onderka/openid-connect-php module

### Jun 13
- update to 2.5.13
- update to 2.4.211

#### May 14
- update to 2.5.11
- update to 2.5.12
- update to 2.4.210

#### Apr 22
- misp-modules 3.0.2

#### Apr 8
- update to 2.5.10

#### Mar 25 and 26
- update to 2.5.8 and 2.4.206
- update to 2.5.9 and 2.4.207
- misp-modules 3.0.0

#### Feb 26 and 28
- update to 2.5.7 and 2.4.205
- misp-modules 2.4.201

#### Jan 17
- update to 2.5.5 and 2.4.203
- update to 2.5.6 and 2.4.204

#### Jan 6
- update to 2.5.4 and 2.4.202

#### Dec 17
- update to 2.5.3 and 2.4.201

#### Nov 22
- update to 2.4.200
- first version(s) for MISP 2.5.X released check the [upgrading instructions](UPGRADE.md) for the details how to upgrade from 2.4.X to 2.5.X

#### Oct 21 2024
- update to 2.4.199
- I'm currently testing the upgrade from MISP 2.4 to 2.5 with the provided RPMs and hope to release the first version in the next days.

#### Sep 19 2024
- update to 2.4.198

#### Sep 3 2024
- update to 2.4.197

#### Aug 22 2024
- update to 2.4.196

#### Aug 8 2024
- update to 2.4.195
- EL7 is end of life (EOL), we still provide the corresponding packages, but a system upgrade to EL8 or EL9 is strongly advised

#### June 27 2024
- update to 2.4.194

#### June 10 2024
- update to 2.4.193
- removed MariaDB-Server and MariaDB-Client as dependency, this allows to install MISP with an external database. See installation instructions for more details.

#### May 21 2024
- new download url, moving to misp-project.ch, see [upgrading instructions](UPGRADE.md)
- new GPG Key
- MariaDB Upgrade to Version 11, see [upgrading instructions](UPGRADE.md)

#### May 6 2024
- started to add a release for every version created
- update to 2.4.192

## Installing MISP
Use the [installation instructions](INSTALL.md) to install MISP from our repository on RHEL7 / CentOS7 Systems

Use the [installation instructions for RHEL8](RHEL8.md) to install MISP from our repository on RHEL8 Systems (not checked on CentOS8!)

## Configuring your system for MISP
Use the [configuration recommendations](CONFIGURE.md) to configure your system for MISP. This settings are not provided by the RPMS but will help to improve operating your MISP installation.

## Upgrading MISP
See the [upgrading instructions](UPGRADE.md) to upgrade MISP from our repository

## Simple Background jobs
See the [official documentation](https://www.circl.lu/doc/misp/appendices/#appendix-g-simplebackgroundjobs-migration-guide) how to activate the SimpleBackgroundJobs. Most important settings are
* ```/etc/supervisord.conf```
```
[inet_http_server]
port=127.0.0.1:9001
username=supervisor
password=securePasswordHere
```

* ```/etc/supervisord.d/misp-workers.ini```
see the [official documentation](https://www.circl.lu/doc/misp/appendices/#appendix-g-simplebackgroundjobs-migration-guide) for this file

* start and enable supervisord
```
systemctl enable supervisord
systemctl start supervisord
```

* enable SimpleBackgroundJobs in MISP
```
'SimpleBackgroundJobs' => array(
  'enabled' => true,
  'redis_host' => 'localhost',
  'redis_port' => 6379,
  'redis_password' => '',
  'redis_database' => 13,
  'redis_namespace' => 'background_jobs',
  'max_job_history_ttl' => 86400,
  'supervisor_host' => 'localhost',
  'supervisor_port' => 9001,
  'supervisor_user' => 'supervisor',
  'supervisor_password' => 'securePasswordHere',
),
```

* check the workers are started, status should be 'RUNNING' for all workers
```
supervisorctl -s http://localhost:9001 -u supervisor -p securePasswordHere status
```
