%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-XlsxWriter
Version:	1.0.2
Release:	1%{?dist}
Summary:    XlsxWriter for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    XlsxWriter-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python XlsxWriter

%prep
%setup -q -n XlsxWriter-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/vba_extract.py
%{pythondir}/xlsxwriter
%{pythondir}/XlsxWriter-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.2
- first version
