%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages
%define pytzversion 2017.2

Name:		python34-pytz
Version:	3.1.0
Release:	1%{?dist}
Summary:    pytz for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    pytz-%{pytzversion}.zip

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python pytz

%prep
%setup -q -n pytz-%{pytzversion}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/pytz
%{pythondir}/pytz-%{pytzversion}-py%{pythonver}.egg-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.1.0
- first version
