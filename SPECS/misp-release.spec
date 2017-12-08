Name:       misp-release	
Version:	1.0
Release:	2%{?dist}
Summary:	configuration for MISP repositories

Group:		System Environment/Base
License:	GPLv2
URL:		https://cruncher.switch.ch/repos/
Source0:	misp.repo

BuildArch:  noarch

%description
Configuration for MISP repositories (Mariadb and MISP)


%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*

%changelog
* Wed Oct 18 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
