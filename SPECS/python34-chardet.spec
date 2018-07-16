%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-chardet
Version:	3.0.4
Release:	3%{?dist}
Summary:    chardet for python34

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/pyaml
Source0:    chardet-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
python34 chardet

%prep
%setup -q -n chardet-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/chardet
%{pythondir}/chardet-%{version}-py%{pythonver}.egg-info
%exclude %{_bindir}/chardetect

%changelog
* Thu May 3 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.0.4
- first version
