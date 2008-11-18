Summary:	Versatile Database Driven Nameserver
Name:		pdns
Version:	2.9.21.2
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/pdns-%{version}.tar.gz
# wget -rm http://rtfm.powerdns.com
Source1:	rtfm.powerdns.com.tar.bz2
Patch0:		pdns-2.9.7-init.patch
Patch1:		pdns-2.9.18-avoid-version.diff
Patch2:		%{name}-gcc43.patch
Patch3:		pdns-boost_fix.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	mysql-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	boost-devel
#BuildRequires:	docbook-utils-pdf
Provides:	nameserver powerdns PowerDNS
Obsoletes:	nameserver powerdns PowerDNS
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
Provides:	PowerDNS-backend-pipe
Obsoletes:	PowerDNS-backend-pipe
Requires:	%{name} = %{version}

%description	backend-pipe
This package contains the pipe backend for the PowerDNS nameserver. This
allows PowerDNS to retrieve domain info from a process that accepts
questions on stdin and returns answers on stdout. 

%package	backend-mysql
Summary:	MySQL backend for %{name}
Group:		System/Servers
Provides:	PowerDNS-backend-mysql
Obsoletes:	PowerDNS-backend-mysql
Requires:	%{name} = %{version}

%description	backend-mysql
This package contains a MySQL backend for the PowerDNS nameserver.

%package	backend-pgsql
Summary:	Generic PostgreSQL backend for %{name}
Group:		System/Servers
Provides:	PowerDNS-backend-pgsql
Obsoletes:	PowerDNS-backend-pgsql
Requires:	%{name} = %{version}

%description	backend-pgsql
This package contains a generic PostgreSQL backend 
for the PowerDNS nameserver. It has configurable SQL statements.

%package	backend-ldap
Summary:	LDAP backend for %{name}
Group:		System/Servers
Provides:	PowerDNS-backend-ldap
Obsoletes:	PowerDNS-backend-ldap
Requires:	%{name} = %{version}

%description	backend-ldap
This package contains a LDAP backend for the PowerDNS nameserver.

%package	backend-sqlite
Summary:	SQLite backend for %{name}
Group:		System/Servers
Provides:	PowerDNS-backend-sqlite
Obsoletes:	PowerDNS-backend-sqlite
Requires:	%{name} = %{version}

%description	backend-sqlite
This package contains a SQLite backend for the PowerDNS nameserver.

%package	backend-geo
Summary:	GEO backend for %{name}
Group:		System/Servers
Provides:	PowerDNS-backend-geo
Obsoletes:	PowerDNS-backend-geo
Requires:	%{name} = %{version}

%description	backend-geo
This package contains a geo backend for the PowerDNS nameserver.

%package	devel
Summary:	Development headers and libraries for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	%{name}-backend-pipe = %{version}
Requires:	%{name}-backend-mysql = %{version}
Requires:	%{name}-backend-pgsql = %{version}
Requires:	%{name}-backend-ldap = %{version}
Requires:	%{name}-backend-sqlite = %{version}
Provides:	PowerDNS-devel
Obsoletes:	PowerDNS-devel

%description	devel
Development headers and libraries for %{name}

%prep

%setup -q -n pdns-%{version} -a1
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# lib64 fix
find -type f -name "configure.in" | xargs perl -pi -e "s|/lib/|/%{_lib}/|g"
find -type f -name "configure.in" | xargs perl -pi -e "s|/lib\ |/%{_lib}\ |g"
find -type f -name "configure.in" | xargs perl -pi -e "s|/lib\"|/%{_lib}\"|g"

%build
#%%define __libtoolize /bin/true
export WANT_AUTOCONF_2_5=1
touch NEWS AUTHORS
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --copy --add-missing

export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/powerdns \
    --libdir=%{_libdir}/powerdns \
    --with-socketdir=/var/run/powerdns \
    --with-dynmodules="gmysql gpgsql pipe ldap gsqlite geo" \
    --with-modules="" \
    --with-mysql=%{_prefix} \
    --with-sqlite=%{_prefix} \
    --with-sqlite-includes=%{_includedir}

# why is this nessesary all of a sudden?
#find . -type f -name "Makefile" | xargs perl -pi -e "s|-pthread|-lpthread|g"

# parallell build's broken now?
make

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
%{_bindir}/pdns_control
%{_bindir}/zone2sql
%{_bindir}/zone2ldap
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

%files backend-sqlite
%defattr(-,root,root)
%{_libdir}/powerdns/libgsqlitebackend.so

%files backend-geo
%defattr(-,root,root)
%doc modules/geobackend/README
%{_libdir}/powerdns/libgeobackend.so

%files devel
%defattr(-,root,root)
#%{_libdir}/powerdns/*.so
%{_libdir}/powerdns/*.la
%{_libdir}/powerdns/*.a
