Name:		python34-pip
Version:	9.0.1
Release:	2%{?dist}
Summary:    Python pip

Group:		Development/Languages
License:	MIT
URL:		https://pypi.python.org/
Source0:	pip-9.0.1.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
Requires:	python34

%description
Python pip

%prep
%setup -q -n pip-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/pip-%{version}-py3.4.egg-info
/usr/lib/python3.4/site-packages/pip
%exclude /usr/bin/pip
/usr/bin/pip3
/usr/bin/pip3.4

%changelog
* Fri Oct 20 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
