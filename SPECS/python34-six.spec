%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-six
Version:	1.11.0
Release:	1%{?dist}
Summary:    libxml for python34

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/six
Source0:    fake-tgz.tgz
Source1:    six-%{version}-py2.py3-none-any.whl

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
six for python34

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pythondir}
mv six.py $RPM_BUILD_ROOT/%{pythondir}
mv six-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/six.py
%{pythondir}/six-%{version}.dist-info

%changelog
* Tue Oct 24 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.11.0
- first version
