#
# Conditional build:
%bcond_without	tests		# build without tests
#
Summary:	STUNTMAN STUN server
Name:		stunserver
Version:	1.2.13
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons
Source0:	http://www.stunprotocol.org/%{name}-%{version}.tgz
# Source0-md5:	c56b74796c5447850ab29d37d947f6c6
Source1:	%{name}.service
Source2:	%{name}.sysconfig
Patch0:		%{name}-openssl.patch
URL:		http://www.stunprotocol.org/
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun,postun):	systemd-units >= 38
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
%patch0 -p1

%build
%{__make} \
	RELEASE_FLAGS="%{rpmcxxflags}" \
	CXX_FLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

%{?with_tests:./stuntestcode}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{systemdunitdir},/etc/sysconfig}

cp -p stunclient stunserver $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README HISTORY
%attr(755,root,root) %{_bindir}/stunserver
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stunserver
%{systemdunitdir}/%{name}.service

%files -n stunclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stunclient
