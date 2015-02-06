%if %mandriva_branch == Cooker
# Cooker
%define release 2
%else
# Old distros
%define subrel 1
%define release 1
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


%changelog
* Wed Jan 25 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-1
+ Revision: 768359
- 3.0.1

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.9.22-9
+ Revision: 645856
- relink against libmysqlclient.so.18

* Sun Jan 02 2011 Funda Wang <fwang@mandriva.org> 2.9.22-8mdv2011.0
+ Revision: 627490
- fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against mysql-5.5.8 libs, again
    - rebuilt against mysql-5.5.8 libs

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 2.9.22-5mdv2011.0
+ Revision: 614490
- the mass rebuild of 2010.1 packages

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 2.9.22-4mdv2010.1
+ Revision: 507503
- rebuild

* Mon Oct 05 2009 Oden Eriksson <oeriksson@mandriva.com> 2.9.22-3mdv2010.0
+ Revision: 454065
- added a gcc44 patch from fedora
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Mar 06 2009 Michael Scherer <misc@mandriva.org> 2.9.22-1mdv2009.1
+ Revision: 349923
- update to 2.9.22
- remove patch 1 about adding -avoid-version, applied upstream
- remove patch 2 for gcc4.3, not needed anymore
- remove patch 3, not needed anymore
- add patch 4, to fix format sting error

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.21.2-2mdv2009.1
+ Revision: 311314
- rebuilt against mysql-5.1.30 libs

* Tue Nov 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.21.2-1mdv2009.1
+ Revision: 304248
- 2.9.21.2 (Major security fixes)

* Sat Sep 13 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.21.1-2mdv2009.0
+ Revision: 284546
- added P3 to fix build against latest boost

* Sat Aug 09 2008 Michael Scherer <misc@mandriva.org> 2.9.21.1-1mdv2009.0
+ Revision: 270058
- new version, and fix building with new pgsql policy

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.21-4mdv2009.0
+ Revision: 209732
- added a gcc43 patch from fedora
- added lsb header and other fixes in the init script

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.9.21-3mdv2008.1
+ Revision: 171019
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.21-2mdv2008.1
+ Revision: 142106
- fix build
- drop the xdb backend, not recently tested
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Apr 23 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9.21-1mdv2008.0
+ Revision: 17247
- 2.9.21


* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9.20-4mdv2007.0
+ Revision: 110707
- rebuilt against new postgresql libs
- remove lies in the description

* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.20-3mdv2007.1
+ Revision: 93708
- Import pdns

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.20-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Thu May 25 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.20-2mdk
- move the recursor to a stand alone package

* Sat Apr 22 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.20-1mdk
- 2.9.20
- drop upstream patches; P10-P17

* Tue Jan 24 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.19-3mdk
- added debian patches (P10-P17)

* Fri Nov 18 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.19-2mdk
- rebuilt against openssl-0.9.8a

* Tue Nov 01 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.19-1mdk
- 2.9.19 (Major bugfixes)
- new docs (S1)
- fix deps
- drop upstream patches; P2

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.18-3mdk
- rebuilt against MySQL-5.0.15

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.18-2mdk
- rebuilt against new openldap-2.3.6 libs
- pass "-DLDAP_DEPRECATED" to the CFLAGS

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.18-1mdk
- 2.9.18
- rediff P1
- drop upstream applied patches (P2,P3)
- renamed to pdns-*
- fix deps
- added P2 from svn to make it compile with gcc4
- updated the manual (S1)

* Thu May 05 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.17-7mdk
- lib64 fixes
- added P3 to make it build on x86_64 (vdanen)

* Thu Apr 21 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.17-6mdk
- rebuilt against new postgresql libs
- rpmlint fixes

* Tue Feb 08 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.9.17-5mdk
- rebuild for ldap2.2_7

* Fri Feb 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-4mdk
- rebuilt against new openldap libs

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-3mdk
- rebuilt against MySQL-4.1.x and PostgreSQL-8.x system libs

* Thu Jan 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-2mdk
- added the forgotten geo backend sub package
- added new docs

* Wed Jan 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-1mdk
- 2.9.17
- rediffed P1 & P2
- drop P3, it's included

* Sun Aug 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.16-2mdk
- rebuilt against new deps and with gcc v3.4.x
- remove obsolete pq++ requirements (new P2)
- added P3
- use libtool magic
- misc spec file fixes

* Sat Apr 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.16-1mdk
- 2.9.16
- rediffed P1

