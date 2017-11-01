%define pythonver 3.4
%define pythondir %{_libdir}/python%{pythonver}/site-packages

Name:	misp-modules	
Version:	2.4.81
Release:	2%{?dist}
Summary:	Expansion modules for MISP

Group:	    Internet Applications	
License:    GPLv3	
URL:		https://github.com/MISP/misp-modules
Source0:	fake-tgz.tgz
Source1:    misp-modules.service

BuildArch:  noarch
BuildRequires:  python34-devel, python34-pip, python34-setuptools
BuildRequires:  misp-stix-converter, python34-libtaxii
BuildRequires:  libpqxx-devel, libjpeg-turbo-devel, git
BuildRequires:  libxml2-devel, libxslt-devel
BuildRequires:  python34-lxml, python34-six, python34-mixbox
BuildRequires:  python34-python_dateutil, python34-ordered_set
BuildRequires:  python34-cybox, python34-stix, python34-backports_abc
BuildRequires:  python34-tornado, python34-dnspython3
BuildRequires:  python34-chardet, python34-nose, python34-jsonschema
BuildRequires:  python34-rdflib, python34-beautifulsoup4, python34-argparse
BuildRequires:  python34-pytz, python34-colorlog, python34-pyparsing
BuildRequires:  python34-isodate, python34-redis, python34-pillow
BuildRequires:  python34-pygeoip, python34-idna, python34-urllib3 <= 1.21
BuildRequires:  python34-certifi, python34-url_normalize, python34-requests_cache
BuildRequires:  python34-requests, python34-urlarchiver, python34-ez_setup
BuildRequires:  python34-asnhistory, python34-bs4, python34-cabby
BuildRequires:  python34-dateutils, python34-furl, python34-domaintools_api
BuildRequires:  python34-ipasn_redis, python34-orderedmultidict, python34-passivetotal
BuildRequires:  python34-olefile, python34-pyaml, python34-pypdns
BuildRequires:  python34-pyeupi, python34-pypssl, python34-pytesseract
BuildRequires:  python34-SPARQLWrapper, python34-PyYAML, python34-uwhoisd
BuildRequires:  python34-shodan, python34-XlsxWriter, python34-colorama
BuildRequires:  python34-click, python34-click_plugins
Requires:	    python34, python34-pip, libpqxx, libjpeg-turbo
Requires:       misp-stix-converter, python34-libtaxii, python34-mixbox
Requires:       libxml2, libxslt, python34-lxml, python34-six
Requires:       python34-python_dateutil, python34-ordered_set
Requires:       python34-cybox, python34-stix, python34-backports_abc
Requires:       python34-tornado, python34-dnspython3
Requires:       python34-chardet, python34-nose, python34-jsonschema
Requires:       python34-rdflib, python34-beautifulsoup4, python34-argparse
Requires:       python34-pytz, python34-colorlog, python34-pyparsing
Requires:       python34-isodate, python34-redis, python34-pillow
Requires:       python34-pygeoip, python34-idna, python34-urllib3 <= 1.21
Requires:       python34-certifi, python34-url_normalize, python34-requests_cache
Requires:       python34-requests, python34-urlarchiver, python34-ez_setup
Requires:       python34-asnhistory, python34-bs4, python34-cabby
Requires:       python34-dateutils, python34-furl, python34-domaintools_api
Requires:       python34-ipasn_redis, python34-orderedmultidict, python34-passivetotal
Requires:       python34-olefile, python34-pyaml, python34-pypdns
Requires:       python34-pyeupi, python34-pypssl, python34-pytesseract
Requires:       python34-SPARQLWrapper, python34-PyYAML, python34-uwhoisd
Requires:       python34-shodan, python34-XlsxWriter, python34-colorama
Requires:       python34-click, python34-click_plugins

%description
Expansion modules for MISP

%prep
%setup -q -n fake-tgz

%build

%install
git clone https://github.com/MISP/misp-modules.git
#mkdir requirements
#pip3 download -d requirements -r misp-modules/REQUIREMENTS
#pip3 install --install-option="--root=$RPM_BUILD_ROOT" -r misp-modules/REQUIREMENTS
cd misp-modules
python3 setup.py install --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system

%files
%{_bindir}/misp-modules
%{_libdir}/python3.4/site-packages/misp_modules-1.0-py3.4.egg-info
%{_libdir}/python3.4/site-packages/misp_modules
%{_sysconfdir}/systemd/system/misp-modules.service
%exclude %{_libdir}/python3.4/site-packages/tests

%changelog
* Wed Oct 18 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.81
- first version
