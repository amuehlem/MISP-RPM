%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-python_dateutil
Version:	2.7.3
Release:	1%{?dist}
Summary:	Extensions to the standard Python datetime module

Group:		Development/Languages
License:	Apache Software License, BSD License (Dual License)
URL:		https://pypi.org/project/python-dateutil/
Source0:	fake-tgz.tgz
Source1:    python_dateutil-2.7.3-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Extensions to the standard Python datetime module

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv dateutil $RPM_BUILD_ROOT/%{pylibdir}
mv python_dateutil-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/dateutil
%{pylibdir}/python_dateutil-%{version}.dist-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.7.3
- first version for python36
