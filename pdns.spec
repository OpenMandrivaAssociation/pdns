Summary:	Versatile Database Driven Nameserver
Name:		pdns
Version:	4.1.3
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
# https://github.com/PowerDNS/pdns/tree/rel/auth-3.3.1
#Source0:	pdns-%%{version}.tar.gz
# Do: "wget -rm http://rtfm.powerdns.com", then compress
Source1:	rtfm.powerdns.com.tar.xz
Source2:	%{name}.service
Source10:	README.urpmi
Source100:	%{name}.rpmlintrc
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	python-virtualenv
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	libstdc++-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	polarssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	pkgconfig(zlib)
Requires(pre,post,preun,postun):	rpm-helper
Requires(post):	systemd

%description
PowerDNS is a versatile nameserver which supports a large number of different
backends ranging from simple zonefiles to relational databases and load
balancing/failover algorithms.
It comes with support for MySQL, PostgreSQL, Bind zonefiles and the 'pipe
backend', all available as external packages.

%files
%doc COPYING README rtfm.powerdns.com
%doc %{name}/*.sql
%doc README.urpmi
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/pdns@.service
%dir %{_sysconfdir}/powerdns
%dir %{_sysconfdir}/powerdns/conf.d
%dir %{_libdir}/powerdns
%{_sbindir}/%{name}_server
%{_bindir}/*
%{_mandir}/man1/*


%pre
%_pre_useradd powerdns /var/lib/powerdns /bin/false

%post
%tmpfiles_create %{name}
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel powerdns

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
%setup -qn %{name}-%{version} -a1


%build
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%configure2_5x \
    --disable-static \
    --enable-tools \
    --enable-libsodium \
    --enable-systemd \
    --with-systemd="%{_unitdir}" \
    --with-sqlite3 \
    --sysconfdir=%{_sysconfdir}/powerdns \
    --libdir=%{_libdir}/powerdns \
    --with-socketdir=/run/powerdns \
    --with-dynmodules="gmysql gpgsql pipe ldap gsqlite3 geoip" \
    --with-modules="" \
    --enable-unit-tests \
    --enable-reproducible \
    --with-mysql-lib=%{_libdir}

%make


%check
%make -C %{name} check


%install
%makeinstall_std

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


# Prepare tmpfiles support config
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/%{name}.conf
d /run/powerdns 0755 powerdns powerdns
EOF

cp %{SOURCE10} README.urpmi
