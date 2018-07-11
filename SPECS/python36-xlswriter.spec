%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-XlsxWriter
Version:	1.0.5
Release:	1%{?dist}
Summary:	A Python module for creating Excel XLSX files.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/XlsxWriter/
Source0:	XlsxWriter-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A Python module for creating Excel XLSX files.

%prep
%setup -q -n XlsxWriter-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/vba_extract.py
%{pylibdir}/xlsxwriter
%{pylibdir}/XlsxWriter-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.5
- first version for python36
