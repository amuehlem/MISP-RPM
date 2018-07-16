%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-ez_setup
Version:	0.9
Release:	1%{?dist}
Summary:	ez_setup.py and distribute_setup.py

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/ez_setup/
Source0:	ez_setup-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
ez_setup.py and distribute_setup.py

%prep
%setup -q -n ez_setup-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/ez_setup.py
%{pylibdir}/distribute_setup.py
%{pylibdir}/ez_setup-%{version}-py%{pybasever}.egg-info
%exclude %{pylibdir}/__pycache__/*.pyc

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.9
- first version for python36
