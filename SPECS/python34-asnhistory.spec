%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-asnhistory
Version:	2.0.4
Release:	1%{?dist}
Summary:    asnhistory for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    asnhistory-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python asnhistory

%prep
%setup -q -n asnhistory-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/asnhistory
%{pythondir}/asnhistory-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.0.4
- first version
