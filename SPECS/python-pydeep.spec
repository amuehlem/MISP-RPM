Name:		python-pydeep
Version:	0.4
Release:	1%{?dist}
Summary:	Python extension for interfacing ssdeep

Group:		Development/Languages
License:	BSD 3-clause
URL:		https://github.com/STIXProject/
Source0:	fake-tgz.tgz

BuildRequires:	python-devel, python-setuptools, git
BuildRequires:  ssdeep-devel
Requires:	python, ssdeep

%description
Python extension for stix

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/kbandla/pydeep.git
cd pydeep
python setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib64/python2.7/site-packages/pydeep-0.4-py2.7.egg-info
/usr/lib64/python2.7/site-packages/pydeep.so
%exclude /usr/lib/debug/*
%exclude /usr/src/debug

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.4
- first version
