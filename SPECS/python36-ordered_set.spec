%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-ordered_set
Version:	3.0.0
Release:	1%{?dist}
Summary:	A MutableSet that remembers its order, so that every entry has an index.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/ordered-set/
Source0:	ordered-set-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A MutableSet that remembers its order, so that every entry has an index.

%prep
%setup -q -n ordered-set-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/ordered_set.py
%{pylibdir}/__pycache__/ordered_set.cpython-36.pyc
%{pylibdir}/ordered_set-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 10.0.1
- first version for python36
