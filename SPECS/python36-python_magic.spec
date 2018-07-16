%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-python_magic
Version:	0.4.15
Release:	1%{?dist}
Summary:	File type identification using libmagic

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/python-magic/
Source0:	python-magic-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
File type identification using libmagic

%prep
%setup -q -n python-magic-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/magic.py
%{pylibdir}/python_magic-%{version}-py%{pybasever}.egg-info
%{pylibdir}/__pycache__/*.pyc

%changelog
* Thu Jul 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.4.15
- first version for python36
