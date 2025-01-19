%define _disable_ld_no_undefined 1

Summary:	Versatile Database Driven Nameserver
Name:		pdns
Version:	4.9.3
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		https://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
# https://github.com/PowerDNS/pdns/tree/rel/auth-3.3.1
#Source0:	pdns-%%{version}.tar.gz
# Do: "wget -rm http://rtfm.powerdns.com", then compress
Source1:	rtfm.powerdns.com.tar.xz
Source2:	%{name}.service
Source100:	%{name}.rpmlintrc
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
# configure script looks for systemctl
BuildRequires:	systemd
BuildRequires:	python-virtualenv
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	libstdc++-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(ldap)
BuildRequires:	polarssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(lmdb)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(libmaxminddb)

%description
PowerDNS is a versatile nameserver which supports a large number of different
backends ranging from simple zonefiles to relational databases and load
balancing/failover algorithms.
It comes with support for MySQL, PostgreSQL, Bind zonefiles and the 'pipe
backend', all available as external packages.

%files
%doc COPYING README rtfm.powerdns.com
%doc %{_docdir}/pdns/*.sql
%doc %{_docdir}/pdns/*.schema
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/pdns@.service
%dir %{_sysconfdir}/powerdns
%dir %{_sysconfdir}/powerdns/conf.d
%dir %{_libdir}/powerdns
%{_mandir}/man1/*
%{_bindir}/calidns
%{_bindir}/dnsbulktest
%{_bindir}/dnsgram
%{_bindir}/dnspcap2calidns
%{_bindir}/dnspcap2protobuf
%{_bindir}/dnsreplay
%{_bindir}/dnsscan
%{_bindir}/dnsscope
%{_bindir}/dnstcpbench
%{_bindir}/dnswasher
%{_bindir}/dumresp
%{_bindir}/ixplore
%{_bindir}/nproxy
%{_bindir}/nsec3dig
%{_bindir}/pdns_control
%{_bindir}/pdns_notify
%{_bindir}/pdns_server
%{_bindir}/pdnsutil
%{_bindir}/saxfr
%{_bindir}/sdig
%{_bindir}/stubquery
%{_bindir}/zone2json
%{_bindir}/zone2ldap
%{_bindir}/zone2sql

#----------------------------------------------------------------------------
%package ixfrdist
Summary:	IXFR domain transfer tool
Group:		System/Servers

%description ixfrdist
IXFR domain transfer tool

%files ixfrdist
%{_bindir}/ixfrdist
%{_sysconfdir}/powerdns/ixfrdist.example.yml
%{_unitdir}/ixfrdist.service
%{_unitdir}/ixfrdist@.service
%{_mandir}/man5/ixfrdist.yml.5*

#----------------------------------------------------------------------------

%package backend-lua
Summary:	Lua scripting backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description backend-lua
This package contains a Lua scripting backend for the PowerDNS nameserver.

%files backend-lua
%doc COPYING
%{_libdir}/powerdns/%{name}/liblua2backend.so

#----------------------------------------------------------------------------

%package backend-bind
Summary:	BIND backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description backend-bind
This package contains a BIND backend for the PowerDNS nameserver.

%files backend-bind
%doc COPYING
%{_libdir}/powerdns/%{name}/libbindbackend.so

#----------------------------------------------------------------------------

%package backend-lmdb
Summary:	LMDB backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description backend-lmdb
This package contains an LMDB backend for the PowerDNS nameserver.

%files backend-lmdb
%doc COPYING
%{_libdir}/powerdns/%{name}/liblmdbbackend.so


#----------------------------------------------------------------------------

%package backend-remote
Summary:	Remote backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description backend-remote
This package contains a Remote backend for the PowerDNS nameserver.

%files backend-remote
%doc COPYING
%{_libdir}/powerdns/%{name}/libremotebackend.so

#----------------------------------------------------------------------------

%package backend-geo
Summary:	GEOIP backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-geo
This package contains a geoip backend for the PowerDNS nameserver.

%files backend-geo
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libgeoipbackend.conf
%{_libdir}/powerdns/%{name}/libgeoipbackend.so

#----------------------------------------------------------------------------

%package backend-pipe
Summary:	Pipe/coprocess backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-pipe
This package contains the pipe backend for the PowerDNS nameserver. This
allows PowerDNS to retrieve domain info from a process that accepts
questions on stdin and returns answers on stdout. 

%files backend-pipe
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libpipebackend.conf
%{_libdir}/powerdns/%{name}/libpipebackend.so

#----------------------------------------------------------------------------

%package backend-ldap
Summary:	LDAP backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-ldap
This package contains a LDAP backend for the PowerDNS nameserver.

%files backend-ldap
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libldapbackend.conf
%{_libdir}/powerdns/pdns/libldapbackend.so

#----------------------------------------------------------------------------

%package backend-mysql
Summary:	MySQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-mysql
This package contains a MySQL backend for the PowerDNS nameserver.

%files backend-mysql
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libgmysqlbackend.conf
%{_libdir}/powerdns/%{name}/libgmysqlbackend.so

#----------------------------------------------------------------------------

%package backend-pgsql
Summary:	Generic PostgreSQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-pgsql
This package contains a generic PostgreSQL backend for the PowerDNS
nameserver. It has configurable SQL statements.

%files backend-pgsql
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libgpgsqlbackend.conf
%{_libdir}/powerdns/%{name}/libgpgsqlbackend.so

#----------------------------------------------------------------------------

%package backend-sqlite
Summary:	SQLite backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-sqlite
This package contains a SQLite backend for the PowerDNS nameserver.

%files backend-sqlite
%doc COPYING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/conf.d/libgsqlite3backend.conf
%{_libdir}/powerdns/%{name}/libgsqlite3backend.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -a1

%conf
%configure \
	--enable-tools \
	--enable-libsodium \
	--enable-systemd \
	--with-systemd="%{_unitdir}" \
	--with-sqlite3 \
	--sysconfdir=%{_sysconfdir}/powerdns \
	--libdir=%{_libdir}/powerdns \
	--with-socketdir=/run/powerdns \
	--with-dynmodules="gmysql gpgsql pipe ldap lmdb lua2 gsqlite3 geoip remote bind" \
	--with-modules="" \
	--enable-unit-tests \
	--enable-dns-over-tls \
	--enable-ipcipher \
	--enable-reproducible \
	--with-mysql-lib=%{_libdir} \
	--enable-experimental-pkcs11 \
	--enable-experimental-gss-tsig \
	--enable-remotebackend-zeromq \
	--enable-ixfrdist \
	--enable-lto

%build
%make_build

%check
make -C %{name} check

%install -a
%make_install

# Install systemd unit
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service


# Fix the config
mv %{buildroot}%{_sysconfdir}/powerdns/%{name}.conf-dist %{buildroot}%{_sysconfdir}/powerdns/%{name}.conf

cat >> %{buildroot}%{_sysconfdir}/powerdns/%{name}.conf << EOF
include-dir=%{_sysconfdir}/powerdns/conf.d
module-dir=%{_libdir}/powerdns
socket-dir=/run/powerdns
setuid=powerdns
setgid=powerdns
launch=bind
EOF

chmod 600 %{buildroot}%{_sysconfdir}/powerdns/%{name}.conf

install -d %{buildroot}%{_sysconfdir}/powerdns/conf.d


# Fix per backend config files
for i in geoip gmysql gpgsql gsqlite3 ldap pipe; do
    echo "# backend config for %{_libdir}/powerdns/lib${i}backend.so" > %{buildroot}%{_sysconfdir}/powerdns/conf.d/lib${i}backend.conf
done

# Create user/group
mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<EOF
g powerdns
u powerdns - "PowerDNS Name Server" %{_localstatedir}/lib/powerdns -
EOF

# Prepare tmpfiles support config
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/%{name}.conf
d /run/powerdns 0755 powerdns powerdns
EOF
