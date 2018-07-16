%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-url_normalize
Version:	1.3.3
Release:	1%{?dist}
Summary:	URL normalization for Python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/url_normalize/
Source0:	url-normalize-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
URL normalization for Python

%prep
%setup -q -n url-normalize-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/url_normalize
%{pylibdir}/url_normalize-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.3.3
- first version for python36
