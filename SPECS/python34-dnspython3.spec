%define date %(date +"%Y%m%d")
%define pythonver 3.4
%define pythondir %{_libdir}/python%pythonver/site-packages

Name:		python34-dnspython3
Version:	1.15.0
Release:	1%{?dist}
Summary:	Python dnspython3

Group:		Development/Languages
License:	DNSpython
URL:		https://github.com/pypa/dnspython3/
Source0:	dnspython3-%{version}.zip

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
Requires:	python34

%description
Python dnspython3

%prep
%setup -q -n dnspython3-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/dnspython3-%{version}-py%{pythonver}.egg-info
#%{pythondir}/dnspython3

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.5.2
- first version
