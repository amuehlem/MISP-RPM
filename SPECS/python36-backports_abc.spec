%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-backports_abc
Version:	0.5
Release:	1%{?dist}
Summary:	A backport of recent additions to the 'collections.abc' module.

Group:		Development/Languages
License:	Python Software Foundation License
URL:		https://pypi.org/project/backports_abc/
Source0:	fake-tgz.tgz
Source1:    backports_abc-%{version}-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A backport of recent additions to the 'collections.abc' module.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv backports_abc.py $RPM_BUILD_ROOT/%{pylibdir}
mv backports_abc-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/backports_abc.py
%{pylibdir}/backports_abc-%{version}.dist-info

%changelog
* Tue Jul 10 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.5
- first version for python36
