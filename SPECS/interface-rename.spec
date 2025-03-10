%global package_speccommit a641d796e17072781218dbc1ec8f1af1064e3180
%global package_srccommit v2.0.6
Summary:        A program that rename network interfaces to keep them consistent
Name:           interface-rename
Version: 2.0.6
Release:        1%{?xsrel}.1%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Source0: interface-rename-2.0.6.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildArch:      noarch
Requires:       python3-xcp-libs
Requires:       systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The %{name} package rename network interfaces in order to keep consistent
naming while moving or replacing cards on the machine.

%prep
%autosetup -p1

%install
rm -rf $RPM_BUILD_ROOT

# directories
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_unitdir}
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename-data
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
mkdir -p -m755 $RPM_BUILD_ROOT/opt/xensource/bin

# files from sources
install -m 755 interface-rename.py $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename.py
install -m 644 systemd/interface-rename.service $RPM_BUILD_ROOT%{_unitdir}/interface-rename.service
install -m 644 60-net.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -m 755 enqueue-interface-rename.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install -m 755 net-rename-sideways.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install -m 644 logrotate-interface-rename $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/interface-rename

# compatibility executable
ln $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename.py $RPM_BUILD_ROOT/opt/xensource/bin/interface-rename

# lock files
umask 022
touch $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/enqueue-interface-rename.lock
touch $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/net-rename-sideways.lock

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post interface-rename.service

%preun
%systemd_preun interface-rename.service

%postun
%systemd_postun interface-rename.service

%files
%defattr(-,root,root,-)
/etc/*
/opt/xensource/bin/*
%{_unitdir}/interface-rename.service

%changelog
* Tue Mar 04 2025 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.0.6-1.1
- remove python3 fix that has been upstreamed
- Sync with 2.0.6-1
- *** Upstream changelog ***
  * Wed Jul 24 2024 Lin Liu <lin.liu@citrix.com> - 2.0.6-1
  - CA-395874: Some python3 fix

* Thu Jul 11 2024 Yann Dirson <yann.dirson@valtes.tech> - 2.0.5-1.1
- Fix python3 port

* Fri May 03 2024 Frediano Ziglio <frediano.ziglio@cloud.com> - 2.0.5-1
- CP-49083: Do not rotate logs if empty

* Thu Oct 26 2023 Lin Liu <lin.liu@citrix.com> - 2.0.4-1
- Update to python3 and build for xs8 and xs9

* Wed Jun 26 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.3-1
- CA-322646: udevadm set as ExecStartPre to make sure interface-rename always run

* Mon Mar 26 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.2-1
- CA-286300: start interface-rename even if udev settle timed out

* Tue Dec 29 2015 Salvatore Cambria <salvatore.cambria@citrix.com>
- Switch to systemd service unit
* Wed Jul 17 2013 Frediano Ziglio <frediano.ziglio@citrix.com>
- First packaged version

