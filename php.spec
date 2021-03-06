# TODO 5.5:
# - enable --with-fpm-systemd, but ensure it checks for sd_booted()
# - build with system libgd 2.1, see 73c5128
# TODO 5.4:
# - check php-sapi-ini-file.patch for safe mode removal
# - update imap annotations patch (needs api porting)
# - update imap myrights patch (needs api porting)
# --with-libmbfl=DIR      MBSTRING: Use external libmbfl.  DIR is the libmbfl base install directory BUNDLED
# --with-onig=DIR         MBSTRING: Use external oniguruma. DIR is the oniguruma install prefix.
# NOTE: mysqlnd does not support ssl or compression (see FAQ at http://dev.mysql.com/downloads/connector/php-mysqlnd/)
# UNPACKAGED EXTENSION NOTES:
# - com_dotnet is Win32-only
# TODO:
# - fileinfo extension bundles magic db in library: data_file.c (dump of magic.mgc) is 14M
#   - 2.3M fileinfo.so php54-fileinfo-5.4.6-0.15.x86_64
#   - 2.3M fileinfo.so php-fileinfo-5.3.16-1.x86_64
#   -  13K fileinfo.so php-pecl-fileinfo-1.0.4-8.amd64
# - ttyname_r() misdetected http://bugs.php.net/bug.php?id=48820
# - wddx: restore session support (not compiled in due DL extension check)
# - deal with modules removed from php and not moved to PECL, still not obsoleted anywhere
#   - removed from php 5.0 (currently in php4):
#   db [pecl-svn], hyperwave [pecl-svn], java [pecl-svn], mcal [pecl-svn], qtdom [pecl-svn]
#   - removed from php 5.1:
#   oracle [pecl-svn]
#   - removed from php 5.2:
#   filepro [pecl-svn], hwapi [pecl-svn]
# - make additional headers and checking added by mail patch configurable
# - modularize standard (output from pure php -m)?
# - lib64 patch obsolete by $PHP_LIBDIR ?
# - WARNING: Phar: sha256/sha512 signature support disabled if ext/hash is
#   built shared, also PHAR_HAVE_OPENSSL is false if openssl is built shared.
#   make it runtime dep and add Suggests (or php warning messages)
# - some mods should be shared:
#$ php -m
# [PHP Modules]
#+Core
# date
#+ereg
# libxml
# Reflection
#
# Conditional build:
%bcond_with	interbase_inst	# use InterBase install., not Firebird	(BR: proprietary libs)
%bcond_with	oci		# with Oracle oci8 extension module	(BR: proprietary libs)
%bcond_without	instantclient	# build Oracle oci8 extension module against oracle-instantclient package
%bcond_with	system_gd	# with system gd (imageantialias function is missing then)
%bcond_with	system_libzip	# with system libzip (reported broken currently)
%bcond_with	default_php	# use this PHP as default PHP in distro
%bcond_without	curl		# without CURL extension module
%bcond_without	enchant		# without Enchant extension module
%bcond_without	filter		# without filter extension module
%bcond_without	imap		# without IMAP extension module
%bcond_without	interbase	# without InterBase extension module
%bcond_without	intl		# without Intl extension module
%bcond_without	kerberos5	# without Kerberos5 support
%bcond_without	litespeed	# build litespeed module
%bcond_without	ldap		# without LDAP extension module
%bcond_without	mhash		# without mhash extension (supported by hash extension)
%bcond_without	mm		# without mm support for session storage
%bcond_without	mssql		# without MS SQL extension module
# don't turn it on by default; see TODO item for mysqlnd in this spec
%bcond_with	mysqlnd		# with mysqlnd support in mysql related extensions
%bcond_without	mysqli		# without mysqli support (Requires mysql > 4.1)
%bcond_without	odbc		# without ODBC extension module
%bcond_without	opcache		# without Enable Zend OPcache extension support
%bcond_without	openssl		# without OpenSSL support and OpenSSL extension (module)
%bcond_without	pcre		# without PCRE extension module
%bcond_without	pdo_sqlite	# without PDO SQLite extension module
%bcond_without	pgsql		# without PostgreSQL extension module
%bcond_without	phar		# without phar extension module
%bcond_without	pspell		# without pspell extension module
%bcond_without	recode		# without recode extension module
%bcond_without	snmp		# without SNMP extension module
%bcond_without	sqlite2		# without SQLite extension module
%bcond_without	sqlite3		# without SQLite3 extension module
%bcond_without	sybase_ct	# without Sybase-CT extension module
%bcond_without	tidy		# without Tidy extension module
%bcond_without	webp		# Without WebP support in GD extension (imagecreatefromwebp)
%bcond_without	wddx		# without WDDX extension module
%bcond_without	xmlrpc		# without XML-RPC extension module
%bcond_without	apache1		# disable building Apache 1.3.x SAPI
%bcond_without	apache2		# disable building Apache 2.x SAPI
%bcond_with	zts		# Zend Thread Safety
%bcond_without	cgi		# disable CGI/FCGI SAPI
%bcond_without	fpm		# disable FPM
%bcond_without	embed		# disable Embedded API
%bcond_without	suhosin		# with suhosin patch
%bcond_with	tests		# default off; test process very often hangs on builders, approx run time 45m; perform "make test"
%bcond_with	gcov		# Enable Code coverage reporting
%bcond_with	type_hints	# experimental support for strict typing/casting

%define apxs1		/usr/sbin/apxs1
%define	apxs2		/usr/sbin/apxs

# disable all sapis
%if %{with gcov}
%undefine	with_apache1
%undefine	with_apache2
%undefine	with_cgi
%undefine	with_litespeed
%endif

# mm is not thread safe
%if %{with zts}
%undefine	with_mm
%endif

%ifnarch %{ix86} %{x8664} x32 sparc sparcv9 alpha
# ppc disabled (broken on th-ppc)
%undefine	with_interbase
%endif

%ifnarch %{ix86} %{x8664} x32
# unsupported, see sapi/cgi/fpm/fpm_atomic.h
%undefine	with_fpm
%endif

%if 0
%if %{without apache1} && %{without apache2}
ERROR: You need to select at least one Apache SAPI to build shared modules.
%endif
%endif

# filter depends on pcre
%if %{without pcre}
%undefine	with_filter
%endif

%define		rel	1
%define		orgname	php
%define		ver_suffix 55
%define		php_suffix %{!?with_default_php:%{ver_suffix}}
Summary:	PHP: Hypertext Preprocessor
Summary(fr.UTF-8):	Le langage de script embarque-HTML PHP
Summary(pl.UTF-8):	Język skryptowy PHP
Summary(pt_BR.UTF-8):	A linguagem de script PHP
Summary(ru.UTF-8):	PHP Версии 5 - язык препроцессирования HTML-файлов, выполняемый на сервере
Summary(uk.UTF-8):	PHP Версії 5 - мова препроцесування HTML-файлів, виконувана на сервері
Name:		%{orgname}%{php_suffix}
Version:	5.5.20
Release:	%{rel}%{?with_type_hints:.th}
Epoch:		4
License:	PHP
Group:		Libraries
Source0:	http://www.php.net/distributions/%{orgname}-%{version}.tar.xz
# Source0-md5:	51377838dfee2d7bb4715674ac715394
Source2:	%{orgname}-mod_%{orgname}.conf
Source3:	%{orgname}-cgi-fcgi.ini
Source4:	%{orgname}-apache.ini
Source5:	%{orgname}-cli.ini
# Taken from: http://browsers.garykeith.com/downloads.asp
Source9:	%{orgname}_browscap.ini
Source10:	%{orgname}-fpm.init
Source11:	%{orgname}-fpm.logrotate
Source12:	%{orgname}-branch.sh
Source13:	dep-tests.sh
Source14:	skip-tests.sh
Patch0:		%{orgname}-shared.patch
Patch1:		%{orgname}-pldlogo.patch
Patch2:		%{orgname}-mail.patch
Patch3:		%{orgname}-link-libs.patch
Patch4:		%{orgname}-libpq_fs_h_path.patch
Patch5:		%{orgname}-filter-shared.patch
Patch6:		%{orgname}-build_modules.patch
Patch7:		%{orgname}-sapi-ini-file.patch

Patch10:	%{orgname}-ini.patch
Patch11:	embed.patch
%if %{with type_hints}
Patch12:	http://ilia.ws/patch/type_hint_53_v2.txt
%endif
Patch14:	%{orgname}-no_pear_install.patch
Patch17:	%{orgname}-readline.patch
Patch18:	%{orgname}-nohttpd.patch
Patch20:	%{orgname}-uint32_t.patch
Patch21:	%{orgname}-dba-link.patch
Patch22:	%{orgname}-both-apxs.patch
Patch23:	%{orgname}-builddir.patch
Patch24:	%{orgname}-zlib-for-getimagesize.patch
Patch25:	%{orgname}-stupidapache_version.patch
Patch26:	%{orgname}-pear.patch
Patch27:	%{orgname}-config-dir.patch
Patch29:	%{orgname}-fcgi-graceful.patch
Patch31:	%{orgname}-fcgi-error_log-no-newlines.patch
Patch34:	%{orgname}-libtool.patch
Patch35:	%{orgname}-tds.patch
Patch36:	%{orgname}-mysql-charsetphpini.patch
Patch37:	%{orgname}-mysqli-charsetphpini.patch
Patch38:	%{orgname}-pdo_mysql-charsetphpini.patch
Patch39:	%{orgname}-use-prog_sendmail.patch
Patch41:	%{orgname}-fpm-config.patch
Patch42:	%{orgname}-fpm-shared.patch
Patch43:	%{orgname}-silent-session-cleanup.patch
Patch44:	%{orgname}-include_path.patch
Patch45:	%{orgname}-imap-annotations.patch
Patch46:	%{orgname}-imap-myrights.patch
Patch47:	suhosin.patch
Patch50:	extension-shared-optional-dep.patch
Patch51:	spl-shared.patch
Patch52:	pcre-shared.patch
Patch53:	fix-test-run.patch
Patch55:	bug-52078-fileinode.patch
Patch59:	%{orgname}-systzdata.patch
Patch60:	%{orgname}-oracle-instantclient.patch
Patch62:	mcrypt-libs.patch
Patch63:	%{orgname}-mysql-nowarning.patch
Patch65:	system-libzip.patch
Patch66:	php-db.patch
Patch67:	mysql-lib-ver-mismatch.patch
Patch68:	x32.patch
Patch69:	fpm-conf-split.patch
URL:		http://www.php.net/
%{?with_interbase:%{!?with_interbase_inst:BuildRequires:	Firebird-devel >= 1.0.2.908-2}}
%{?with_pspell:BuildRequires:	aspell-devel >= 2:0.50.0}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.4d
BuildRequires:	bison
BuildRequires:	bzip2-devel
%{?with_curl:BuildRequires:	curl-devel >= 7.12.0}
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db-devel >= 4.0
BuildRequires:	elfutils-devel
%{?with_enchant:BuildRequires:	enchant-devel >= 1.1.3}
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_system_libzip:BuildRequires:	libzip-devel >= 0.10.1-2}
%{!?with_mysqlnd:BuildRequires:	mysql-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with mssql} || %{with sybase_ct}
BuildRequires:	freetds-devel >= 0.82
%endif
BuildRequires:	freetype-devel >= 1:2.5.1
%if %{with system_gd}
BuildRequires:	gd-devel >= 2.1
%endif
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
%{?with_imap:BuildRequires:	imap-devel >= 1:2007e-2}
%{?with_intl:BuildRequires:	libicu-devel >= 4.4}
BuildRequires:	libjpeg-devel
BuildRequires:	libltdl-devel >= 1.4
BuildRequires:	libmcrypt-devel >= 2.4.4
BuildRequires:	libpng-devel >= 1.0.8
%{?with_webp:BuildRequires:	libvpx-devel}
BuildRequires:	tokyocabinet-devel
%if "%{pld_release}" != "ac"
BuildRequires:	libtool >= 2:2.2
%else
BuildRequires:	libtool >= 1.4.3
%endif
BuildRequires:	libxml2-devel >= 1:2.7.6-4
BuildRequires:	libxslt-devel >= 1.1.0
%{?with_mm:BuildRequires:	mm-devel >= 1.3.0}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%if %{with openssl} || %{with ldap}
BuildRequires:	openssl-devel >= 0.9.7d
%endif
%{?with_gcov:BuildRequires:	lcov}
%{?with_snmp:%{?with_tests:BuildRequires:	mibs-net-snmp}}
%{?with_snmp:BuildRequires:	net-snmp-devel >= 5.0.7}
%{?with_oci:%{?with_instantclient:BuildRequires:	oracle-instantclient-devel}}
BuildRequires:	pam-devel
%{?with_pcre:BuildRequires:	pcre-devel >= 8.10}
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel >= 7.2}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	readline-devel
%{?with_recode:BuildRequires:	recode-devel >= 3.5d-3}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-build >= 4.4.0
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with sqlite3} || %{with pdo_sqlite}
BuildRequires:	sqlite3-devel >= 3.3.9
%endif
BuildRequires:	t1lib-devel
%{?with_tidy:BuildRequires:	tidy-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel}
%{?with_xmlrpc:BuildRequires:	xmlrpc-epi-devel >= 0.54.1}
BuildRequires:	zlib-devel >= 1.0.9
%if %{with apache1}
BuildRequires:	apache1-devel
%endif
%if %{with apache2}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	apr-util-devel >= 1:1.0.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		php_sysconfdir		/etc/%{name}
%define		php_extensiondir	%{_libdir}/%{name}
%define		_sysconfdir			%{php_sysconfdir}

# must be in sync with source. extra check ensuring that it is so is done in %%build
%define		php_api_version		20121113
%define		zend_module_api		20121212
%define		zend_extension_api	220121212
%define		php_pdo_api_version	20080721

# Extension versions
%define		bz2ver		1.0
%define		enchantver	1.1.0
%define		fileinfover	1.0.5
%define		hashver		1.0
%define		intlver		1.1.0
%define		jsonver		1.2.1
%define		opcachever	7.0.4-dev
%define		pharver		2.0.2
%define		sqlite3ver	0.7-dev
%define		zipver		1.11.0

%define		_zend_zts		%{!?with_zts:0}%{?with_zts:1}
%define		php_debug		%{!?debug:0}%{?debug:1}

%if %{with gcov}
%undefine	with_ccache
%endif

%if %{with oci}
# ORACLE_HOME is required for oci8 ext to build
%define _preserve_env %_preserve_env_base ORACLE_HOME
%endif

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. The
mod_php module enables the Apache web server to understand and process
the embedded PHP language in web pages. This package contains PHP
version %{version}.

%description -l fr.UTF-8
PHP est un langage de script embarque dans le HTM. PHP essaye de
rendre simple aux developpeurs d'ecrire des pages web generees
dynamiquement. PHP incorpore egalement une integration avec plusieurs
systemes de gestion de bases de donnees commerciaux et
non-connerciaux, qui rent facile la creation de pages web liees avec
des bases de donnees. L'utilisation la plus commune de PHP est
probablement en remplacement de scripts CGI. Le module mod_php permet
au serveur web Apache de comprendre et de traiter le langage PHP
integre dans des pages web. Ce package contient PHP version
%{version}.

%description -l pl.UTF-8
PHP jest językiem skryptowym, którego polecenia umieszcza się w
plikach HTML. Jest próbą ułatwienia programistom pisania dynamicznie
generowanych stron WWW. Oferuje także wbudowaną integrację z bazami
danych dla kilku komercyjnych i niekomercyjnych systemów baz danych,
co czyni tworzenie stron korzystających z baz danych w miarę łatwym.
Najczęściej PHP jest używany prawdopodobnie jako zamiennik skryptów
CGI. Moduł mod_php pozwala serwerowi WWW Apache rozumieć i przetwarzać
język PHP osadzony w stronach. Ten pakiet zawiera PHP w wersji
%{version}.

%description -l pt_BR.UTF-8
PHP: Preprocessador de Hipertexto versão 4 é uma linguagem script
embutida em HTML. Muito de sua sintaxe é emprestada de C, Java e Perl,
com algumas características únicas, específicas ao PHP. O objetivo da
linguagem é permitir que desenvolvedores web escrevam páginas
dinamicamente geradas de forma rápida.

%description -l ru.UTF-8
PHP - это язык написания скриптов, встраиваемых в HTML-код. PHP
предлагает интерграцию с множеством СУБД, поэтому написание скриптов
для работы с базами данных относительно просто. Наиболее популярное
использование PHP - замена для CGI скриптов.

%description -l uk.UTF-8
PHP - це мова написання скриптів, що вбудовуються в HTML-код. PHP
пропонує інтеграцію з багатьма СУБД, тому написання скриптів для
роботи з базами даних є доволі простим. Найбільш популярне
використання PHP - заміна для CGI скриптів.

%package -n apache1-mod_%{name}
Summary:	PHP DSO module for Apache 1.3.x
Summary(pl.UTF-8):	Moduł DSO (Dynamic Shared Object) PHP dla Apache 1.3.x
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	apache1(EAPI) >= 1.3.33-2
Requires:	apache1-mod_mime
Provides:	webserver(php) = %{version}
Obsoletes:	apache-mod_php < 1:4.1.1
Obsoletes:	apache1-mod_php < 4:5.3.28-7
Obsoletes:	phpfi

%description -n apache1-mod_%{name}
PHP as DSO module for Apache 1.3.x.

%description -n apache1-mod_%{name} -l pl.UTF-8
PHP jako moduł DSO (Dynamic Shared Object) dla Apache 1.3.x.

%package -n apache-mod_%{name}
Summary:	PHP DSO module for Apache 2.x
Summary(pl.UTF-8):	Moduł DSO (Dynamic Shared Object) PHP dla Apache 2.x
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-mod_mime
Provides:	webserver(php) = %{version}
Obsoletes:	apache-mod_php < 4:5.3.28-7
Obsoletes:	phpfi

%description -n apache-mod_%{name}
PHP as DSO module for Apache 2.x.

%description -n apache-mod_%{name} -l pl.UTF-8
PHP jako moduł DSO (Dynamic Shared Object) dla Apache 2.x.

%package litespeed
Summary:	PHP for litespeed HTTP server
Summary(pl.UTF-8):	PHP dla serwera HTTP litespeed
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(litespeed)
Provides:	webserver(php) = %{version}
Obsoletes:	php-litespeed < 4:5.3.28-7

%description litespeed
PHP for litespeed HTTP server.

%description litespeed -l pl.UTF-8
PHP dla serwera HTTP litespeed.

%package cgi
Summary:	PHP as CGI/FastCGI program
Summary(pl.UTF-8):	PHP jako program CGI/FastCGI
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	%{name}-fcgi = %{epoch}:%{version}-%{release}
Provides:	php(cgi)
Provides:	php(fcgi)
Provides:	webserver(php) = %{version}
Obsoletes:	php-cgi < 4:5.3.28-7
Obsoletes:	php-fcgi < 4:5.3.0
%if "%{pld_release}" != "ac"
Conflicts:	logrotate < 3.8.0
%endif

%description cgi
PHP as CGI or FastCGI program.

%description cgi -l pl.UTF-8
PHP jako program CGI lub FastCGI.

%package cli
Summary:	PHP as CLI interpreter
Summary(pl.UTF-8):	PHP jako interpreter działający z linii poleceń
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	php-cli < 4:5.3.28-7

%description cli
PHP as CLI interpreter.

%description cli -l pl.UTF-8
PHP jako interpreter działający z linii poleceń.

%package embedded
Summary:	PHP library for embedding in applications
Summary(pl.UTF-8):	Biblioteka PHP do osadzania w aplikacjach
Group:		Libraries
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	php-embedded < 4:5.3.28-7

%description embedded
The php-embedded package contains a library which can be embedded into
applications to provide PHP scripting language support.

%description embedded -l pl.UTF-8
Ten pakiet zawiera bibliotekę, którą można osadzać w aplikacjach w
celu obsługi PHP jako języka skryptowego.

%package program
Summary:	/usr/bin/php symlink
Summary(pl.UTF-8):	Dowiązanie symboliczne /usr/bin/php
Group:		Development/Languages/PHP
Requires:	%{name}-cli = %{epoch}:%{version}-%{release}
Obsoletes:	/usr/bin/php
Obsoletes:	php-program < 4:5.3.28-7

%description program
Package providing /usr/bin/php symlink to PHP CLI.

%description program -l pl.UTF-8
Pakiet dostarczający dowiązanie symboliczne /usr/bin/php do PHP CLI.

%package fpm
Summary:	PHP FastCGI Process Manager
Summary(pl.UTF-8):	PHP FastCGI Process Manager - zarządca procesów FastCGI
Group:		Development/Languages/PHP
URL:		http://www.php-fpm.org/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	rc-scripts
Provides:	php(fpm)
Provides:	user(http)
Provides:	webserver(php) = %{version}
Obsoletes:	php-fpm < 4:5.3.28-7

%description fpm
PHP FastCGI Process Manager.

%description fpm -l pl.UTF-8
PHP FastCGI Process Manager - zarządca procesów FastCGI.

%package common
Summary:	Common files needed by both Apache modules and CGI/CLI SAPIs
Summary(pl.UTF-8):	Wspólne pliki dla modułu Apache'a i programu CGI
Summary(ru.UTF-8):	Разделяемые библиотеки для PHP
Summary(uk.UTF-8):	Бібліотеки спільного використання для PHP
Group:		Libraries
Requires(post):	sed >= 4.0
# because of dlclose() bugs in glibc <= 2.3.4 causing SEGVs on exit
Requires:	glibc >= 6:2.3.5
Requires:	php-dirs >= 1.4
Requires:	rpm-whiteout >= 1.28
Requires:	tzdata
Provides:	%{name}(debug) = %{php_debug}
Provides:	%{name}(modules_api) = %{php_api_version}
Provides:	%{name}(thread-safety) = %{_zend_zts}
Provides:	%{name}(zend_extension_api) = %{zend_extension_api}
Provides:	%{name}(zend_module_api) = %{zend_module_api}
Provides:	%{name}-core
Provides:	%{name}-date
Provides:	%{name}-ereg
Provides:	%{name}-reflection
Provides:	%{name}-standard
Provides:	php(core) = %{version}
Provides:	php(date)
Provides:	php(ereg)
Provides:	php(libxml)
Provides:	php(reflection)
Provides:	php(standard)
%{!?with_mysqlnd:Obsoletes:	php-mysqlnd}
%{?with_pcre:%requires_ge_to	pcre pcre-devel}
Obsoletes:	php-common < 4:5.3.28-7
Obsoletes:	php-pecl-domxml
Conflicts:	php4-common < 3:4.4.4-8
Conflicts:	php55-common < 4:5.5.10-4
Conflicts:	rpm < 4.4.2-0.2

%description common
Common files needed by both Apache modules and CGI/CLI SAPIs.

%description common -l pl.UTF-8
Wspólne pliki dla modułu Apache'a i programu CGI.

%description common -l ru.UTF-8
Этот пакет содержит общие файлы для разных вариантов реализации PHP
(самодостаточной и в качестве модуля Apache).

%description common -l uk.UTF-8
Цей пакет містить спільні файли для різних варіантів реалізації PHP
(самодостатньої та в якості модуля Apache).

%package devel
Summary:	Files for PHP modules development
Summary(pl.UTF-8):	Pliki do kompilacji modułów PHP
Summary(pt_BR.UTF-8):	Arquivos de desenvolvimento para PHP
Summary(ru.UTF-8):	Пакет разработки для построения расширений PHP
Summary(uk.UTF-8):	Пакет розробки для побудови розширень PHP
Group:		Development/Languages/PHP
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	autoconf >= 2.13
Requires:	automake
%if "%{pld_release}" != "ac"
Requires:	libtool >= 2:2.2
%else
Requires:	libtool
%endif
%{?with_pcre:Requires:	pcre-devel >= 8.10}
Requires:	shtool
Provides:	php-devel = %{epoch}:%{version}-%{release}
Obsoletes:	php-devel
Obsoletes:	php-pear-devel
Obsoletes:	php4-devel
Obsoletes:	php52-devel
Obsoletes:	php53-devel
Obsoletes:	php54-devel

%description devel
The php-devel package lets you compile dynamic extensions to PHP.
Included here is the source for the PHP extensions. Instead of
recompiling the whole PHP binary to add support for, say, oracle,
install this package and use the new self-contained extensions
support. For more information, read the file
README.SELF-CONTAINED-EXTENSIONS.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do kompilacji modułów PHP. Zamiast
rekompilować całe PHP aby dodać obsługę np. oracle, można przy użyciu
tego pakietu skompilować samodzielne rozszerzenie. Więcej informacji o
samodzielnych rozszerzeniach można znaleźć w pliku
README.SELF-CONTAINED-EXTENSIONS.

%description devel -l pt_BR.UTF-8
Este pacote contém arquivos usados no desenvolvimento de programas ou
módulos PHP.

%description devel -l ru.UTF-8
Пакет php-devel дает возможность компилировать динамические расширения
PHP. Пакет включает исходный код этих расширений. Вместо повторной
компиляции бинарного файла PHP для добавления, например, поддержки
oracle, установите этот пакет для компилирования отдельных расширений.
Подробности - в файле README.SELF-CONTAINED-EXTENSIONS.

%description devel -l uk.UTF-8
Пакет php-devel дає можливість компілювати динамічні розширення PHP.
До пакету включено вихідний код для розширень. Замість повторної
компіляції бінарного файлу PHP для додання, наприклад, підтримки
oracle, встановіть цей пакет для компіляції окремих розширень.
Детальніша інформація - в файлі README.SELF-CONTAINED-EXTENSIONS.

%package bcmath
Summary:	bcmath extension module for PHP
Summary(pl.UTF-8):	Moduł bcmath dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.bc.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(bcmath)
Obsoletes:	php-bcmath < 4:5.3.28-7

%description bcmath
This is a dynamic shared object (DSO) for PHP that will add bc style
precision math functions support.

%description bcmath -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z dokładnych funkcji
matematycznych takich jak w programie bc.

%package bz2
Summary:	Bzip2 extension module for PHP
Summary(pl.UTF-8):	Moduł bzip2 dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.bzip2.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(bz2) = %{bz2ver}
Provides:	php(bzip2)
Provides:	php-bzip2 = %{epoch}:%{version}-%{release}
Obsoletes:	php-bz2 < 4:5.3.28-7
Obsoletes:	php-bzip2 < 4:5.2.14-3
Obsoletes:	php-pecl-bz2 < %{bz2ver}

%description bz2
This is a dynamic shared object (DSO) for PHP that will add bzip2
compression support to PHP.

%description bz2 -l pl.UTF-8
Moduł PHP umożliwiający używanie kompresji bzip2.

%package calendar
Summary:	Calendar extension module for PHP
Summary(pl.UTF-8):	Moduł funkcji kalendarza dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.calendar.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(calendar)
Obsoletes:	php-calendar < 4:5.3.28-7

%description calendar
This is a dynamic shared object (DSO) for PHP that will add calendar
support.

%description calendar -l pl.UTF-8
Moduł PHP dodający wsparcie dla kalendarza.

%package ctype
Summary:	ctype extension module for PHP
Summary(pl.UTF-8):	Moduł ctype dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.ctype.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(ctype)
Obsoletes:	php-ctype < 4:5.3.28-7

%description ctype
This is a dynamic shared object (DSO) for PHP that will add ctype
support.

%description ctype -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z funkcji ctype.

%package curl
Summary:	curl extension module for PHP
Summary(pl.UTF-8):	Moduł curl dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.curl.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(curl)
Obsoletes:	php-curl < 4:5.3.28-7

%description curl
This is a dynamic shared object (DSO) for PHP that will add curl
support.

%description curl -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z biblioteki curl.

%package dba
Summary:	DBA extension module for PHP
Summary(pl.UTF-8):	Moduł DBA dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.dba.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(dba)
Obsoletes:	php-dba < 4:5.3.28-7

%description dba
This is a dynamic shared object (DSO) for PHP that will add flat-file
databases (DBA) support.

%description dba -l pl.UTF-8
Moduł dla PHP dodający obsługę dla baz danych opartych na plikach
(DBA).

%package dom
Summary:	DOM extension module for PHP
Summary(pl.UTF-8):	Moduł DOM dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.dom.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(dom)
# it has some compatibility functions
Provides:	%{name}-domxml = %{epoch}:%{version}-%{release}
Provides:	php(domxml)
Obsoletes:	php-dom < 4:5.3.28-7
Obsoletes:	php-domxml <= 3:4.3.8-1

%description dom
This is a dynamic shared object (DSO) for PHP that will add new DOM
support.

%description dom -l pl.UTF-8
Moduł PHP dodający nową obsługę DOM.

%package enchant
Summary:	libenchant binder
Summary(pl.UTF-8):	dowiązania biblioteki libenchant
Group:		Libraries
URL:		http://www.php.net/manual/en/book.exif.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(enchant) = %{enchantver}
Obsoletes:	php-enchant < 4:5.3.28-7
Obsoletes:	php-pecl-enchant < %{enchantver}

%description enchant
Enchant is a binder for libenchant. Libenchant provides a common API
for many spell libraries:
- aspell/pspell (intended to replace ispell)
- hspell (hebrew)
- ispell
- myspell (OpenOffice.org project, mozilla)
- uspell (primarily Yiddish, Hebrew, and Eastern European languages) A
  plugin system allows to add custom spell support.

%description enchant -l pl.UTF-8
Enchant jest dowiązaniem do biblioteki libenchant, która udostępnia
ujednolicone API dla wielu narzędzi sprawdzających pisownię:
- aspell/pspell (w zamierzeniu ma zastąpić ispell)
- hspell (hebrajski)
- ispell
- myspell (projekt OpenOffice.org, mozilla)
- uspell (głównie Jidysz, Hebrajski oraz języki wschodnioeuropejskie)
  System wtyczek pozwala na dodanie wsparcia dla kolejnych narzędzi.

%package exif
Summary:	exif extension module for PHP
Summary(pl.UTF-8):	Moduł exif dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.exif.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(exif)
Obsoletes:	php-exif < 4:5.3.28-7

%description exif
This is a dynamic shared object (DSO) for PHP that will add EXIF tags
support in image files.

%description exif -l pl.UTF-8
Moduł PHP dodający obsługę znaczników EXIF w plikach obrazków.

%package fileinfo
Summary:	libmagic bindings
Summary(pl.UTF-8):	Wiązania do libmagic
Group:		Libraries
URL:		http://www.php.net/manual/en/book.fileinfo.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pcre = %{epoch}:%{version}-%{release}
Provides:	php(fileinfo) = %{fileinfover}
Obsoletes:	php-fileinfo < 4:5.3.28-7
Obsoletes:	php-mime_magic
Obsoletes:	php-pecl-fileinfo < %{fileinfover}

%description fileinfo
This extension allows retrieval of information regarding vast majority
of file. This information may include dimensions, quality, length
etc...

Additionally it can also be used to retrieve the MIME type for a
particular file and for text files proper language encoding.

%description fileinfo -l pl.UTF-8
To rozszerzenie pozwala na uzyskanie informacji dotyczących większości
plików. Informacje mogą zawierać wymiary, jakość, długość itp.

Ponadto rozszerzenie można wykorzystać do odczytania typu MIME danego
pliku oraz kodowania plików tekstowych.

%package filter
Summary:	Extension for safely dealing with input parameters
Summary(pl.UTF-8):	Rozszerzenie do bezpiecznej obsługi danych wejściowych
Group:		Libraries
URL:		http://www.php.net/manual/en/book.filter.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pcre = %{epoch}:%{version}-%{release}
Provides:	php(filter)
Obsoletes:	php-filter < 4:5.3.28-7
Obsoletes:	php-pecl-filter

%description filter
We all know that you should always check input variables, but PHP does
not offer really good functionality for doing this in a safe way. The
Input Filter extension is meant to address this issue by implementing
a set of filters and mechanisms that users can use to safely access
their input data.

%description filter -l pl.UTF-8
Wiadomo, że trzeba zawsze sprawdzać zmienne wejściowe, ale PHP nie
oferuje naprawdę dobrej funkcjonalności do robienia tego w sposób
bezpieczny. Rozszerzenie Input Filter ma rozwiązać ten problem poprzez
zaimplementowanie zestawu filtrów i mechanizmów, których użytkownicy
mogą bezpiecznie używać do dostępu do danych.

%package ftp
Summary:	FTP extension module for PHP
Summary(pl.UTF-8):	Moduł FTP dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.ftp.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(ftp)
Obsoletes:	php-ftp < 4:5.3.28-7

%description ftp
This is a dynamic shared object (DSO) for PHP that will add FTP
support.

%description ftp -l pl.UTF-8
Moduł PHP dodający obsługę protokołu FTP.

%package gd
Summary:	GD extension module for PHP
Summary(pl.UTF-8):	Moduł GD dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.image.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%if %{with system_gd}
Requires:	gd >= 2.1
Requires:	gd(gif)
%endif
Provides:	php(gd)
Obsoletes:	php-gd < 4:5.3.28-7

%description gd
This is a dynamic shared object (DSO) for PHP that will add GD
support, allowing you to create and manipulate images with PHP.

%description gd -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z biblioteki GD, pozwalającej na
tworzenie i obróbkę obrazków.

%package gettext
Summary:	gettext extension module for PHP
Summary(pl.UTF-8):	Moduł gettext dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.gettext.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(gettext)
Obsoletes:	php-gettext < 4:5.3.28-7

%description gettext
This is a dynamic shared object (DSO) for PHP that will add gettext
support.

%description gettext -l pl.UTF-8
Moduł PHP dodający obsługę lokalizacji przez gettext.

%package gmp
Summary:	gmp extension module for PHP
Summary(pl.UTF-8):	Moduł gmp dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.gmp.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(gmp)
Obsoletes:	php-gmp < 4:5.3.28-7

%description gmp
This is a dynamic shared object (DSO) for PHP that will add arbitrary
length number support with GNU MP library.

%description gmp -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z biblioteki gmp do obliczeń na
liczbach o dowolnej długości.

%package hash
Summary:	HASH Message Digest Framework
Summary(pl.UTF-8):	Szkielet do obliczania skrótów wiadomości
Group:		Libraries
URL:		http://www.php.net/manual/en/book.gmp.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(hash) = %{hashver}
%if %{with mhash}
Provides:	php(mhash)
Provides:	php-mhash = %{epoch}:%{version}-%{release}
Obsoletes:	php-mhash < 4:5.3.0
%endif
Obsoletes:	php-hash < 4:5.3.28-7
Obsoletes:	php-pecl-hash < %{hashver}

%description hash
Native implementations of common message digest algorithms using a
generic factory method.

%description hash -l pl.UTF-8
Natywne implementacje popularnych algorytmów obliczania skrótów
wiadomości przy użyciu wspólnego interfejsu.

%package iconv
Summary:	iconv extension module for PHP
Summary(pl.UTF-8):	Moduł iconv dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.iconv.php
Requires:	%{_libdir}/gconv
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	iconv
Provides:	php(iconv)
Obsoletes:	php-iconv < 4:5.3.28-7

%description iconv
This is a dynamic shared object (DSO) for PHP that will add iconv
support.

%description iconv -l pl.UTF-8
Moduł PHP dodający obsługę iconv.

%package imap
Summary:	IMAP extension module for PHP
Summary(pl.UTF-8):	Moduł IMAP dla PHP
Summary(pt_BR.UTF-8):	Um módulo para aplicações PHP que usam IMAP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.imap.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pcre = %{epoch}:%{version}-%{release}
Requires:	imap-lib >= 1:2007e-2
Provides:	php(imap)
Obsoletes:	php-imap < 4:5.3.28-7

%description imap
This is a dynamic shared object (DSO) for PHP that will add IMAP
support.

%description imap -l pl.UTF-8
Moduł PHP dodający obsługę skrzynek IMAP.

%description imap -l pt_BR.UTF-8
Um módulo para aplicações PHP que usam IMAP.

%package interbase
Summary:	InterBase/Firebird database module for PHP
Summary(pl.UTF-8):	Moduł bazy danych InterBase/Firebird dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.ibase.php
%if %{with interbase_inst}
%{?requires_php_extension}
%else
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%endif
Provides:	php(interbase)
Obsoletes:	php-interbase < 4:5.3.28-7

%description interbase
This is a dynamic shared object (DSO) for PHP that will add InterBase
and Firebird database support.

%description interbase -l pl.UTF-8
Moduł PHP umożliwiający dostęp do baz danych InterBase i Firebird.

%package intl
Summary:	Internationalization extension (ICU wrapper)
Summary(pl.UTF-8):	Rozszerzenie do internacjonalizacji (interfejs do ICU)
Group:		Libraries
URL:		http://www.php.net/intl
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(intl) = %{intlver}
Obsoletes:	php-intl < 4:5.3.28-7
Obsoletes:	php-pecl-intl < %{intlver}

%description intl
Internationalization extension (further is referred as Intl) is a
wrapper for ICU library, enabling PHP programmers to perform
UCA-conformant collation and date/time/number/currency formatting in
their scripts.

%description intl -l pl.UTF-8
Rozszerzenie do internacjonalizacji (dalej nazywane Intl) jest
interfejsem do biblioteki ICU, pozwalającym programistom PHP na
wykonywanie w skryptach porównań zgodnych z UCA oraz formatowania
daty/czasu/walut.

%package json
Summary:	PHP C extension for JSON serialization
Summary(pl.UTF-8):	Rozszerzenie C PHP dla serializacji JSON
Group:		Libraries
URL:		http://www.php.net/manual/en/book.json.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(json) = %{jsonver}
Obsoletes:	php-json < 4:5.3.28-7
Obsoletes:	php-pecl-json < %{jsonver}

%description json
php-json is an extremely fast PHP C extension for JSON (JavaScript
Object Notation) serialisation.

%description json -l pl.UTF-8
php-json to bardzo szybkie rozszerzenie C PHP dla serializacji JSON
(JavaScript Object Notation).

%package ldap
Summary:	LDAP extension module for PHP
Summary(pl.UTF-8):	Moduł LDAP dla PHP
Summary(pt_BR.UTF-8):	Um módulo para aplicações PHP que usam LDAP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.ldap.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(ldap)
Obsoletes:	php-ldap < 4:5.3.28-7

%description ldap
This is a dynamic shared object (DSO) for PHP that will add LDAP
support.

%description ldap -l pl.UTF-8
Moduł PHP dodający obsługę LDAP.

%description ldap -l pt_BR.UTF-8
Um módulo para aplicações PHP que usam LDAP.

%package mbstring
Summary:	mbstring extension module for PHP
Summary(pl.UTF-8):	Moduł mbstring dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mbstring.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(mbstring)
Obsoletes:	php-mbstring < 4:5.3.28-7

%description mbstring
This is a dynamic shared object (DSO) for PHP that will add multibyte
string support.

%description mbstring -l pl.UTF-8
Moduł PHP dodający obsługę ciągów znaków wielobajtowych.

%package mcrypt
Summary:	mcrypt extension module for PHP
Summary(pl.UTF-8):	Moduł mcrypt dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mcrypt.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(mcrypt)
Obsoletes:	php-mcrypt < 4:5.3.28-7

%description mcrypt
This is a dynamic shared object (DSO) for PHP that will add mcrypt
support.

%description mcrypt -l pl.UTF-8
Moduł PHP dodający możliwość szyfrowania poprzez bibliotekę mcrypt.

%package mssql
Summary:	MS SQL extension module for PHP
Summary(pl.UTF-8):	Moduł MS SQL dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mssql.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(mssql)
Obsoletes:	php-mssql < 4:5.3.28-7

%description mssql
This is a dynamic shared object (DSO) for PHP that will add MS SQL
databases support through FreeTDS library.

%description mssql -l pl.UTF-8
Moduł PHP dodający obsługę baz danych MS SQL poprzez bibliotekę
FreeTDS.

%package mysql
Summary:	MySQL database module for PHP
Summary(pl.UTF-8):	Moduł bazy danych MySQL dla PHP
Summary(pt_BR.UTF-8):	Um módulo para aplicações PHP que usam bancos de dados MySQL
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mysql.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%{?with_mysqlnd:Requires:	%{name}-mysqlnd = %{epoch}:%{version}-%{release}}
Provides:	php(mysql)
Obsoletes:	php-mysql < 4:5.3.28-7

%description mysql
This is a dynamic shared object (DSO) for PHP that will add MySQL
database support.

%description mysql -l pl.UTF-8
Moduł PHP umożliwiający dostęp do bazy danych MySQL.

%description mysql -l pt_BR.UTF-8
Um módulo para aplicações PHP que usam bancos de dados MySQL.

%package mysqli
Summary:	MySQLi module for PHP
Summary(pl.UTF-8):	Moduł MySQLi dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mysqli.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%{?with_mysqlnd:Requires:	%{name}-mysqlnd = %{epoch}:%{version}-%{release}}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Provides:	php(mysqli)
Obsoletes:	php-mysqli < 4:5.3.28-7

%description mysqli
This is a dynamic shared object (DSO) for PHP that will add MySQLi
(Improved MySQL) support. The difference between it and mysql module
is that it provides access to functionality of MySQL 4.1 and above.

%description mysqli -l pl.UTF-8
Moduł PHP umożliwiający udoskonalony dostęp do bazy danych MySQL.
Różnicą między nim a modułem mysql jest dostęp do funkcjonalności
MySQL w wersji 4.1 i nowszych.

%package mysqlnd
Summary:	MySQL Native Client Driver for PHP
Summary(pl.UTF-8):	Sterownik natywnego klienta MySQL dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.mysqlnd.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(mysqlnd)
Obsoletes:	php-mysqlnd < 4:5.3.28-7

%description mysqlnd
MySQL Native Driver is a replacement for the MySQL Client Library
(libmysql).

Because MySQL Native Driver is written as a PHP extension, it is
tightly coupled to the workings of PHP. This leads to gains in
efficiency, especially when it comes to memory usage, as the driver
uses the PHP memory management system. It also supports the PHP memory
limit. Using MySQL Native Driver leads to comparable or better
performance than using MySQL Client Library, it always ensures the
most efficient use of memory. One example of the memory efficiency is
the fact that when using the MySQL Client Library, each row is stored
in memory twice, whereas with the MySQL Native Driver each row is only
stored once in memory.

%description mysqlnd -l pl.UTF-8
MySQL Native Driver (natywny sterownik MySQL) to zamiennik biblioteki
klienckiej MySQL (libmysql).

Ponieważ sterownik natywny jest napisany jako rozszerzenie PHP, jest
ściśle powiązany z pracą PHP. Daje to większą wydajność, zwłaszcza
jeśli chodzi o wykorzystanie pamięci, jako że sterownik wykorzystuje
system zarządzania pamięcią PHP; obsługuje także ograniczenie pamięci
z PHP. Niniejszy sterownik ma wydajność porównywalną lub lepszą niż
biblioteka kliencka MySQL, a pamięć zawsze wykorzystuje efektywniej.
Przykładem tego może być fakt, że w przypadku biblioteki klienckiej
każdy wiersz jest przechowywany w pamięci dwukrotnie, natomiast przy
tym sterowniku - tylko raz.

%package oci8
Summary:	Oracle 8+ database module for PHP
Summary(pl.UTF-8):	Moduł bazy danych Oracle 8+ dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.oci8.php
%{?requires_php_extension}
Provides:	php(oci8)
Obsoletes:	php-oci8 < 4:5.3.28-7

%description oci8
This is a dynamic shared object (DSO) for PHP that will add Oracle 7,
8, 9 and 10 database support through Oracle8 Call-Interface (OCI8).

%description oci8 -l pl.UTF-8
Moduł PHP umożliwiający dostęp do bazy danych Oracle 7, 8, 9 i 10
poprzez interfejs Oracle8 Call-Interface (OCI8).

%package odbc
Summary:	ODBC extension module for PHP
Summary(pl.UTF-8):	Moduł ODBC dla PHP
Summary(pt_BR.UTF-8):	Um módulo para aplicações PHP que usam bases de dados ODBC
Group:		Libraries
URL:		http://www.php.net/manual/en/book.uodbc.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	unixODBC >= 2.1.1-3
Provides:	php(odbc)
Obsoletes:	php-odbc < 4:5.3.28-7

%description odbc
This is a dynamic shared object (DSO) for PHP that will add ODBC
support.

%description odbc -l pl.UTF-8
Moduł PHP ze wsparciem dla ODBC.

%description odbc -l pt_BR.UTF-8
Um módulo para aplicações PHP que usam ODBC.

%package opcache
Summary:	Zend Optimizer+ - PHP code optimizer
Summary(pl.UTF-8):	Zend Optimizer+ - optymalizator kodu PHP
Group:		Libraries
URL:		https://wiki.php.net/rfc/optimizerplus
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(opcache) = %{opcachever}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching
and optimization. It improves PHP performance by storing precompiled
script bytecode in the shared memory. This eliminates the stages of
reading code from the disk and compiling it on future access. In
addition, it applies a few bytecode optimization patterns that make
code execution faster.

%description opcache -l pl.UTF-8
Zend OPcache zapewnia szybsze wykonywanie kodu PHP dzięki buforowaniu
i optymalizacji na poziomie opcode'ów. Poprawia wydajność PHP
przechowując prekompilowany bajtkod skryptu w pamięci współdzielonej.
Eliminuje etapy odczytu kodu z dysku i kompilacji przy późniejszym
dostępie. Ponadto wykonuje kilka wzorców optymalizacji bajtkodu,
czyniąc wykonywanie kodu szybszym.

%package openssl
Summary:	OpenSSL extension module for PHP
Summary(pl.UTF-8):	Moduł OpenSSL dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.openssl.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(openssl)
Obsoletes:	php-openssl < 4:5.3.28-7

%description openssl
This is a dynamic shared object (DSO) for PHP that will add OpenSSL
support.

%description openssl -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z biblioteki OpenSSL.

%package pcntl
Summary:	Process Control extension module for PHP
Summary(pl.UTF-8):	Moduł Process Control dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.pcntl.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(pcntl)
Obsoletes:	php-pcntl < 4:5.3.28-7

%description pcntl
This is a dynamic shared object (DSO) for PHP that will add process
spawning and control support. It supports functions like fork(),
waitpid(), signal() etc.

%description pcntl -l pl.UTF-8
Moduł PHP umożliwiający tworzenie nowych procesów i kontrolę nad nimi.
Obsługuje funkcje takie jak fork(), waitpid(), signal() i podobne.

%package pcre
Summary:	PCRE extension module for PHP
Summary(pl.UTF-8):	Moduł PCRE dla PHP
Group:		Libraries
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(pcre)
Obsoletes:	php-pcre < 4:5.3.28-7

%description pcre
This is a dynamic shared object (DSO) for PHP that will add Perl
Compatible Regular Expression support.

%description pcre -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z perlowych wyrażeń regularnych
(Perl Compatible Regular Expressions)

%package pdo
Summary:	PHP Data Objects (PDO)
Summary(pl.UTF-8):	Obsługa PHP Data Objects (PDO)
Group:		Libraries
URL:		http://www.php.net/manual/en/book.pdo.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Provides:	%{name}(PDO_API) = %{php_pdo_api_version}
Provides:	php(pdo)
Obsoletes:	php-pdo < 4:5.3.28-7
Obsoletes:	php-pecl-PDO

%description pdo
This is a dynamic shared object (DSO) for PHP that will add PDO
support.

%description pdo -l pl.UTF-8
Moduł PHP dodający obsługę PDO (PHP Data Objects).

%package pdo-dblib
Summary:	PHP Data Objects (PDO) FreeTDS support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą FreeTDS
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-dblib.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(dblib)
Obsoletes:	php-pdo-dblib < 4:5.3.28-7

%description pdo-dblib
This is a dynamic shared object (DSO) for PHP that will add PDO
FreeTDS support.

%description pdo-dblib -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych FreeTDS za pośrednictwem
interfejsu PDO.

%package pdo-firebird
Summary:	PHP Data Objects (PDO) Firebird support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą Firebirda
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-firebird.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(pdo-firebird)
Obsoletes:	php-pdo-firebird < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_FIREBIRD

%description pdo-firebird
This is a dynamic shared object (DSO) for PHP that will add PDO
Firebird support.

%description pdo-firebird -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych Firebird za pośrednictwem
interfejsu PDO.

%package pdo-mysql
Summary:	PHP Data Objects (PDO) MySQL support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą MySQL-a
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-mysql.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%{?with_mysqlnd:Requires:	%{name}-mysqlnd = %{epoch}:%{version}-%{release}}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(pdo-mysql)
Obsoletes:	php-pdo-mysql < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_MYSQL

%description pdo-mysql
This is a dynamic shared object (DSO) for PHP that will add PDO MySQL
support.

%description pdo-mysql -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych MySQL za pośrednictwem
interfejsu PDO.

%package pdo-oci
Summary:	PHP Data Objects (PDO) Oracle support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą Oracle'a
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-oci.php
%{?requires_php_extension}
%{?requires_php_pdo_module}
Provides:	php(pdo-oci)
Obsoletes:	php-pdo-oci < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_OCI

%description pdo-oci
This is a dynamic shared object (DSO) for PHP that will add PDO Oracle
support.

%description pdo-oci -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych Oracle za pośrednictwem
interfejsu PDO.

%package pdo-odbc
Summary:	PHP Data Objects (PDO) ODBC support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą ODBC
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-odbc.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(pdo-odbc)
Obsoletes:	php-pdo-odbc < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_ODBC

%description pdo-odbc
This is a dynamic shared object (DSO) for PHP that will add PDO ODBC
support.

%description pdo-odbc -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych ODBC za pośrednictwem
interfejsu PDO.

%package pdo-pgsql
Summary:	PHP Data Objects (PDO) PostgreSQL support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą PostgreSQL-a
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-pgsql.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(pdo-pgsql)
Provides:	php-pecl-PDO_PGSQL
Obsoletes:	php-pdo-pgsql < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_PGSQL < 4:5.2.1-2

%description pdo-pgsql
This is a dynamic shared object (DSO) for PHP that will add PDO
PostgreSQL support.

%description pdo-pgsql -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych PostgreSQL za pośrednictwem
interfejsu PDO.

%package pdo-sqlite
Summary:	PHP Data Objects (PDO) SQLite support
Summary(pl.UTF-8):	Moduł PHP Data Objects (PDO) z obsługą SQLite
Group:		Libraries
URL:		http://www.php.net/manual/en/ref.pdo-sqlite.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pdo = %{epoch}:%{version}-%{release}
Provides:	php(pdo-sqlite)
Obsoletes:	php-pdo-sqlite < 4:5.3.28-7
Obsoletes:	php-pecl-PDO_SQLITE

%description pdo-sqlite
This is a dynamic shared object (DSO) for PHP that will add PDO SQLite
support.

%description pdo-sqlite -l pl.UTF-8
Moduł dla PHP dodający obsługę baz danych SQLite za pośrednictwem
interfejsu PDO.

%package pgsql
Summary:	PostgreSQL database module for PHP
Summary(pl.UTF-8):	Moduł bazy danych PostgreSQL dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.pgsql.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(pgsql)
Obsoletes:	php-pgsql < 4:5.3.28-7

%description pgsql
This is a dynamic shared object (DSO) for PHP that will add PostgreSQL
database support.

%description pgsql -l pl.UTF-8
Moduł PHP umożliwiający dostęp do bazy danych PostgreSQL.

%description pgsql -l pt_BR.UTF-8
Um módulo para aplicações PHP que usam bancos de dados postgresql.

%package phar
Summary:	phar database module for PHP
Summary(pl.UTF-8):	Moduł phar dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.phar.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Suggests:	%{name}-cli
# zlib is required by phar program, but as phar cli is optional should the dep be too
Suggests:	%{name}-zlib
Provides:	php(phar) = %{pharver}
Obsoletes:	php-pecl-phar < %{pharver}
Obsoletes:	php-phar < 4:5.3.28-7
Conflicts:	php-ioncube < 4.0.9

%description phar
This is a dynamic shared object (DSO) for PHP that will add phar
archive a support.

%description phar -l pl.UTF-8
Moduł PHP umożliwiający dostęp do achiwów .phar.

%package posix
Summary:	POSIX extension module for PHP
Summary(pl.UTF-8):	Moduł POSIX dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.posix.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(posix)
Obsoletes:	php-posix < 4:5.3.28-7

%description posix
This is a dynamic shared object (DSO) for PHP that will add POSIX
functions support to PHP.

%description posix -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z funkcji POSIX.

%package pspell
Summary:	pspell extension module for PHP
Summary(pl.UTF-8):	Moduł pspell dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.pspell.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(pspell)
Obsoletes:	php-pspell < 4:5.3.28-7

%description pspell
This is a dynamic shared object (DSO) for PHP that will add pspell
support to PHP. It allows to check the spelling of a word and offer
suggestions.

%description pspell -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z pspella. Pozwala on na
sprawdzanie pisowni słowa i sugerowanie poprawek.

%package readline
Summary:	readline extension module for PHP
Summary(pl.UTF-8):	Moduł readline dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.readline.php
Requires:	%{name}-cli = %{epoch}:%{version}-%{release}
Provides:	php(readline)
Obsoletes:	php-readline < 4:5.3.28-7

%description readline
This PHP module adds support for readline functions (only for cli and
cgi SAPIs).

%description readline -l pl.UTF-8
Moduł PHP dodający obsługę funkcji readline (tylko do SAPI cli i cgi).

%package recode
Summary:	recode extension module for PHP
Summary(pl.UTF-8):	Moduł recode dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.recode.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	recode >= 3.5d-3
Provides:	php(recode)
Obsoletes:	php-recode < 4:5.3.28-7

%description recode
This is a dynamic shared object (DSO) for PHP that will add recode
support.

%description recode -l pl.UTF-8
Moduł PHP dodający możliwość konwersji kodowania plików (poprzez
bibliotekę recode).

%package session
Summary:	session extension module for PHP
Summary(pl.UTF-8):	Moduł session dla PHP
Group:		Libraries
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Suggests:	%{name}-hash = %{epoch}:%{version}-%{release}
Suggests:	tmpwatch
Provides:	php(session)
Obsoletes:	php-session < 4:5.3.28-7

%description session
This is a dynamic shared object (DSO) for PHP that will add session
support.

%description session -l pl.UTF-8
Moduł PHP dodający obsługę sesji.

%package shmop
Summary:	Shared Memory Operations extension module for PHP
Summary(pl.UTF-8):	Moduł shmop dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.shmop.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(shmop)
Obsoletes:	php-shmop < 4:5.3.28-7

%description shmop
This is a dynamic shared object (DSO) for PHP that will add Shared
Memory Operations support.

%description shmop -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z pamięci dzielonej.

%package simplexml
Summary:	Simple XML extension module for PHP
Summary(pl.UTF-8):	Moduł prostego rozszerzenia XML dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.simplexml.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Provides:	php(simplexml)
Obsoletes:	php-simplexml < 4:5.3.28-7

%description simplexml
This is a dynamic shared object (DSO) for PHP that will add Simple XML
support.

%description simplexml -l pl.UTF-8
Moduł PHP dodający obsługę prostego XML-a.

%package snmp
Summary:	SNMP extension module for PHP
Summary(pl.UTF-8):	Moduł SNMP dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.snmp.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-sockets = %{epoch}:%{version}-%{release}
Requires:	%{name}-spl = %{epoch}:%{version}-%{release}
Provides:	php(snmp)
Obsoletes:	php-snmp < 4:5.3.28-7

%description snmp
This is a dynamic shared object (DSO) for PHP that will add SNMP
support.

%description snmp -l pl.UTF-8
Moduł PHP dodający obsługę SNMP.

%package soap
Summary:	soap extension module for PHP
Summary(pl.UTF-8):	Moduł soap dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.soap.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(soap)
Obsoletes:	php-soap < 4:5.3.28-7

%description soap
This is a dynamic shared object (DSO) for PHP that will add SOAP/WSDL
support.

%description soap -l pl.UTF-8
Moduł PHP dodający obsługę SOAP/WSDL.

%package sockets
Summary:	sockets extension module for PHP
Summary(pl.UTF-8):	Moduł socket dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.sockets.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sockets)
Obsoletes:	php-sockets < 4:5.3.28-7

%description sockets
This is a dynamic shared object (DSO) for PHP that will add sockets
support.

%description sockets -l pl.UTF-8
Moduł PHP dodający obsługę gniazdek.

%package spl
Summary:	Standard PHP Library module for PHP
Summary(pl.UTF-8):	Moduł biblioteki standardowej (Standard PHP Library) dla PHP
Group:		Libraries
URL:		http://php.net/manual/en/book.spl.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-pcre = %{epoch}:%{version}-%{release}
Requires:	%{name}-simplexml = %{epoch}:%{version}-%{release}
Provides:	php(spl)
Obsoletes:	php-spl < 4:5.3.28-7

%description spl
This is a dynamic shared object (DSO) for PHP that will add Standard
PHP Library support.

%description spl -l pl.UTF-8
Moduł PHP z biblioteką standardową PHP (SPL - Standard PHP Library).

%package sqlite3
Summary:	SQLite3 extension module for PHP
Summary(pl.UTF-8):	Moduł SQLite3 dla PHP
Group:		Libraries
URL:		http://php.net/manual/en/book.sqlite3.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sqlite3) = %{sqlite3ver}
Obsoletes:	php-sqlite3 < 4:5.3.28-7

%description sqlite3
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is the server. The SQLite library reads and writes
directly to and from the database files on disk.

%description sqlite3 -l pl.UTF-8
SQLite jest napisaną w C biblioteką implementującą osadzalny silnik
bazodanowy SQL. Program linkujący się z biblioteką SQLite może mieć
dostęp do bazy SQL bez potrzeby uruchamiania dodatkowego procesu
RDBMS.

SQLite to nie klient baz danych - biblioteka nie łączy się z serwerami
baz danych. SQLite sam jest serwerem. Biblioteka SQLite czyta i
zapisuje dane bezpośrednio z/do plików baz danych znajdujących się na
dysku.

%package sybase-ct
Summary:	Sybase-CT extension module for PHP
Summary(pl.UTF-8):	Moduł Sybase-CT dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.sybase.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sybase-ct)
Obsoletes:	php-sybase
Obsoletes:	php-sybase-ct < 4:5.3.28-7

%description sybase-ct
This is a dynamic shared object (DSO) for PHP that will add Sybase and
MS SQL databases support through CT-lib.

%description sybase-ct -l pl.UTF-8
Moduł PHP dodający obsługę baz danych Sybase oraz MS SQL poprzez
CT-lib.

%package sysvmsg
Summary:	SysV msg extension module for PHP
Summary(pl.UTF-8):	Moduł SysV msg dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.sem.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sysvmsg)
Obsoletes:	php-sysvmsg < 4:5.3.28-7

%description sysvmsg
This is a dynamic shared object (DSO) for PHP that will add SysV
message queues support.

%description sysvmsg -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z kolejek komunikatów SysV.

%package sysvsem
Summary:	SysV sem extension module for PHP
Summary(pl.UTF-8):	Moduł SysV sem dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.sem.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sysvsem)
Obsoletes:	php-sysvsem < 4:5.3.28-7

%description sysvsem
This is a dynamic shared object (DSO) for PHP that will add SysV
semaphores support.

%description sysvsem -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z semaforów SysV.

%package sysvshm
Summary:	SysV shm extension module for PHP
Summary(pl.UTF-8):	Moduł SysV shm dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.shmop.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(sysvshm)
Obsoletes:	php-sysvshm < 4:5.3.28-7

%description sysvshm
This is a dynamic shared object (DSO) for PHP that will add SysV
Shared Memory support.

%description sysvshm -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z pamięci dzielonej SysV.

%package tests
Summary:	Contains unit test files for PHP and extensions
Summary(pl.UTF-8):	Zawiera pliki testów jednostkowych dla PHP i rozszerzeń
Group:		Libraries
URL:		http://qa.php.net/
Requires:	%{name}-cli

%description tests
This package contains unit tests for PHP and its extensions.

%description tests -l pl.UTF-8
Ten pakiet zawiera pliki testów jednostkowych dla PHP i rozszerzeń.

%package tidy
Summary:	Tidy extension module for PHP
Summary(pl.UTF-8):	Moduł Tidy dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.tidy.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	tidy
Provides:	php(tidy)
Obsoletes:	php-tidy < 4:5.3.28-7

%description tidy
This is a dynamic shared object (DSO) for PHP that will add Tidy
support.

%description tidy -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z tidy.

%package tokenizer
Summary:	tokenizer extension module for PHP
Summary(pl.UTF-8):	Moduł rozszerzenia tokenizer dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.tokenizer.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(tokenizer)
Obsoletes:	php-tokenizer < 4:5.3.28-7

%description tokenizer
This is a dynamic shared object (DSO) for PHP that will add tokenizer
support.

%description tokenizer -l pl.UTF-8
Moduł PHP dodający obsługę tokenizera do PHP.

%package wddx
Summary:	wddx extension module for PHP
Summary(pl.UTF-8):	Moduł wddx dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.wddx.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
# - wddx doesn't require session as it's disabled at compile time:
#   if HAVE_PHP_SESSION && !defined(COMPILE_DL_SESSION)
#   see also php.spec#rev1.120.2.22
#Requires:	%{name}-session = %{epoch}:%{version}-%{release}
Requires:	%{name}-xml = %{epoch}:%{version}-%{release}
Provides:	php(wddx)
Obsoletes:	php-wddx < 4:5.3.28-7

%description wddx
This is a dynamic shared object (DSO) for PHP that will add wddx
support.

%description wddx -l pl.UTF-8
Moduł PHP umożliwiający korzystanie z wddx.

%package xml
Summary:	XML extension module for PHP
Summary(pl.UTF-8):	Moduł XML dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.xml.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(xml)
Obsoletes:	php-xml < 4:5.3.28-7

%description xml
This is a dynamic shared object (DSO) for PHP that will add XML
support. This extension lets you create XML parsers and then define
handlers for different XML events.

%description xml -l pl.UTF-8
Moduł PHP umożliwiający parsowanie plików XML i obsługę zdarzeń
związanych z tymi plikami. Pozwala on tworzyć analizatory XML-a i
następnie definiować procedury obsługi dla różnych zdarzeń XML.

%package xmlreader
Summary:	XML Reader extension module for PHP
Summary(pl.UTF-8):	Moduł XML Reader dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.xmlreader.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-dom = %{epoch}:%{version}-%{release}
Provides:	php(xmlreader)
Obsoletes:	php-xmlreader < 4:5.3.28-7

%description xmlreader
This is a dynamic shared object (DSO) for PHP that will add XML Reader
support. The XMLReader extension is an XML Pull parser. The reader
acts as a cursor going forward on the document stream and stopping at
each node on the way.

%description xmlreader -l pl.UTF-8
Moduł PHP umożliwiający analizę plików XML w trybie Pull. Czytnik
działa jako kursor przechodzący przez strumień dokumentu i
zatrzymujący się na każdym węźle po drodze.

%package xmlrpc
Summary:	xmlrpc extension module for PHP
Summary(pl.UTF-8):	Moduł xmlrpc dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.xmlrpc.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-xml = %{epoch}:%{version}-%{release}
Provides:	php(xmlrpc)
Obsoletes:	php-xmlrpc < 4:5.3.28-7

%description xmlrpc
This is a dynamic shared object (DSO) for PHP that will add XMLRPC
support.

%description xmlrpc -l pl.UTF-8
Moduł PHP dodający obsługę XMLRPC.

%package xmlwriter
Summary:	Fast, non-cached, forward-only means to write XML data
Summary(pl.UTF-8):	Szybka, nie cachowana metoda zapisu danych w formacie XML
Group:		Libraries
URL:		http://www.php.net/manual/en/book.xmlwriter.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(xmlwriter)
Obsoletes:	php-pecl-xmlwriter
Obsoletes:	php-xmlwriter < 4:5.3.28-7

%description xmlwriter
This extension wraps the libxml xmlWriter API. Represents a writer
that provides a non-cached, forward-only means of generating streams
or files containing XML data.

%description xmlwriter -l pl.UTF-8
To rozszerzenie obudowuje API xmlWriter z libxml. Reprezentuje obsługę
zapisu dostarczającą nie cachowanych metod generowania strumieni lub
plików zawierających dane XML.

%package xsl
Summary:	xsl extension module for PHP
Summary(pl.UTF-8):	Moduł xsl dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.xsl.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-dom = %{epoch}:%{version}-%{release}
Requires:	libxslt >= 1.0.18
Provides:	php(xsl)
Obsoletes:	php-xsl < 4:5.3.28-7
# actually not true, functionality is similar, but API differs
Obsoletes:	php-xslt <= 3:4.3.8-1

%description xsl
This is a dynamic shared object (DSO) for PHP that will add new XSL
support (using libxslt).

%description xsl -l pl.UTF-8
Moduł PHP dodający nową obsługę XSLT (przy użyciu libxslt).

%package zip
Summary:	Zip management extension
Summary(pl.UTF-8):	Zarządzanie archiwami zip
Group:		Libraries
URL:		http://www.php.net/manual/en/book.zip.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%{?with_system_libzip:Requires:	libzip >= 0.10.1-2}
Provides:	php(zip) = %{zipver}
Obsoletes:	php-pecl-zip < %{zipver}
Obsoletes:	php-zip < 4:5.3.28-7

%description zip
Zip is an extension to create, modify and read zip files.

%description zip -l pl.UTF-8
Zip jest rozszerzeniem umożliwiającym tworzenie, modyfikację oraz
odczyt archiwów zip.

%package zlib
Summary:	Zlib extension module for PHP
Summary(pl.UTF-8):	Moduł zlib dla PHP
Group:		Libraries
URL:		http://www.php.net/manual/en/book.zlib.php
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php(zlib)
Obsoletes:	php-zlib < 4:5.3.28-7

%description zlib
This is a dynamic shared object (DSO) for PHP that will add zlib
compression support to PHP.

%description zlib -l pl.UTF-8
Moduł PHP umożliwiający używanie kompresji zlib.

%prep
%setup -q -n %{orgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

cp -p php.ini-production php.ini
%patch10 -p1
%if %{with type_hints}
%patch12 -p0
%endif
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch29 -p1
%patch31 -p1
%if "%{pld_release}" != "ac"
%patch34 -p1
%endif
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%if %{with fpm}
%patch41 -p1
%patch42 -p1
%endif
%patch43 -p1
%patch44 -p1
#%patch45 -p1 # imap annotations. fixme
#%patch46 -p1 # imap myrights. fixme
%if %{with suhosin}
%patch47 -p1
%endif
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%undos ext/spl/tests/SplFileInfo_getInode_basic.phpt
%patch55 -p1
%patch59 -p1
%patch60 -p1
%patch62 -p1
%patch63 -p1
%{?with_system_libzip:%patch65 -p1}
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1

sed -i -e '/PHP_ADD_LIBRARY_WITH_PATH/s#xmlrpc,#xmlrpc-epi,#' ext/xmlrpc/config.m4

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# conflict seems to be resolved by recode patches
%{__rm} ext/recode/config9.m4

# remove all bundled libraries not to link with them accidentally
%{__rm} -r ext/sqlite3/libsqlite
#%{__rm} -r ext/bcmath/libbcmath
#%{__rm} -r ext/date/lib
#%{__rm} -r ext/fileinfo/libmagic
#%{__rm} -r ext/dba/libcdb
#%{__rm} -r ext/dba/libflatfile
#%{__rm} -r ext/dba/libinifile
#%{__rm} -r ext/gd/libgd
#%{__rm} -r ext/mbstring/libmbfl
#%{__rm} -r ext/mbstring/oniguruma
%{__rm} -r ext/pcre/pcrelib
#%{__rm} -r ext/soap/interop
%{__rm} -r ext/xmlrpc/libxmlrpc
#%{__rm} -r ext/zip/lib
%{__rm} ext/date/lib/timezonedb.h

cp -pf Zend/LICENSE{,.Zend}
install -p %{SOURCE13} dep-tests.sh

# breaks build
sed -i -e 's#-fvisibility=hidden##g' configure*

# disable broken tests
# says just "Terminated" twice and fails
mv sapi/cli/tests/022.phpt{,.broken}

# really dumb test, executable binary name is .libs/ something when building
# https://bugs.php.net/bug.php?id=54514
mv tests/basic/bug54514.phpt{,.disable}

# breaks whole testsuite unexpectedly:
# Fatal error: Call to undefined function gzencode() in run-tests.php on line 1714
# probably broken as zlib is built as shared
mv ext/soap/tests/server019.phpt{,disable}
# Fatal error: Call to undefined function gzcompress() in run-tests.php on line 1728
mv ext/soap/tests/server020.phpt{,disable}

# runs out of memory and kills carme vserver
# PASS Bug #39438 (Fatal error: Out of memory) [Zend/tests/bug39438.phpt]
mv Zend/tests/bug39438.phpt{,.disable}

# php-5.3.3/ext/standard/tests/file/statpage.phpt
%{__rm} ext/standard/tests/file/statpage.phpt

# idiotic test, it will fail if somebody else makes space on disk or if disk
# space is not yet allocated (xfs). report upstream to advice bogus test is
# probably pointless.
%{__rm} ext/standard/tests/file/disk_free_space_basic.phpt

%ifarch %{x8664}
# all pdo_sqlite, sqlite3 tests die with Aborted on carme
%{__rm} -r ext/pdo_sqlite/tests
%{__rm} -r ext/sqlite3/tests
%endif

# skip XFAILs
# no point testing stuff that is knowingly broken
find -name '*.phpt' | xargs grep XFAIL -l | xargs rm -v

env \
%ifarch %{ix86}
ix86= x8664=:
%endif
%ifarch %{x8664}
ix86=: x8664= \
%endif
%ifarch x32
ix86=: x8664=: \
%endif
	sh -xe %{_sourcedir}/skip-tests.sh

%build
API=$(awk '/#define PHP_API_VERSION/{print $3}' main/php.h)
if [ $API != %{php_api_version} ]; then
	echo "Set %%define php_api_version to $API and re-run."
	exit 1
fi

API=$(awk '/#define ZEND_MODULE_API_NO/{print $3}' Zend/zend_modules.h)
if [ $API != %{zend_module_api} ]; then
	echo "Set %%define zend_module_api to $API and re-run."
	exit 1
fi

API=$(awk '/#define ZEND_EXTENSION_API_NO/{print $3}' Zend/zend_extensions.h)
if [ $API != %{zend_extension_api} ]; then
	echo "Set %%define zend_extension_api to $API and re-run."
	exit 1
fi

API=$(awk '/#define PDO_DRIVER_API/{print $3}' ext/pdo/php_pdo_driver.h)
if [ $API != %{php_pdo_api_version} ]; then
	echo "Set %%define php_pdo_api_version to $API and re-run."
	exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
	: Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
	: Update the fileinfover macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
	: Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
	: Update the pharver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_SQLITE3_VERSION/{s/.* "//;s/".*$//;p}' ext/sqlite3/php_sqlite3.h)
if test "$ver" != "%{sqlite3ver}"; then
	: Error: Upstream Sqlite3 version is now ${ver}, expecting %{sqlite3ver}.
	: Update the sqlite3ver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
	: Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
	: Update the zipver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
	: Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
	: Update the jsonver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION /{s/.* "//;s/".*$//;p}' ext/opcache/ZendAccelerator.h)
if test "$ver" != "%{opcachever}"; then
	: Error: Upstream Zend Opcache version is now ${ver}, expecting %{opcachever}.
	: Update the opcachever macro and rebuild.
	exit 1
fi
ver=$(sed -rne 's,.*<version>(.+)</version>,\1,p' ext/bz2/package.xml)
if test "$ver" != "%{bz2ver}"; then
	: Error: Upstream BZIP2 version is now ${ver}, expecting %{bz2ver}.
	: Update the bz2ver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_ENCHANT_VERSION /{s/.* "//;s/".*$//;p}' ext/enchant/php_enchant.h)
if test "$ver" != "%{enchantver}"; then
	: Error: Upstream Enchant version is now ${ver}, expecting %{enchantver}.
	: Update the enchantver macro and rebuild.
	exit 1
fi
ver=$(awk '/#define PHP_HASH_EXTVER/ {print $3}' ext/hash/php_hash.h | xargs)
if test "$ver" != "%{hashver}"; then
	: Error: Upstream HASH version is now ${ver}, expecting %{hashver}.
	: Update the hashver macro and rebuild.
	exit 1
fi
ver=$(sed -n '/#define PHP_INTL_VERSION /{s/.* "//;s/".*$//;p}' ext/intl/php_intl.h)
if test "$ver" != "%{intlver}"; then
	: Error: Upstream Intl version is now ${ver}, expecting %{intlver}.
	: Update the intlver macro and rebuild.
	exit 1
fi

export EXTENSION_DIR="%{php_extensiondir}"
# configure once (for faster debugging purposes)
if [ ! -f _built-conf ]; then
	# now remove Makefile copies
	rm -f Makefile.{cgi-fcgi,fpm,cli,apxs1,apxs2,litespeed}
	%{__libtoolize}
	%{__aclocal}
	cp -f /usr/share/automake/config.* .
	./buildconf --force
	touch _built-conf
fi
export PROG_SENDMAIL="/usr/lib/sendmail"
export CPPFLAGS="-DDEBUG_FASTCGI -DHAVE_STRNDUP %{rpmcppflags} \
	-I%{_includedir}/xmlrpc-epi"

sapis="
cli
%if %{with cgi}
cgi-fcgi
%endif
%if %{with litespeed}
litespeed
%endif
%if %{with fpm}
fpm
%endif
%if %{with embed}
embed
%endif
%if %{with apache1}
apxs1
%endif
%if %{with apache2}
apxs2
%endif
"
for sapi in $sapis; do
	: SAPI $sapi
	# skip if already configured (for faster debugging purposes)
	[ -f Makefile.$sapi ] && continue

	sapi_args=''
	case $sapi in
	cgi-fcgi)
		sapi_args='--disable-cli'
	;;
	cli)
		sapi_args='--disable-cgi %{?with_gcov:--enable-gcov}'
	;;
	fpm)
		sapi_args='--disable-cli --disable-cgi --enable-fpm'
		;;
	embed)
		sapi_args='--disable-cli --disable-cgi --enable-embed'
		;;
	apxs1)
		ver=$(rpm -q --qf '%{V}' apache1-devel)
		sapi_args="--disable-cli --disable-cgi --with-apxs=%{apxs1} --with-apache-version=$ver"
	;;
	apxs2)
		ver=$(rpm -q --qf '%{V}' apache-devel)
		sapi_args="--disable-cli --disable-cgi --with-apxs2=%{apxs2} --with-apache-version=$ver"
	;;
	litespeed)
		sapi_args='--disable-cli --disable-cgi --with-litespeed '
	;;
	esac

	%configure \
	$sapi_args \
%if "%{!?configure_cache:0}%{?configure_cache}" == "0"
	--cache-file=config.cache \
%endif
	--with-libdir=%{_lib} \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/conf.d \
	--with-system-tzdata \
	--%{!?debug:dis}%{?debug:en}able-debug \
	%{?with_zts:--enable-maintainer-zts} \
	--enable-inline-optimization \
	--enable-bcmath=shared \
	--enable-calendar=shared \
	--enable-ctype=shared \
	--enable-dba=shared \
	--enable-dom=shared \
	--enable-exif=shared \
	--enable-fileinfo=shared \
	--enable-ftp=shared \
	--enable-gd-native-ttf \
	%{?with_intl:--enable-intl=shared} \
	--enable-libxml \
	--enable-mbstring=shared,all \
	--enable-mbregex \
	--enable-pcntl=shared \
	--enable-pdo=shared \
	--enable-json=shared \
	--enable-hash=shared \
	--enable-xmlwriter=shared \
%if %{with fpm}
	--with-fpm-user=http \
	--with-fpm-group=http \
%endif
%if %{with mssql} || %{with sybase_ct}
	--with-pdo-dblib=shared \
%endif
%if %{with interbase} && %{without interbase_inst}
	--with-pdo-firebird=shared,/usr \
%endif
	%{?with_mhash:--with-mhash=yes} \
	--with-mysql-sock=/var/lib/mysql/mysql.sock \
	--with-pdo-mysql=shared,%{!?with_mysqlnd:/usr}%{?with_mysqlnd:mysqlnd} \
	%{?with_oci:--with-pdo-oci=shared%{?with_instantclient:,instantclient,%{_libdir}}} \
	%{?with_odbc:--with-pdo-odbc=shared,unixODBC,/usr} \
	%{?with_pgsql:--with-pdo-pgsql=shared} \
	%{?with_pdo_sqlite:--with-pdo-sqlite=shared,/usr} \
	%{?with_webp:--with-vpx-dir=/usr} \
	--without-libexpat-dir \
	--enable-posix=shared \
	--enable-shared \
	--enable-session=shared \
	--enable-shmop=shared \
	--enable-simplexml=shared \
	--enable-sysvmsg=shared \
	--enable-sysvsem=shared \
	--enable-sysvshm=shared \
	--enable-soap=shared \
	--enable-sockets=shared \
	--enable-tokenizer=shared \
	%{?with_wddx:--enable-wddx=shared} \
	--enable-xml=shared \
	--enable-xmlreader=shared \
	--with-bz2=shared \
	%{__with_without curl curl shared} \
	--with-db4 \
	--with-iconv=shared \
	%{?with_enchant:--with-enchant=shared,/usr} \
	--with-freetype-dir=shared \
	--with-gettext=shared \
	--with-gd=shared%{?with_system_gd:,/usr} \
	--with-gdbm \
	--with-gmp=shared \
	%{?with_imap:--with-imap=shared --with-imap-ssl} \
	%{?with_interbase:--with-interbase=shared%{!?with_interbase_inst:,/usr}} \
	--with-jpeg-dir=/usr \
	%{?with_ldap:--with-ldap=shared --with-ldap-sasl} \
	--with-mcrypt=shared \
	%{?with_mm:--with-mm} \
	%{?with_mssql:--with-mssql=shared} \
	%{?with_mysqlnd:--enable-mysqlnd=shared} \
	--with-mysql=shared,%{!?with_mysqlnd:/usr}%{?with_mysqlnd:mysqlnd} \
	%{?with_mysqli:--with-mysqli=shared,%{!?with_mysqlnd:/usr/bin/mysql_config}%{?with_mysqlnd:mysqlnd}} \
	%{?with_oci:--with-oci8=shared%{?with_instantclient:,instantclient,%{_libdir}}} \
	%{?with_opcache:--enable-opcache=shared} \
	%{?with_openssl:--with-openssl=shared} \
	%{?with_kerberos5:--with-kerberos} \
	--with-tcadb=/usr \
	%{__with_without pcre pcre-regex /usr} \
	%{__enable_disable filter filter shared} \
	--with-pear=%{php_pear_dir} \
	%{__with_without pgsql pgsql shared,/usr} \
	%{__enable_disable phar phar shared} \
	--with-png-dir=/usr \
	%{?with_pspell:--with-pspell=shared} \
	--with-readline=shared \
	%{?with_recode:--with-recode=shared} \
	--with-regex=system \
	%{?with_snmp:--with-snmp=shared} \
	%{?with_sybase_ct:--with-sybase-ct=shared,/usr} \
	%{!?with_pdo_sqlite:--without-pdo-sqlite} \
	%{__with_without sqlite3 sqlite3 shared,/usr} \
	--with-t1lib=shared \
	%{?with_tidy:--with-tidy=shared} \
	%{?with_odbc:--with-unixODBC=shared,/usr} \
	%{__with_without xmlrpc xmlrpc shared,/usr} \
	--with-xsl=shared \
	--with-zlib=shared \
	--with-zlib-dir=shared,/usr \
	%{?with_system_libzip:--with-libzip} \
	--enable-zip=shared,/usr \

	# save for debug
	cp -f Makefile Makefile.$sapi
	cp -f main/php_config.h php_config.h.$sapi
	cp -f config.log config.log.$sapi
done

# as we build each SAPI in own make, adjust php-config.in forehead
sapis=$(%{__sed} -rne 's/^PHP_INSTALLED_SAPIS = (.+)/\1/p' Makefile.* | tr ' ' '\n' | sort -u | xargs)
%{__sed} -i -e "s,@PHP_INSTALLED_SAPIS@,$sapis," scripts/php-config.in

# must make libphp_common first, so modules can link against it.
cp -af php_config.h.cli main/php_config.h
cp -af Makefile.cli Makefile
%{__make} libphp_common.la
%{__make} build-modules

%if %{with apache1}
%{__make} libtool-sapi LIBTOOL_SAPI=sapi/apache/libphp5.la -f Makefile.apxs1
%endif

%if %{with apache2}
%{__make} libtool-sapi LIBTOOL_SAPI=sapi/apache2handler/libphp5.la -f Makefile.apxs2
%endif

%if %{with litespeed}
%{__make} -f Makefile.litespeed litespeed
%endif

%if %{with embed}
%{__make} -f Makefile.embed libphp5.la
%endif

# CGI/FCGI
%if %{with cgi}
cp -pf php_config.h.cgi-fcgi main/php_config.h
%{__make} -f Makefile.cgi-fcgi
[ "$(echo '<?=php_sapi_name();' | ./sapi/cgi/php-cgi -qn)" = "cgi-fcgi" ]
%endif

# PHP FPM
%if %{with fpm}
cp -pf php_config.h.fpm main/php_config.h
%{__make} -f Makefile.fpm
[ $(./sapi/fpm/php-fpm -n -m | grep cgi-fcgi) = "cgi-fcgi" ]
%endif

# CLI
cp -pf php_config.h.cli main/php_config.h
%{__make} -f Makefile.cli
[ "$(echo '<?=php_sapi_name();' | ./sapi/cli/php -qn)" = "cli" ]

# check for stupid xml parse breakage where &lt; and &gt; just get lost in parse result
./sapi/cli/php -n -dextension_dir=modules -dextension=xml.so -r '$p = xml_parser_create(); xml_parse_into_struct($p, "<x>&lt;</x>", $vals, $index); exit((int )empty($vals[0]["value"]));'

# Generate stub .ini files for each extension
rm -rf conf.d
install -d conf.d
generate_inifiles() {
	for so in modules/*.so; do
		mod=$(basename $so .so)
		ext=extension
		# opcache.so is zend extension
		nm $so | grep -q zend_extension_entry && ext=zend_extension
		conf="$mod.ini"
		# xml needs to be loaded before wddx
		[ "$mod" = "wddx" ] && conf="xml_$mod.ini"
		# pre needs to be loaded before SPL
		[ "$mod" = "pcre" ] && conf="PCRE.ini"
		# spl needs to be loaded before mysqli
		[ "$mod" = "spl" ] && conf="SPL.ini"
		# session needs to be loaded before php-pecl-http, php-pecl-memcache, php-pecl-session_mysql
		[ "$mod" = "session" ] && conf="Session.ini"
		# mysqlnd needs to be loaded before mysql,mysqli,pdo_mysqli
		[ "$mod" = "mysqlnd" ] && conf="MySQLND.ini"
		echo "+ $conf"
		cat > conf.d/$conf <<-EOF
			; Enable $mod $ext module
			$ext=$mod.so
		EOF
	done
}
generate_inifiles

# Check that the module inner-dependencies are intact
PHP=./sapi/cli/php EXTENSION_DIR=modules CONFIG_DIR=conf.d ./dep-tests.sh > dep-tests.log
if grep -v OK dep-tests.log; then
	echo >&2 "The results above were not expected"
	exit 1
fi

%if %{with gcov}
# Use CLI SAPI
cp -pf php_config.h.cli main/php_config.h
cp -pf Makefile.cli Makefile
%{__make} lcov
# you really don't want to package result of gcov build
exit 1
%endif

cat <<'EOF' > run-tests.sh
#!/bin/sh
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL || :
%{__make} test \
	EXTENSION_DIR=modules \
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS= \
	RUN_TESTS_SETTINGS="-q $*"
EOF
chmod +x run-tests.sh

%if %{with tests}
# Run tests, using the CLI SAPI
cp -pf php_config.h.cli main/php_config.h
cp -pf Makefile.cli Makefile

./run-tests.sh -w failed.log -s tests.log

# collect failed tests into cleanup script used in prep.
sed -ne '/^FAILED TEST SUMMARY/,/^===/p' tests.log | sed -e '1,/^---/d;/^===/,$d' > tests-failed.log
sed -ne '/^via/d;/\[.*\]/{s/\t*\(.*\) \[\(.*\)\]\(.*\)/# \1\3\nmv \2{,.skip}/p}' tests-failed.log \
	>> %{_sourcedir}/skip-tests.sh

# if on builders, dump test log
tty -q || cat tests.log

test ! -s failed.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/{php,apache{,1}},%{_sysconfdir}/{apache,cgi}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_bindir}} \
	$RPM_BUILD_ROOT/etc/{apache/conf.d,httpd/conf.d} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,8} \

cp -pf php_config.h.cli main/php_config.h
cp -pf Makefile.cli Makefile
%{__make} install \
	phpbuilddir=%{_libdir}/%{name}/build \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# make link relative
ln -sfn phar.phar $RPM_BUILD_ROOT%{_bindir}/phar

# version suffix
v=$(echo %{version} | cut -d. -f1-2)

# install Apache1 DSO module
%if %{with apache1}
libtool --mode=install install -p sapi/apache/libphp5.la $RPM_BUILD_ROOT%{_libdir}/apache1
mv $RPM_BUILD_ROOT%{_libdir}/apache1/libphp5{,-$v}.so
ln -s libphp5-$v.so $RPM_BUILD_ROOT%{_libdir}/apache1/libphp5.so
%endif

# install Apache2 DSO module
%if %{with apache2}
libtool --mode=install install -p sapi/apache2handler/libphp5.la $RPM_BUILD_ROOT%{_libdir}/apache
mv $RPM_BUILD_ROOT%{_libdir}/apache/libphp5{,-$v}.so
ln -s libphp5-$v.so $RPM_BUILD_ROOT%{_libdir}/apache/libphp5.so
%endif

# install litespeed sapi
%if %{with litespeed}
libtool --mode=install install -p sapi/litespeed/php $RPM_BUILD_ROOT%{_sbindir}/%{name}.litespeed
%endif

libtool --mode=install install -p libphp_common.la $RPM_BUILD_ROOT%{_libdir}

# install CGI/FCGI
%if %{with cgi}
# install-cgi
libtool --mode=install install -p sapi/cgi/php-cgi $RPM_BUILD_ROOT%{_bindir}/%{name}.cgi
ln -sf %{name}.cgi $RPM_BUILD_ROOT%{_bindir}/%{name}.fcgi
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/php-cgi-fcgi.ini
%endif

# install FCGI PM
%if %{with fpm}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/fpm.d,%{_sbindir}}
libtool --mode=install install -p sapi/fpm/php-fpm $RPM_BUILD_ROOT%{_sbindir}/%{name}-fpm
cp -p sapi/fpm/php-fpm.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}-fpm.8
cp -p sapi/fpm/php-fpm.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p sapi/fpm/php-fpm.conf-d $RPM_BUILD_ROOT%{_sysconfdir}/fpm.d/www.conf
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -p %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-fpm
install -d $RPM_BUILD_ROOT/etc/logrotate.d
cp -p %{SOURCE11} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}-fpm
%if "%{pld_release}" == "ac"
%{__sed} -i -e '/su/d' $RPM_BUILD_ROOT/etc/logrotate.d/%{name}-fpm
%endif

%{__sed} -i -e '
	s#/usr/lib/php#%{php_extensiondir}#
	s#/etc/php#%{_sysconfdir}#
	s#@processname@#%{name}-fpm#g
' $RPM_BUILD_ROOT{/etc/{rc.d/init.d/%{name}-fpm,logrotate.d/%{name}-fpm},%{_sysconfdir}/php-fpm.conf,%{_sysconfdir}/fpm.d/www.conf}
%endif

# install Embedded API
%if %{with embed}
# we could use install-headers from Makefile.embed, but that would reinstall all headers
# install-sapi installs to wrong dir, so just do it all manually
install -d $RPM_BUILD_ROOT%{_includedir}/php/sapi/embed
install -p libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}
cp -p sapi/embed/php_embed.h $RPM_BUILD_ROOT%{_includedir}/php/sapi/embed
%endif

# install CLI
# versioned suffix is always installed
libtool --mode=install install -p sapi/cli/php $RPM_BUILD_ROOT%{_bindir}/php%{ver_suffix}
cp -p sapi/cli/php.1 $RPM_BUILD_ROOT%{_mandir}/man1/php%{ver_suffix}.1
echo ".so php%{ver_suffix}.1" >$RPM_BUILD_ROOT%{_mandir}/man1/php.1
ln -sf php%{ver_suffix} $RPM_BUILD_ROOT%{_bindir}/php

cp -p php.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.ini

cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-cli.ini
cp -p %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/browscap.ini

%if %{with apache1}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/apache/conf.d/70_mod_php.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-apache.ini
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/apache1/libphp5.la
%endif

%if %{with apache2}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/70_mod_php.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-apache2handler.ini
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/apache/libphp5.la
%endif

# ensure that paths are correct for current php version and arch
grep -El '/etc/php/|/usr/lib/php/' $RPM_BUILD_ROOT%{_sysconfdir}/*.ini | xargs -r \
%{__sed} -i -e '
	s#/usr/lib/php#%{php_extensiondir}#
	s#/etc/php#%{_sysconfdir}#
'

install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d
cp -p conf.d/*.ini $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

# per SAPI ini directories
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cgi-fcgi,cli,apache,apache2handler}.d

# for CLI SAPI only
mv $RPM_BUILD_ROOT%{_sysconfdir}/{conf.d/readline.ini,cli.d}

# use system automake and {lib,sh}tool
ln -snf /usr/share/automake/config.{guess,sub} $RPM_BUILD_ROOT%{_libdir}/%{name}/build
ln -snf %{_bindir}/shtool $RPM_BUILD_ROOT%{_libdir}/%{name}/build
for fn in libtool.m4 lt~obsolete.m4 ltoptions.m4 ltsugar.m4 ltversion.m4; do
	f=%{_aclocaldir}/$fn
	test -f $f || continue
	ln -snf $f $RPM_BUILD_ROOT%{_libdir}/%{name}/build
done
for fn in ltmain.sh config/ltmain.sh build-aux/ltmain.sh; do
	f=/usr/share/libtool/$fn
	test -f $f || continue
	ln -snf $f $RPM_BUILD_ROOT%{_libdir}/%{name}/build
	break
done
sed -i -e '/^phpdir/ s,/php/build,/%{name}/build,' $RPM_BUILD_ROOT%{_bindir}/phpize

# for php-pecl-mailparse
install -d $RPM_BUILD_ROOT%{_includedir}/php/ext/mbstring
cp -p ext/mbstring/libmbfl/mbfl/*.h $RPM_BUILD_ROOT%{_includedir}/php/ext/mbstring

# tests
install -d $RPM_BUILD_ROOT%{php_data_dir}/tests/php
install -p run-tests.php $RPM_BUILD_ROOT%{php_data_dir}/tests/php/run-tests.php
cp -a tests/* $RPM_BUILD_ROOT%{php_data_dir}/tests/php

# fix install paths, avoid evil rpaths
sed -i -e "s|^libdir=.*|libdir='%{_libdir}'|" $RPM_BUILD_ROOT%{_libdir}/libphp_common.la
# better solution?
sed -i -e 's|libphp_common.la|$(libdir)/libphp_common.la|' $RPM_BUILD_ROOT%{_libdir}/%{name}/build/acinclude.m4

%clean
rm -rf $RPM_BUILD_ROOT

%post -n apache1-mod_%{name}
if [ "$1" = "1" ]; then
	%service -q apache restart
fi

%postun -n apache1-mod_%{name}
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%post -n apache-mod_%{name}
if [ "$1" = "1" ]; then
	%service -q httpd restart
fi

%postun -n apache-mod_%{name}
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%pre fpm
%useradd -u 51 -r -s /bin/false -c "HTTP User" -g http http

%post fpm
/sbin/chkconfig --add %{name}-fpm
%service %{name}-fpm restart

%preun fpm
if [ "$1" = 0 ]; then
	%service %{name}-fpm stop
	/sbin/chkconfig --del %{name}-fpm
fi

%postun fpm
if [ "$1" = "0" ]; then
	%userremove http
fi

%post	embedded -p /sbin/ldconfig
%postun	embedded -p /sbin/ldconfig

%post common
# PHP 5.3 requires timezone being setup, try setup it from tzdata
if ! grep -q '^date.timezone[[:space:]]*=' %{_sysconfdir}/php.ini && [ -f /etc/sysconfig/timezone ]; then
	TIMEZONE=
	. /etc/sysconfig/timezone
	if [ "$TIMEZONE" ]; then
		%{__sed} -i -e "s,^;date.timezone[[:space:]]*=.*,date.timezone = $TIMEZONE," %{_sysconfdir}/php.ini
	fi
fi

%posttrans common
# minimizing apache restarts logics. we restart webserver:
#
# 1. at the end of transaction. (posttrans, feature from rpm 4.4.2)
# 2. first install of extension (post: $1 = 1)
# 2. uninstall of extension (postun: $1 == 0)
#
# the strict internal deps between extensions (and apache modules) and
# common package are very important for all this to work.

# restart webserver at the end of transaction
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/conf.d/??_mod_php.conf ] || %service -q httpd restart

%triggerpostun common -- php-common < 4:5.3.28-7
# migrate configs /etc/php/conf.d -> /etc/phpXY/conf.d/
# do config migration in php-common trigger, as the trigger is ran after all packages are upgraded
# this way we can stick to one trigger, instead of attaching one for each (sub)package!
for f in /etc/php/*.ini.rpmsave /etc/php/*.d/*.ini.rpmsave; do
	test -f "$f" || continue
	bn=${f#/etc/php/}
	dn=${bn%/*}
	fn=${bn#*/}
	test "$dn" = "$fn" && dn=
	fn=${fn%.rpmsave}
	nf=%{_sysconfdir}/$dn/$fn
	test -f "$nf" || continue
	cp -vf $nf{,.rpmnew}
	mv -vf $f $nf
	%{__sed} -i -e '
		s#%{_libdir}/php#%{_libdir}/%{name}#
		s#/etc/php#%{_sysconfdir}#
	' $nf
done

# common macros called at extension post/postun scriptlet
%define	extension_scripts() \
%post %1 \
if [ "$1" = "1" ]; then \
	%php_webserver_restart \
fi \
\
%postun %1 \
if [ "$1" = "0" ]; then \
	%php_webserver_restart \
fi
%{nil}

# extension scripts defines
%extension_scripts bcmath
%extension_scripts bz2
%extension_scripts calendar
%extension_scripts ctype
%extension_scripts curl
%extension_scripts dba
%extension_scripts dom
%extension_scripts enchant
%extension_scripts exif
%extension_scripts fileinfo
%extension_scripts filter
%extension_scripts ftp
%extension_scripts gd
%extension_scripts gettext
%extension_scripts gmp
%extension_scripts hash
%extension_scripts iconv
%extension_scripts imap
%extension_scripts interbase
%extension_scripts intl
%extension_scripts json
%extension_scripts ldap
%extension_scripts mbstring
%extension_scripts mcrypt
%extension_scripts mssql
%extension_scripts mysql
%extension_scripts mysqli
%extension_scripts mysqlnd
%extension_scripts oci8
%extension_scripts odbc
%extension_scripts opcache
%extension_scripts openssl
%extension_scripts pcre
%extension_scripts pdo
%extension_scripts pdo-dblib
%extension_scripts pdo-firebird
%extension_scripts pdo-oci
%extension_scripts pdo-mysql
%extension_scripts pdo-odbc
%extension_scripts pdo-pgsql
%extension_scripts pdo-sqlite
%extension_scripts pgsql
%extension_scripts phar
%extension_scripts pcntl
%extension_scripts posix
%extension_scripts pspell
%extension_scripts recode
%extension_scripts session
%extension_scripts shmop
%extension_scripts simplexml
%extension_scripts snmp
%extension_scripts soap
%extension_scripts sockets
%extension_scripts spl
%extension_scripts sqlite3
%extension_scripts sybase-ct
%extension_scripts sysvmsg
%extension_scripts sysvsem
%extension_scripts sysvshm
%extension_scripts tidy
%extension_scripts tokenizer
%extension_scripts wddx
%extension_scripts xml
%extension_scripts xmlreader
%extension_scripts xmlrpc
%extension_scripts xmlwriter
%extension_scripts xsl
%extension_scripts zip
%extension_scripts zlib

%if %{with apache1}
%files -n apache1-mod_%{name}
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/apache/conf.d/*_mod_php.conf
%dir %{_sysconfdir}/apache.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php-apache.ini
%attr(755,root,root) %{_libdir}/apache1/libphp5.so
%attr(755,root,root) %{_libdir}/apache1/libphp5-*.*.so
%endif

%if %{with apache2}
%files -n apache-mod_%{name}
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/httpd/conf.d/*_mod_php.conf
%dir %{_sysconfdir}/apache2handler.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php-apache2handler.ini
%attr(755,root,root) %{_libdir}/apache/libphp5.so
%attr(755,root,root) %{_libdir}/apache/libphp5-*.*.so
%endif

%if %{with litespeed}
%files litespeed
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{name}.litespeed
%endif

%if %{with cgi}
%files cgi
%defattr(644,root,root,755)
%dir %{_sysconfdir}/cgi-fcgi.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php-cgi-fcgi.ini
%attr(755,root,root) %{_bindir}/%{name}.cgi
%attr(755,root,root) %{_bindir}/%{name}.fcgi
%endif

%if %{with embed}
%files embedded
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libphp5.so
%endif

%files cli
%defattr(644,root,root,755)
%dir %{_sysconfdir}/cli.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php-cli.ini
%attr(755,root,root) %{_bindir}/php%{ver_suffix}
%{_mandir}/man1/php%{ver_suffix}.1*

%files program
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php
%{_mandir}/man1/php.1*

%if %{with fpm}
%files fpm
%defattr(644,root,root,755)
%doc sapi/fpm/{CREDITS,LICENSE}
%dir %{_sysconfdir}/fpm.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fpm.d/www.conf
%attr(755,root,root) %{_sbindir}/%{name}-fpm
%{_mandir}/man8/%{name}-fpm.8*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}-fpm
%attr(754,root,root) /etc/rc.d/init.d/%{name}-fpm
%endif

%files common
%defattr(644,root,root,755)
%doc CREDITS EXTENSIONS LICENSE NEWS README.{PHP4-TO-PHP5-THIN-CHANGES,namespaces} UPGRADING* Zend/{LICENSE.Zend,ZEND_CHANGES} php.ini-*
%dir %{_sysconfdir}
%dir %{_sysconfdir}/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/browscap.ini
%attr(755,root,root) %{_libdir}/libphp_common-*.so
%dir %{php_extensiondir}

%doc ext/session/mod_files.sh

%files devel
%defattr(644,root,root,755)
%doc CODING_STANDARDS README.{EXTENSIONS,EXT_SKEL,PARAMETER_PARSING_API,SELF-CONTAINED-EXTENSIONS,STREAMS,SUBMITTING_PATCH,TESTING,TESTING2,UNIX-BUILD-SYSTEM,input_filter}
%attr(755,root,root) %{_bindir}/phpize
%attr(755,root,root) %{_bindir}/php-config
%attr(755,root,root) %{_libdir}/libphp_common.so
%{_libdir}/libphp_common.la
%{_includedir}/php
%{_libdir}/%{name}/build
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*

%files bcmath
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/bcmath.ini
%attr(755,root,root) %{php_extensiondir}/bcmath.so

%files bz2
%defattr(644,root,root,755)
%doc ext/bz2/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/bz2.ini
%attr(755,root,root) %{php_extensiondir}/bz2.so

%files calendar
%defattr(644,root,root,755)
%doc ext/calendar/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/calendar.ini
%attr(755,root,root) %{php_extensiondir}/calendar.so

%files ctype
%defattr(644,root,root,755)
%doc ext/calendar/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/ctype.ini
%attr(755,root,root) %{php_extensiondir}/ctype.so

%if %{with curl}
%files curl
%defattr(644,root,root,755)
%doc ext/curl/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/curl.ini
%attr(755,root,root) %{php_extensiondir}/curl.so
%endif

%files dba
%defattr(644,root,root,755)
%doc ext/dba/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/dba.ini
%attr(755,root,root) %{php_extensiondir}/dba.so

%files dom
%defattr(644,root,root,755)
%doc ext/dom/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/dom.ini
%attr(755,root,root) %{php_extensiondir}/dom.so

%if %{with enchant}
%files enchant
%defattr(644,root,root,755)
%doc ext/enchant/{CREDITS,docs/examples}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/enchant.ini
%attr(755,root,root) %{php_extensiondir}/enchant.so
%endif

%files exif
%defattr(644,root,root,755)
%doc ext/exif/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/exif.ini
%attr(755,root,root) %{php_extensiondir}/exif.so

%files fileinfo
%defattr(644,root,root,755)
%doc ext/fileinfo/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/fileinfo.ini
%attr(755,root,root) %{php_extensiondir}/fileinfo.so

%if %{with filter}
%files filter
%defattr(644,root,root,755)
%doc ext/filter/{CREDITS,docs/*}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/filter.ini
%attr(755,root,root) %{php_extensiondir}/filter.so
%endif

%files ftp
%defattr(644,root,root,755)
%doc ext/ftp/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/ftp.ini
%attr(755,root,root) %{php_extensiondir}/ftp.so

%files gd
%defattr(644,root,root,755)
%doc ext/gd/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/gd.ini
%attr(755,root,root) %{php_extensiondir}/gd.so

%files gettext
%defattr(644,root,root,755)
%doc ext/gettext/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/gettext.ini
%attr(755,root,root) %{php_extensiondir}/gettext.so

%files gmp
%defattr(644,root,root,755)
%doc ext/gmp/{CREDITS,README,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/gmp.ini
%attr(755,root,root) %{php_extensiondir}/gmp.so

%files hash
%defattr(644,root,root,755)
%doc ext/hash/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/hash.ini
%attr(755,root,root) %{php_extensiondir}/hash.so

%files iconv
%defattr(644,root,root,755)
%doc ext/iconv/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/iconv.ini
%attr(755,root,root) %{php_extensiondir}/iconv.so

%if %{with imap}
%files imap
%defattr(644,root,root,755)
%doc ext/imap/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/imap.ini
%attr(755,root,root) %{php_extensiondir}/imap.so
%endif

%if %{with interbase}
%files interbase
%defattr(644,root,root,755)
%doc ext/interbase/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/interbase.ini
%attr(755,root,root) %{php_extensiondir}/interbase.so
%endif

%if %{with intl}
%files intl
%defattr(644,root,root,755)
%doc ext/intl/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/intl.ini
%attr(755,root,root) %{php_extensiondir}/intl.so
%endif

%files json
%defattr(644,root,root,755)
%doc ext/json/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/json.ini
%attr(755,root,root) %{php_extensiondir}/json.so

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%doc ext/ldap/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/ldap.ini
%attr(755,root,root) %{php_extensiondir}/ldap.so
%endif

%files mbstring
%defattr(644,root,root,755)
%doc ext/mbstring/{CREDITS,README*}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/mbstring.ini
%attr(755,root,root) %{php_extensiondir}/mbstring.so

%files mcrypt
%defattr(644,root,root,755)
%doc ext/mcrypt/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/mcrypt.ini
%attr(755,root,root) %{php_extensiondir}/mcrypt.so

%if %{with mssql}
%files mssql
%defattr(644,root,root,755)
%doc ext/mssql/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/mssql.ini
%attr(755,root,root) %{php_extensiondir}/mssql.so
%endif

%files mysql
%defattr(644,root,root,755)
%doc ext/mysql/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/mysql.ini
%attr(755,root,root) %{php_extensiondir}/mysql.so

%if %{with mysqli}
%files mysqli
%defattr(644,root,root,755)
%doc ext/mysqli/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/mysqli.ini
%attr(755,root,root) %{php_extensiondir}/mysqli.so
%endif

%if %{with mysqlnd}
%files mysqlnd
%defattr(644,root,root,755)
%doc ext/mysqlnd/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/MySQLND.ini
%attr(755,root,root) %{php_extensiondir}/mysqlnd.so
%endif

%if %{with oci}
%files oci8
%defattr(644,root,root,755)
%doc ext/oci8/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/oci8.ini
%attr(755,root,root) %{php_extensiondir}/oci8.so
%endif

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%doc ext/odbc/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/odbc.ini
%attr(755,root,root) %{php_extensiondir}/odbc.so
%endif

%if %{with opcache}
%files opcache
%defattr(644,root,root,755)
%doc ext/opcache/README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/opcache.ini
%attr(755,root,root) %{php_extensiondir}/opcache.so
%endif

%if %{with openssl}
%files openssl
%defattr(644,root,root,755)
%doc ext/openssl/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/openssl.ini
%attr(755,root,root) %{php_extensiondir}/openssl.so
%endif

%files pcntl
%defattr(644,root,root,755)
%doc ext/pcntl/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pcntl.ini
%attr(755,root,root) %{php_extensiondir}/pcntl.so

%if %{with pcre}
%files pcre
%defattr(644,root,root,755)
%doc ext/pcre/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/PCRE.ini
%attr(755,root,root) %{php_extensiondir}/pcre.so
%endif

%files pdo
%defattr(644,root,root,755)
%doc ext/pdo/{CREDITS,README,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo.ini
%attr(755,root,root) %{php_extensiondir}/pdo.so

%if %{with mssql} || %{with sybase_ct}
%files pdo-dblib
%defattr(644,root,root,755)
%doc ext/pdo_dblib/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_dblib.ini
%attr(755,root,root) %{php_extensiondir}/pdo_dblib.so
%endif

%if %{with interbase} && !%{with interbase_inst}
%files pdo-firebird
%defattr(644,root,root,755)
%doc ext/pdo_firebird/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_firebird.ini
%attr(755,root,root) %{php_extensiondir}/pdo_firebird.so
%endif

%files pdo-mysql
%defattr(644,root,root,755)
%doc ext/pdo_mysql/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_mysql.ini
%attr(755,root,root) %{php_extensiondir}/pdo_mysql.so

%if %{with oci}
%files pdo-oci
%defattr(644,root,root,755)
%doc ext/pdo_oci/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_oci.ini
%attr(755,root,root) %{php_extensiondir}/pdo_oci.so
%endif

%if %{with odbc}
%files pdo-odbc
%defattr(644,root,root,755)
%doc ext/pdo_odbc/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_odbc.ini
%attr(755,root,root) %{php_extensiondir}/pdo_odbc.so
%endif

%if %{with pgsql}
%files pdo-pgsql
%defattr(644,root,root,755)
%doc ext/pdo_pgsql/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_pgsql.ini
%attr(755,root,root) %{php_extensiondir}/pdo_pgsql.so
%endif

%if %{with pdo_sqlite}
%files pdo-sqlite
%defattr(644,root,root,755)
%doc ext/pdo_sqlite/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pdo_sqlite.ini
%attr(755,root,root) %{php_extensiondir}/pdo_sqlite.so
%endif

%if %{with pgsql}
%files pgsql
%defattr(644,root,root,755)
%doc ext/pgsql/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pgsql.ini
%attr(755,root,root) %{php_extensiondir}/pgsql.so
%endif

%if %{with phar}
%files phar
%defattr(644,root,root,755)
%doc ext/phar/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/phar.ini
%attr(755,root,root) %{php_extensiondir}/phar.so
%attr(755,root,root) %{_bindir}/phar
%attr(755,root,root) %{_bindir}/phar.phar
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1
%endif

%files posix
%defattr(644,root,root,755)
%doc ext/posix/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/posix.ini
%attr(755,root,root) %{php_extensiondir}/posix.so

%if %{with pspell}
%files pspell
%defattr(644,root,root,755)
%doc ext/pspell/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/pspell.ini
%attr(755,root,root) %{php_extensiondir}/pspell.so
%endif

%files readline
%defattr(644,root,root,755)
%doc ext/readline/{CREDITS,README*}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cli.d/readline.ini
%attr(755,root,root) %{php_extensiondir}/readline.so

%if %{with recode}
%files recode
%defattr(644,root,root,755)
%doc ext/recode/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/recode.ini
%attr(755,root,root) %{php_extensiondir}/recode.so
%endif

%files session
%defattr(644,root,root,755)
%doc ext/session/CREDITS
%doc ext/session/mod_files.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/Session.ini
%attr(755,root,root) %{php_extensiondir}/session.so

%files shmop
%defattr(644,root,root,755)
%doc ext/shmop/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/shmop.ini
%attr(755,root,root) %{php_extensiondir}/shmop.so

%files simplexml
%defattr(644,root,root,755)
%doc ext/simplexml/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/simplexml.ini
%attr(755,root,root) %{php_extensiondir}/simplexml.so

%if %{with snmp}
%files snmp
%defattr(644,root,root,755)
%doc ext/snmp/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/snmp.ini
%attr(755,root,root) %{php_extensiondir}/snmp.so
%endif

%files soap
%defattr(644,root,root,755)
%doc ext/soap/{CREDITS,TODO*}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/soap.ini
%attr(755,root,root) %{php_extensiondir}/soap.so

%files sockets
%defattr(644,root,root,755)
%doc ext/sockets/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sockets.ini
%attr(755,root,root) %{php_extensiondir}/sockets.so

%files spl
%defattr(644,root,root,755)
%doc ext/spl/{CREDITS,README,TODO,examples}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/SPL.ini
%attr(755,root,root) %{php_extensiondir}/spl.so

%if %{with sqlite3}
%files sqlite3
%defattr(644,root,root,755)
%doc ext/sqlite3/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sqlite3.ini
%attr(755,root,root) %{php_extensiondir}/sqlite3.so
%endif

%if %{with sybase_ct}
%files sybase-ct
%defattr(644,root,root,755)
%doc ext/sybase_ct/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sybase_ct.ini
%attr(755,root,root) %{php_extensiondir}/sybase_ct.so
%endif

%files sysvmsg
%defattr(644,root,root,755)
%doc ext/sysvmsg/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sysvmsg.ini
%attr(755,root,root) %{php_extensiondir}/sysvmsg.so

%files sysvsem
%defattr(644,root,root,755)
%doc ext/sysvsem/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sysvsem.ini
%attr(755,root,root) %{php_extensiondir}/sysvsem.so

%files sysvshm
%defattr(644,root,root,755)
%doc ext/sysvshm/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/sysvshm.ini
%attr(755,root,root) %{php_extensiondir}/sysvshm.so

%files tests
%defattr(644,root,root,755)
%dir %{php_data_dir}/tests
%dir %{php_data_dir}/tests/php
%{php_data_dir}/tests/php/basic
%{php_data_dir}/tests/php/classes
%{php_data_dir}/tests/php/func
%{php_data_dir}/tests/php/lang
%{php_data_dir}/tests/php/output
%{php_data_dir}/tests/php/run-test
%{php_data_dir}/tests/php/security
%{php_data_dir}/tests/php/strings
%{php_data_dir}/tests/php/quicktester.inc
%attr(755,root,root) %{php_data_dir}/tests/php/run-tests.php

%if %{with tidy}
%files tidy
%defattr(644,root,root,755)
%doc ext/tidy/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/tidy.ini
%attr(755,root,root) %{php_extensiondir}/tidy.so
%endif

%files tokenizer
%defattr(644,root,root,755)
%doc ext/tokenizer/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/tokenizer.ini
%attr(755,root,root) %{php_extensiondir}/tokenizer.so

%if %{with wddx}
%files wddx
%defattr(644,root,root,755)
%doc ext/wddx/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*wddx.ini
%attr(755,root,root) %{php_extensiondir}/wddx.so
%endif

%files xml
%defattr(644,root,root,755)
%doc ext/xml/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/xml.ini
%attr(755,root,root) %{php_extensiondir}/xml.so

%files xmlreader
%defattr(644,root,root,755)
%doc ext/xmlreader/{CREDITS,README,TODO,examples}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/xmlreader.ini
%attr(755,root,root) %{php_extensiondir}/xmlreader.so

%if %{with xmlrpc}
%files xmlrpc
%defattr(644,root,root,755)
%doc ext/xmlrpc/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/xmlrpc.ini
%attr(755,root,root) %{php_extensiondir}/xmlrpc.so
%endif

%files xmlwriter
%defattr(644,root,root,755)
%doc ext/xmlwriter/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/xmlwriter.ini
%attr(755,root,root) %{php_extensiondir}/xmlwriter.so

%files xsl
%defattr(644,root,root,755)
%doc ext/xsl/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/xsl.ini
%attr(755,root,root) %{php_extensiondir}/xsl.so

%files zip
%defattr(644,root,root,755)
%doc ext/zip/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/zip.ini
%attr(755,root,root) %{php_extensiondir}/zip.so

%files zlib
%defattr(644,root,root,755)
%doc ext/zlib/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/zlib.ini
%attr(755,root,root) %{php_extensiondir}/zlib.so
