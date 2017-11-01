%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-url_normalize
Version:	1.3.3
Release:	1%{?dist}
Summary:    url_normalize for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    url-normalize-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python url_normalize

%prep
%setup -q -n url-normalize-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/url_normalize
%{pythondir}/url_normalize-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.3.3
- first version
