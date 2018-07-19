%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-idna_ssl
Version:	1.1.0
Release:	1%{?dist}
Summary:	Patch ssl.match_hostname for Unicode(idna) domains support

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/idna_ssl/
Source0:	idna-ssl-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Patch ssl.match_hostname for Unicode(idna) domains support

%prep
%setup -q -n idna-ssl-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/idna_ssl.py
%{pylibdir}/idna_ssl-%{version}-py%{pybasever}.egg-info
%{pylibdir}/__pycache__/idna_ssl*.pyc

%changelog
* Thu Jul 19 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.1.0
- first version for python36
