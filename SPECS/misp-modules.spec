%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		misp-modules
Version:	2.4.93
Release:	1%{?dist}
Summary:	MISP modules for expansion services, import and export

Group:		Development/Languages
License:	GPLv3
URL:		https://github.com/MISP/misp-modules
Source0:	fake-tgz.tgz
Source1:    misp-modules.service
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools, python36-pip
BuildRequires:  misp-stix-converter, python36-libtaxii
BuildRequires:  libpqxx-devel, libjpeg-turbo-devel, git
BuildRequires:  libxml2-devel, libxslt-devel
BuildRequires:  python36-lxml, python36-six, python36-mixbox
BuildRequires:  python36-python_dateutil, python36-ordered_set
BuildRequires:  python36-cybox, python36-stix, python36-backports_abc
BuildRequires:  python36-tornado, python36-dnspython
BuildRequires:  python36-chardet, python36-nose, python36-jsonschema
BuildRequires:  python36-rdflib, python36-beautifulsoup4, python36-argparse
BuildRequires:  python36-pytz, python36-colorlog, python36-pyparsing
BuildRequires:  python36-isodate, python36-redis, python36-pillow
BuildRequires:  python36-pygeoip, python36-idna, python36-urllib3 < 1.23
BuildRequires:  python36-certifi, python36-url_normalize, python36-requests_cache
BuildRequires:  python36-requests, python36-urlarchiver, python36-ez_setup
BuildRequires:  python36-asnhistory, python36-cabby
BuildRequires:  python36-dateutils, python36-furl, python36-domaintools_api
BuildRequires:  python36-ipasn_redis, python36-orderedmultidict, python36-passivetotal
BuildRequires:  python36-olefile, python36-pyaml, python36-pypdns
BuildRequires:  python36-pyeupi, python36-pypssl, python36-pytesseract
BuildRequires:  python36-SPARQLWrapper, python36-PyYAML, python36-uwhois
BuildRequires:  python36-shodan, python36-XlsxWriter, python36-colorama
BuildRequires:  python36-click, python36-click_plugins, python36-future
Requires:	    python36, python36-setuptools, python36-pip
Requires:       libpqxx, libjpeg-turbo, misp-stix-converter
Requires:       libxml2, libxslt
Requires:       python36-libtaxii, python36-six
Requires:       python36-python_dateutil, python36-ordered_set
Requires:       python36-cybox, python36-stix, python36-backports_abc
Requires:       python36-tornado, python36-dnspython
Requires:       python36-chardet, python36-nose, python36-jsonschema
Requires:       python36-rdflib, python36-beautifulsoup4, python36-argparse
Requires:       python36-pytz, python36-colorlog, python36-pyparsing
Requires:       python36-isodate, python36-redis, python36-pillow
Requires:       python36-pygeoip, python36-idna, python36-urllib3 < 1.23
Requires:       python36-certifi, python36-url_normalize, python36-requests_cache
Requires:       python36-requests, python36-urlarchiver, python36-ez_setup
Requires:       python36-asnhistory, python36-cabby
Requires:       python36-dateutils, python36-furl, python36-domaintools_api
Requires:       python36-ipasn_redis, python36-orderedmultidict, python36-passivetotal
Requires:       python36-olefile, python36-pyaml, python36-pypdns
Requires:       python36-pyeupi, python36-pypssl, python36-pytesseract
Requires:       python36-SPARQLWrapper, python36-PyYAML, python36-uwhois
Requires:       python36-shodan, python36-XlsxWriter, python36-colorama
Requires:       python36-click, python36-click_plugins, python36-future

%description
MISP modules for expansion services, import and export

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/MISP/misp-modules.git
cd misp-modules
python3 setup.py install --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system

%files
%{_bindir}/misp-modules
%{pylibdir}/misp_modules
%{pylibdir}/misp_modules-%{version}-py%{pybasever}.egg-info
%{_sysconfdir}/systemd/system/misp-modules.service
%exclude %{pylibdir}/tests

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.93
- first version for python36