Name:		python-lief
Version:	0.8.0
Release:	1%{?dist}
Summary:	Python extension for lief

Group:		Development/Languages
License:	Apache
URL:		https://github.com/lief-project/
Source0:	pylief-0.8.0.zip

BuildRequires:	python-devel, python-setuptools > 36
Requires:	python

%description
Python extension for lief

%prep
%setup -q -n lief-%{version}

%build
# intentianally left empty

%install
python setup.py install --root=$RPM_BUILD_ROOT

%files
%{_libdir}/python2.7/site-packages/_pylief.so
%{_libdir}/python2.7/site-packages/lief-%{version}-py2.7.egg-info
%{_libdir}/python2.7/site-packages/lief

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.2
- first version
