#
# Conditional build:
%bcond_without	tests		# build without tests
#
Summary:	STUNTMAN STUN server
Name:		stunserver
Version:	1.2.15
Release:	3
License:	Apache v2.0
Group:		Networking/Daemons
Source0:	http://www.stunprotocol.org/%{name}-%{version}.tgz
# Source0-md5:	8a923faa15fff05cbfb77330e5ebf116
Source1:	%{name}.service
Source2:	%{name}.sysconfig
Source3:	%{name}.init
URL:		http://www.stunprotocol.org/
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun,postun):	systemd-units >= 38
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
STUNTMAN is an open source implementation of the STUN protocol
(Session Traversal Utilities for NAT) as specified in RFCs 5389, 5769,
and 5780. It also includes backwards compatibility for RFC 3489.

This package contains a high performance STUN server.

%package -n stunclient
Summary:	STUNTMAN STUN client
Group:		Networking/Utilities

%description -n stunclient
STUNTMAN is an open source implementation of the STUN protocol
(Session Traversal Utilities for NAT) as specified in RFCs 5389, 5769,
and 5780. It also includes backwards compatibility for RFC 3489.

This package contains the client application.

%prep
%setup -qn %{name}

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	RELEASE_FLAGS="%{rpmcxxflags}" \
	CXX_FLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

%{?with_tests:./stuntestcode}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{systemdunitdir},/etc/{rc.d/init.d,sysconfig}}

cp -p stunclient stunserver $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README HISTORY
%attr(755,root,root) %{_bindir}/stunserver
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stunserver
%{systemdunitdir}/%{name}.service
%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files -n stunclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stunclient
