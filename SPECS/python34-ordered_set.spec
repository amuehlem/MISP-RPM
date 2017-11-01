%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-ordered_set
Version:	2.0.2
Release:	1%{?dist}
Summary:    ordered-set for python34

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.python.org/pypi/ordered-set
Source0:    ordered-set-2.0.2.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
ordered-set for python34

%prep
%setup -q -n ordered-set-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/ordered_set.py
%{pythondir}/ordered_set-%{version}-py3.4.egg-info
%{pythondir}/__pycache__/ordered_set.cpython-34.pyc

%changelog
* Tue Oct 24 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.11.0
- first version
