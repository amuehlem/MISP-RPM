%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-cybox
Version:	2.1.0.17
Release:	2%{?dist}
Summary:	A Python library for parsing and generating CybOX content.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/libtaxii/
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36

%description
A Python library for parsing and generating CybOX content.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/CybOXProject/python-cybox.git
cd python-cybox
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/cybox
%{pylibdir}/cybox-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.17
- first version for python36
