%global commit 019267cb494ad2e8cc5b54d4a38fe169886831b1 
%global shortcommit %(echo %{commit} | cut -c1-7)

%if 0%{?rhel} == 8
# Disable debugsource package (RHEL8 source file tracking issues with meson)
# but keep debuginfo (actual debug symbols)
%undefine _debugsource_packages
%endif

# RHEL 8 does not support sysusers for RPM-managed user creation
%if 0%{?rhel} == 8
%global use_sysusers 0
%else
%global use_sysusers 1
%endif

Name:           pam_okta
Version:        0.1.0
Release:        0.20260312git%{shortcommit}%{?dist}
Summary:        PAM module for Okta authentication

License:        ISC
URL:            https://github.com/dgwynne/pam_okta
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        pam_okta.sysusers

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  byacc
BuildRequires:  pam-devel
BuildRequires:  jansson-devel
BuildRequires:  libbsd-devel
BuildRequires:  libcurl-devel
BuildRequires:  libjwt-devel
BuildRequires:  systemd-units

Requires:       pam
%{?systemd_requires}

Requires(pre):  shadow-utils

%description
pam_okta is a Pluggable Authentication Module (PAM) that enables
authentication against Okta.

%prep
%autosetup -n %{name}-%{commit} -p1

%build
%meson
%meson_build

%install
%meson_install

%if %{use_sysusers}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/pam_okta.conf
%endif

# Runtime directory
mkdir -p %{buildroot}%{_rundir}/pam_okta

%pre
%if ! %{use_sysusers}
# Legacy user creation for RHEL 8
getent group _pam_oktad >/dev/null || groupadd -r _pam_oktad
getent passwd _pam_oktad >/dev/null || \
    useradd -r -g _pam_oktad -s /sbin/nologin -d / -M _pam_oktad
%endif

%post
%systemd_post pam_oktad.service

%if %{use_sysusers}
%sysusers_create pam_okta.conf
%endif

%preun
%systemd_preun pam_oktad.service

%postun
%systemd_postun pam_oktad.service

%files
%doc README.md
%attr(0755,root,root) %{_libdir}/security/pam_okta.so
%{_sbindir}/pam_oktad
%{_mandir}/man5/pam_oktad.conf.5.gz
%{_mandir}/man8/pam_okta.8.gz
%{_mandir}/man8/pam_oktad.8.gz
%{_unitdir}/pam_oktad.service
%dir %attr(0700,root,root) %{_rundir}/pam_okta
%if %{use_sysusers}
%{_sysusersdir}/pam_okta.conf
%endif

%changelog
* Thu Mar 12 2026 Douglas Kosovic <doug@uq.edu.au> - 0.1.0-0.20260312git019267c
- Build from Git commit 019267cb494ad2e8cc5b54d4a38fe169886831b1

