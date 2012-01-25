%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

Summary:	Versatile Database Driven Nameserver
Name:		pdns
Version:	3.0.1
Release:	%release
License:	GPL
Group:		System/Servers
URL:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/pdns-%{version}.tar.gz
# wget -rm http://rtfm.powerdns.com
Source1:	rtfm.powerdns.com.tar.bz2
# from http://downloads.powerdns.com/releases/pdns-recursor-3.3.tar.bz2
Source2:	cachecleaner.hh
# http://wiki.powerdns.com/trac/browser/trunk/pdns/modules/luabackend/lua_functions.hh?rev=2208
Source3:	lua_functions.hh
Patch0:		pdns-2.9.7-init.patch
Patch1:		pdns-3.0.1-lib64_fix.diff
Patch2:		pdns-3.0.1-lua_linkage_fix.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	lua-devel >= 5.1
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
#BuildRequires:	docbook-utils-pdf
Provides:	nameserver powerdns PowerDNS
Obsoletes:	nameserver powerdns PowerDNS
Requires:	pdns-backend-lua
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PowerDNS is a versatile nameserver which supports a large number
of different backends ranging from simple zonefiles to relational
databases and load balancing/failover algorithms.

It comes with support for MySQL, PostgreSQL, Bind zonefiles and the 'pipe
backend' availible as external packages.

%package	backend-pipe
Summary:	Pipe/coprocess backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-pipe
This package contains the pipe backend for the PowerDNS nameserver. This
allows PowerDNS to retrieve domain info from a process that accepts
questions on stdin and returns answers on stdout. 

%package	backend-mysql
Summary:	MySQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-mysql
This package contains a MySQL backend for the PowerDNS nameserver.

%package	backend-pgsql
Summary:	Generic PostgreSQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-pgsql
This package contains a generic PostgreSQL backend 
for the PowerDNS nameserver. It has configurable SQL statements.

%package	backend-ldap
Summary:	LDAP backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-ldap
This package contains a LDAP backend for the PowerDNS nameserver.

%package	backend-sqlite3
Summary:	SQLite3 backend for %{name}
Group:		System/Servers
Provides:	pdns-backend-sqlite = %{version}-%{release}
Obsoletes:	pdns-backend-sqlite
Requires:	%{name} = %{version}

%description	backend-sqlite3
This package contains a SQLite3 backend for the PowerDNS nameserver.

%package	backend-geo
Summary:	GEO backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-geo
This package contains a geo backend for the PowerDNS nameserver.

%package	backend-lua
Summary:	LUA backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-lua
This package contains a LUA backend for the PowerDNS nameserver.

%package	backend-odbc
Summary:	ODBC backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-odbc
This package contains a ODBC backend for the PowerDNS nameserver.

%prep

%setup -q -n pdns-%{version} -a1
%patch0 -p0
%patch1 -p0
%patch2 -p0

cp %{SOURCE2} pdns/
cp %{SOURCE3} modules/luabackend/

%build
touch NEWS AUTHORS
autoreconf -fi

export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/powerdns \
    --libdir=%{_libdir}/powerdns \
    --with-socketdir=/var/run/powerdns \
    --with-dynmodules="gmysql gpgsql pipe ldap geo godbc gsqlite3 lua" \
    --with-modules="" \
    --with-mysql=%{_prefix} --with-mysql-lib=%{_libdir} --with-mysql-includes=%{_includedir} \
    --with-pgsql=%{_prefix} --with-pgsql-lib=%{_libdir} --with-pgsql-includes=%{_includedir} \
    --with-sqlite=%{_prefix} --with-sqlite-lib=%{_libdir} --with-sqlite-includes=%{_includedir} \
    --with-unixodbc=%{_prefix} --with-unixodbc-lib=%{_libdir} --with-unixodbc-includes=%{_includedir}

# why is this nessesary all of a sudden?
#find . -type f -name "Makefile" | xargs perl -pi -e "s|-pthread|-lpthread|g"

# parallell build's broken now?
%make

# this might work someday..., meanwhile use S1
#pushd pdns/docs
#    make
#popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%makeinstall_std

install -d %{buildroot}/var/run/powerdns

# fix the config
mv %{buildroot}%{_sysconfdir}/powerdns/pdns.conf-dist %{buildroot}%{_sysconfdir}/powerdns/pdns.conf

cat >> %{buildroot}%{_sysconfdir}/powerdns/pdns.conf << EOF
module-dir=%{_libdir}/powerdns
socket-dir=/var/run/powerdns
setuid=powerdns
setgid=powerdns
launch=bind
#recursor=127.0.0.1:5300
EOF

chmod 600 %{buildroot}%{_sysconfdir}/powerdns/pdns.conf

# install sysv scripts
install -d %{buildroot}%{_initrddir}
install -m755 pdns/pdns %{buildroot}%{_initrddir}/powerdns

# cleanup
rm -f %{buildroot}%{_libdir}/powerdns/*.*a

%pre
%_pre_useradd powerdns /var/lib/powerdns /bin/false

%post
%_post_service powerdns

%preun
%_preun_service powerdns

%postun
%_postun_userdel powerdns

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog HACKING INSTALL README TODO rtfm.powerdns.com
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/powerdns/pdns.conf
%attr(0755,root,root) %{_initrddir}/powerdns
%dir %{_sysconfdir}/powerdns
%dir %{_libdir}/powerdns
%dir %attr(0755,powerdns,powerdns) /var/run/powerdns
%{_bindir}/dnsreplay
%{_bindir}/pdns_control
%{_bindir}/pdnssec
%{_bindir}/zone2ldap
%{_bindir}/zone2sql
%{_sbindir}/pdns_server
%{_mandir}/man8/pdns_control.8*
%{_mandir}/man8/pdns_server.8*
%{_mandir}/man8/zone2sql.8*

%files backend-pipe
%defattr(-,root,root)
%{_libdir}/powerdns/libpipebackend.so

%files backend-mysql
%defattr(-,root,root)
%{_libdir}/powerdns/libgmysqlbackend.so

%files backend-pgsql
%defattr(-,root,root)
%{_libdir}/powerdns/libgpgsqlbackend.so

%files backend-ldap
%defattr(-,root,root)
%{_libdir}/powerdns/libldapbackend.so

%files backend-sqlite3
%defattr(-,root,root)
%{_libdir}/powerdns/libgsqlite3backend.so

%files backend-geo
%defattr(-,root,root)
%doc modules/geobackend/README
%{_libdir}/powerdns/libgeobackend.so

%files backend-lua
%defattr(-,root,root)
%doc modules/luabackend/README
%{_libdir}/powerdns/libluabackend.so

%files backend-odbc
%defattr(-,root,root)
%{_libdir}/powerdns/libgodbcbackend.so
