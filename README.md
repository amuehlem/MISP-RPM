# MISP RPM
Installing MISP on Red Hat / CentOS base systems is a bit difficult, as they provide either older
versions like PHP (e.g. 5.6), or the newer versions are installed into different paths on the systems.

We know, with our RPMs we break a number of rules for Red Hat based systems, but on the same time they simplify
the process of getting MISP running on RHEL systems. From our tests we got very good results to operate
MISP on RHEL servers without any big issues. So if you can profit from our work, please feel free to do so!

# Architecture
The idea is to install minimal CentOS or Red Hat system and enable the provided repository on it. Combining MISP
with other PHP applications might work, but was not the intention for this project. The intended setup
is to just use MISP on this server.

# Summary
We provide the following components as RPMs

* misp
* pymisp
* misp-modules
* all needed sub-modules
* php 7.4.x (will be installed from external remi repository)
* mariadb 10.3.x (will be installed from external mariadb repository)

With our RPMs there's no need to use git to install MISP and you don't need a to install from github.com. All you
is to be able to include our repository on your systems. MariaDB will be installed from the official mariadb repository.

## Installing MISP
Use the [installation instructions](INSTALL.md) to install MISP from our repository on RHEL7 / CentOS7 Systems
Use the [installation instructions for RHEL8](RHEL8.md) to install MISP from our repository on RHEL8 Systems (not checked on CentOS8!)

## Upgrading MISP
See the [upgrading instructions](UPGRADE.md) to upgrade MISP from our repository
