#
# TODO:
# - php-shared is SERIOUSLY broken. Try compiling with --enable-versioning.
# - think of including support for:
#    - mcve,
#    - ovrimos,
#    - pfpro,
#    - ircg,
#   These extensions BuildRequires proprietary libraries...
# - deal with modules removed from php and not moved to PECL
#   (existing only in php4):
#   db, hyperwave, java, mcal, overload, qtdom
# - mime_magic can't handle new "string/*" entries in magic.mime
# - make additional headers added by mail patch configurable
# - apply -hardened patch by default ?
#
# Conditional build:
%bcond_with	db3		# use db3 packages instead of db (4.x) for Berkeley DB support
%bcond_with	fdf		# with FDF (PDF forms) module		(BR: proprietary lib)
%bcond_with	hardened	# build with hardened patch applied (http://www.hardened-php.net/)
%bcond_with	hwapi		# with Hw API support			(BR: proprietary libs)
%bcond_with	interbase_inst	# use InterBase install., not Firebird	(BR: proprietary libs)
%bcond_with	oci8		# with Oracle oci8 extension module	(BR: proprietary libs)
%bcond_with	oracle		# with oracle extension module		(BR: proprietary libs)
%bcond_with	apache1		# build with apache1
%bcond_without	mysqli		# with mysqli support (Requires mysql > 4.1)
%bcond_without	cpdf		# without cpdf extension module
%bcond_without	curl		# without CURL extension module
%bcond_without	fam		# without FAM (File Alteration Monitor) extension module
%bcond_without	imap		# without IMAP extension module
%bcond_with		interbase	# without InterBase extension module
%bcond_without	ldap		# without LDAP extension module
%bcond_without	mhash		# without mhash extension module
%bcond_without	ming		# without ming extension module
%bcond_without	mm		# without mm support for session storage
%bcond_without	mnogosearch	# without mnogosearch extension module
%bcond_without	msession	# without msession extension module
%bcond_without	mssql		# without MS SQL extension module
%bcond_without	odbc		# without ODBC extension module
%bcond_without	openssl		# without OpenSSL support and OpenSSL extension (module)
%bcond_without	pcre		# without PCRE extension module
%bcond_without	pgsql		# without PostgreSQL extension module
%bcond_without	pspell		# without pspell extension module
%bcond_without	recode		# without recode extension module
%bcond_without	snmp		# without SNMP extension module
%bcond_without	sqlite		# without SQLite extension module
%bcond_without	sybase		# without Sybase extension module
%bcond_without	sybase_ct	# without Sybase-CT extension module
%bcond_without	tidy		# without Tidy extension module
%bcond_without	wddx		# without WDDX extension module
%bcond_without	xmlrpc		# without XML-RPC extension module

%define	_apache2	%{?with_apache1:0}%{!?with_apache1:1}
%if %{_apache2}
%define	apxs		/usr/sbin/apxs
%else
%define	apxs		/usr/sbin/apxs1
%endif
# some problems with apache 2.x
%if %{_apache2}
%undefine	with_mm
%endif
%ifnarch %{ix86} amd64 sparc sparcv9 alpha ppc
%undefine	with_interbase
%endif
# x86-only lib
%ifnarch %{ix86}
%undefine	with_msession
%endif
%include	/usr/lib/rpm/macros.php
Summary:	The PHP HTML-embedded scripting language for use with Apache
Summary(fr):	Le langage de script embarque-HTML PHP pour Apache
Summary(pl):	J�zyk skryptowy PHP - u�ywany wraz z serwerem Apache
Summary(pt_BR):	A linguagem de script PHP
Summary(ru):	PHP ������ 5 - ���� ������������������ HTML-������, ����������� �� �������
Summary(uk):	PHP ���Ӧ� 5 - ���� ��������������� HTML-���̦�, ���������� �� �����Ҧ
Name:		php
Version:	5.0.4
Release:	5%{?with_hardened:hardened}
Epoch:		4
Group:		Libraries
License:	PHP
Source0:	http://www.php.net/distributions/%{name}-%{version}.tar.bz2
# Source0-md5:	fb1aac107870f897d26563a9cc5053c0
Source1:	FAQ.%{name}
Source2:	zend.gif
Source3:	%{name}-module-install
Source4:	%{name}-mod_%{name}.conf
Source5:	%{name}-cgi-fcgi.ini
Source6:	%{name}-cgi.ini
Source7:	%{name}-apache.ini
Source8:	%{name}-cli.ini
Source9:	http://www.hardened-php.net/hardened-php-5.0.4-0.2.7.patch.gz
# Source9-md5:	60b3a09d4ea271961a0abe480a5368a2
Patch0:		%{name}-shared.patch
Patch1:		%{name}-pldlogo.patch
Patch2:		%{name}-mail.patch
Patch3:		%{name}-link-libs.patch
Patch4:		%{name}-libpq_fs_h_path.patch
Patch5:		%{name}-msession-shared-lib.patch
Patch6:		%{name}-build_modules.patch
Patch7:		%{name}-sapi-ini-file.patch
Patch8:		%{name}-no-metaccld.patch
Patch9:		%{name}-session-unregister.patch
Patch10:	%{name}-ini.patch
Patch11:	%{name}-acam.patch
Patch12:	%{name}-xmlrpc-fix.patch
Patch13:	%{name}-libtool.patch
Patch14:	%{name}-allow-db31.patch
Patch15:	%{name}-threads-acfix.patch
Patch16:	%{name}-tsrmlsfetchgcc2.patch
Patch17:	%{name}-no_pear_install.patch
Patch18:	%{name}-zlib.patch
Patch19:	%{name}-sybase-fix.patch
Patch20:	%{name}-mnogosearch-fix.patch
Patch21:	%{name}-nohttpd.patch
Patch22:	%{name}-lib64.patch
Patch23:	%{name}-gd_imagerotate_enable.patch
Patch24:	%{name}-uint32_t.patch
Patch25:	%{name}-hwapi-link.patch
Patch26:	%{name}-dba-link.patch
Patch27:	%{name}-install_gd_headers.patch
Patch28:	%{name}-cpdf-fix.patch
Patch29:	%{name}-gcc4.patch
Icon:		php.gif
URL:		http://www.php.net/
%{?with_interbase:%{!?with_interbase_inst:BuildRequires:	Firebird-devel >= 1.0.2.908-2}}
%{?with_pspell:BuildRequires:	aspell-devel >= 2:0.50.0}
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.4d
BuildRequires:	bison
BuildRequires:	bzip2-devel
%{?with_curl:BuildRequires:	curl-devel >= 7.12.0}
BuildRequires:	cyrus-sasl-devel
%{?with_db3:BuildRequires:	db3-devel >= 3.1}
%{!?with_db3:BuildRequires:	db-devel >= 4.0}
BuildRequires:	elfutils-devel
%if %{with xmlrpc}
BuildRequires:	expat-devel
%endif
%{?with_fam:BuildRequires:	fam-devel}
%{?with_fdf:BuildRequires:	fdftk-devel}
BuildRequires:	fcgi-devel
BuildRequires:	flex
%if %{with mssql} || %{with sybase} || %{with sybase_ct}
BuildRequires:	freetds-devel
%endif
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gd-devel >= 2.0.28-4
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
%{?with_imap:BuildRequires:	imap-devel >= 1:2001-0.BETA.200107022325.2}
%{?with_cpdf:BuildRequires:	libcpdf-devel >= 2.02r1-2}
BuildRequires:	libjpeg-devel
BuildRequires:	libltdl-devel >= 1.4
BuildRequires:	libmcrypt-devel >= 2.4.4
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 1.4.3
BuildRequires:	libxml2-devel >= 2.5.10
BuildRequires:	libxslt-devel >= 1.0.18
%{?with_mhash:BuildRequires:	mhash-devel}
%{?with_ming:BuildRequires:	ming-devel >= 0.1.0}
%{?with_mm:BuildRequires:	mm-devel >= 1.3.0}
%{?with_mnogosearch:BuildRequires:	mnogosearch-devel >= 3.2.6}
BuildRequires:	mysql-devel >= 4.0.0
%{?with_mysqli:BuildRequires:	mysql-devel >= 4.1.0}
BuildRequires:	ncurses-ext-devel
%{?with_ldap:BuildRequires:	openldap-devel >= 2.0}
%if %{with openssl} || %{with ldap}
BuildRequires:	openssl-devel >= 0.9.7d
%endif
BuildRequires:	pam-devel
BuildRequires:	%{__perl}
%{?with_msession:BuildRequires:	phoenix-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_pgsql:BuildRequires:	postgresql-backend-devel >= 7.2}
BuildRequires:	readline-devel
%{?with_recode:BuildRequires:	recode-devel >= 3.5d-3}
BuildRequires:	rpm-php-pearprov >= 4.0.2-100
BuildRequires:	rpmbuild(macros) >= 1.120
%{?with_sqlite:BuildRequires:	sqlite-devel}
BuildRequires:	t1lib-devel
%{?with_tidy:BuildRequires:	tidy-devel}
%{?with_snmp:BuildRequires:	net-snmp-devel >= 5.0.7}
%{?with_odbc:BuildRequires:	unixODBC-devel}
%{?with_xmlrpc:BuildRequires:	xmlrpc-epi-devel}
BuildRequires:	zlib-devel >= 1.0.9
# apache 1.3 vs apache 2.0
%if %{_apache2}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	apr-util-devel >= 1:1.0.0
PreReq:		apache >= 2.0.52-2
Requires:	apache(modules-api) = %{apache_modules_api}
%else
BuildRequires:	apache1-devel
PreReq:		apache1(EAPI) >= 1.3.9
Requires(post,preun):	%{apxs}
Requires(post,preun):	%{__perl}
%endif
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	phpfi
Obsoletes:	apache-mod_php
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php
%define		httpdir		/home/services/httpd
%if %{_apache2}
%define		apachelib	%{_libdir}/apache
%else
%define		apachelib	%{_libdir}/apache1
%endif

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. The
mod_php module enables the Apache web server to understand and process
the embedded PHP language in web pages. This package contains php
version %{version}. If you use applications which specifically rely on
PHP/FI (PHP v2 and earlier), you should instead install the PHP/FI
module contained in the phpfi package. If you're just starting with
PHP, you should install this package. You'll also need to install the
Apache web server.

%description -l fr
PHP est un langage de script embarque dans le HTM. PHP essaye de
rendre simple aux developpeurs d'ecrire des pages web generees
dynamiquement. PHP incorpore egalement une integration avec plusieurs
systemes de gestion de bases de donnees commerciaux et
non-connerciaux, qui rent facile la creation de pages web liees avec
des bases de donnees. L'utilisation la plus commune de PHP est
probablement en remplacement de scripts CGI. Le module mod_php permet
au serveur web apache de comprendre et de traiter le langage PHP
integre dans des pages web. Ce package contient php version
%{version}. Si vous utilisez des applications qui utilisent
specifiquement PHP/FI, vous devrez installer le module PHP/FI inclus
dans le package mod_php. Si vous debutez avec PHP, vous devriez
installer ce package. Vous aurez egalement besoin dinstaller le
serveur web Apache.

%description -l pl
PHP jest j�zykiem skryptowym, kt�rego polecenia umieszcza si� w
plikach HTML. Pakiet ten zawiera modu� przeznaczony dla serwera HTTP
(jak np. Apache), kt�ry interpretuje te polecenia. Umo�liwia to
tworzenie dynamicznie stron WWW. Spora cz�� sk�adni PHP zapo�yczona
zosta�a z j�zyk�w: C, Java i Perl.

%description -l pt_BR
PHP: Preprocessador de Hipertexto vers�o 4 � uma linguagem script
embutida em HTML. Muito de sua sintaxe � emprestada de C, Java e Perl,
com algumas caracter�sticas �nicas, espec�ficas ao PHP. O objetivo da
linguagem � permitir que desenvolvedores web escrevam p�ginas
dinamicamente geradas de forma r�pida.

%description -l ru
PHP - ��� ���� ��������� ��������, ������������ � HTML-���. PHP
���������� ����������� � ���������� ����, ������� ��������� ��������
��� ������ � ������ ������ ������������ ������. �������� ����������
������������� PHP - ������ ��� CGI ��������.

���� ����� �������� ��������������� (CGI) ������ �������������� �����.
�� ������ ����� ���������� ����� %{name}-common. ���� ��� �����
������������� PHP � �������� ������ apache, ���������� �����
apache-php.

%description -l uk
PHP - �� ���� ��������� �����Ԧ�, �� ������������ � HTML-���. PHP
������դ �������æ� � �������� ����, ���� ��������� �����Ԧ� ���
������ � ������ ����� � ����̦ �������. ���¦��� ���������
������������ PHP - ��ͦ�� ��� CGI �����Ԧ�.

��� ����� ͦ����� ������������ (CGI) ���Ӧ� �������������� ����. ��
����� ����� ���������� ����� %{name}-common. ���� ��� ���Ҧ���
������������� PHP � ����Ԧ ������ apache, ������צ�� ����� apache-php.

%package fcgi
Summary:	php as FastCGI program
Summary(pl):	php jako program FastCGI
Group:		Development/Languages/PHP
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php-program = %{epoch}:%{version}-%{release}

%description fcgi
php as FastCGI program.

%description fcgi -l pl
php jako program FastCGI.

%package cgi
Summary:	php as CGI program
Summary(pl):	php jako program CGI
Group:		Development/Languages/PHP
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php-program = %{epoch}:%{version}-%{release}

%description cgi
php as CGI program.

%description cgi -l pl
php jako program CGI.

%package cli
Summary:	php as CLI interpreter
Summary(pl):	php jako interpreter dzia�aj�cy z linii polece�
Group:		Development/Languages/PHP
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
Provides:	php-program = %{epoch}:%{version}-%{release}

%description cli
php as CLI interpreter.

%description cli -l pl
php jako interpreter dzia�aj�cy z linii polece�.

%package common
Summary:	Common files needed by both apache module and CGI
Summary(pl):	Wsp�lne pliki dla modu�u apache'a i programu CGI
Summary(ru):	����������� ���������� ��� php
Summary(uk):	��̦����� �Ц������ ������������ ��� php
Group:		Libraries
# because of dlclose() bugs in glibc <= 2.3.4 causing SEGVs on exit
Requires:	glibc >= 6:2.3.5
Provides:	%{name}-session = %{epoch}:%{version}-%{release}
Provides:	php-common(apache-modules-api) = %{apache_modules_api}
Obsoletes:	php-session < 3:4.2.1-2

%description common
Common files needed by both apache module and CGI.

%description common -l pl
Wsp�lne pliki dla modu�u apacha i programu CGI.

%description common -l ru
���� ����� �������� ����� ����� ��� ������ ��������� ���������� PHP
(��������������� � � �������� ������ apache).

%description common -l uk
��� ����� ͦ����� �Ц��Φ ����� ��� Ҧ���� ��Ҧ��Ԧ� ���̦��æ� PHP
(������������ϧ �� � ����Ԧ ������ apache).

%package devel
Summary:	Files for PHP modules development
Summary(pl):	Pliki do kompilacji modu��w PHP
Summary(pt_BR):	Arquivos de desenvolvimento para PHP
Summary(ru):	����� ���������� ��� ���������� ���������� PHP
Summary(uk):	����� �������� ��� �������� ��������� PHP
Group:		Development/Languages/PHP
Requires:	autoconf
Requires:	automake
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	php-pear-devel
Obsoletes:	php4-devel

%description devel
The php-devel package lets you compile dynamic extensions to PHP.
Included here is the source for the PHP extensions. Instead of
recompiling the whole php binary to add support for, say, oracle,
install this package and use the new self-contained extensions
support. For more information, read the file
SELF-CONTAINED-EXTENSIONS.

%description devel -l pl
Pliki potrzebne do kompilacji modu��w PHP.

%description devel -l pt_BR
Este pacote cont�m arquivos usados no desenvolvimento de programas ou
m�dulos PHP.

%description devel -l uk
����� php-devel ��� �����צ��� ���Ц������ ����ͦ�Φ ���������� PHP.
�� ������ �������� ��Ȧ���� ��� ��� ���������. ��ͦ��� �������ϧ
���Ц��æ� ¦������� ����� php ��� �������, ���������, Ц�������
oracle, ������צ�� ��� ����� ��� ���Ц��æ� ������� ���������.
������Φ�� �������æ� - � ���̦ SELF-CONTAINED-EXTENSIONS.

%description devel -l ru
����� php-devel ���� ����������� ������������� ������������ ����������
PHP. ����� �������� �������� ��� ���� ����������. ������ ���������
���������� ��������� ����� php ��� ����������, ��������, ���������
oracle, ���������� ���� ����� ��� �������������� ��������� ����������.
����������� - � ����� SELF-CONTAINED-EXTENSIONS.

%package bcmath
Summary:	bcmath extension module for PHP
Summary(pl):	Modu� bcmath dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description bcmath
This is a dynamic shared object (DSO) for PHP that will add bc style
precision math functions support.

%description bcmath -l pl
Modu� PHP umo�liwiaj�cy korzystanie z dok�adnych funkcji
matematycznych takich jak w programie bc.

%package bzip2
Summary:	Bzip2 extension module for PHP
Summary(pl):	Modu� bzip2 dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description bzip2
This is a dynamic shared object (DSO) for PHP that will add bzip2
compression support to PHP.

%description bzip2 -l pl
Modu� PHP umo�liwiaj�cy u�ywanie kompresji bzip2.

%package calendar
Summary:	Calendar extension module for PHP
Summary(pl):	Modu� funkcji kalendarza dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description calendar
This is a dynamic shared object (DSO) for PHP that will add calendar
support.

%description calendar -l pl
Modu� PHP dodaj�cy wsparcie dla kalendarza.

%package cpdf
Summary:	cpdf extension module for PHP
Summary(pl):	Modu� cpdf dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description cpdf
This is a dynamic shared object (DSO) for PHP that will add PDF
support through libcpdf library.

%description cpdf -l pl
Modu� PHP dodaj�cy obs�ug� plik�w PDF poprzez bibliotek� libcpdf.

%package ctype
Summary:	ctype extension module for PHP
Summary(pl):	Modu� ctype dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description ctype
This is a dynamic shared object (DSO) for PHP that will add ctype
support.

%description ctype -l pl
Modu� PHP umo�liwiaj�cy korzystanie z funkcji ctype.

%package curl
Summary:	curl extension module for PHP
Summary(pl):	Modu� curl dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description curl
This is a dynamic shared object (DSO) for PHP that will add curl
support.

%description curl -l pl
Modu� PHP umo�liwiaj�cy korzystanie z biblioteki curl.

%package dba
Summary:	DBA extension module for PHP
Summary(pl):	Modu� DBA dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description dba
This is a dynamic shared object (DSO) for PHP that will add flat-file
databases (DBA) support.

%description dba -l pl
Modu� dla PHP dodaj�cy obs�ug� dla baz danych opartych na plikach
(DBA).

%package dbase
Summary:	DBase extension module for PHP
Summary(pl):	Modu� DBase dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description dbase
This is a dynamic shared object (DSO) for PHP that will add DBase
support.

%description dbase -l pl
Modu� PHP ze wsparciem dla DBase.

%package dbx
Summary:	DBX extension module for PHP
Summary(pl):	Modu� DBX dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description dbx
This is a dynamic shared object (DSO) for PHP that will add DB
abstraction layer. DBX supports odbc, mysql, pgsql, mssql, fbsql and
more.

%description dbx -l pl
Modu� PHP dodaj�cy warstw� abstrakcji do obs�ugi baz danych. DBX
obs�uguje bazy odbc, mysql, pgsql, mssql, fbsql i inne.

%package dio
Summary:	Direct I/O extension module for PHP
Summary(pl):	Modu� Direct I/O dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description dio
This is a dynamic shared object (DSO) for PHP that will add direct
file I/O support.

%description dio -l pl
Modu� PHP dodaj�cy obs�ug� bezpo�rednich operacji I/O na plikach.

%package dom
Summary:	DOM extension module for PHP
Summary(pl):	Modu� DOM dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
# it has some compatibility functions
Provides:	php-domxml = %{epoch}:%{version}-%{release}
Obsoletes:	php-domxml <= 3:4.3.8-1

%description dom
This is a dynamic shared object (DSO) for PHP that will add new DOM
support.

%description dom -l pl
Modu� PHP dodaj�cy now� obs�ug� DOM.

%package exif
Summary:	exif extension module for PHP
Summary(pl):	Modu� exif dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description exif
This is a dynamic shared object (DSO) for PHP that will add EXIF tags
support in image files.

%description exif -l pl
Modu� PHP dodaj�cy obs�ug� znacznik�w EXIF w plikach obrazk�w.

%package fam
Summary:	FAM (File Alteration Monitor) module for PHP
Summary(pl):	Modu� FAM (File Alteration Monitor) dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description fam
This PHP module adds support for FAM (File Alteration Monitor).
FAM monitors files and directories, notifying interested applications
of changes.

%description fam -l pl
Modu� PHP dodaj�cy obs�ug� dla FAM (File Alteration Monitor).
FAM monitoruje pliki oraz katalogi, informuj�c zainteresowane aplikacje
o zmianach.

%package fdf
Summary:	FDF extension module for PHP
Summary(pl):	Modu� FDF dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description fdf
This PHP module adds support for PDF Forms through Adobe FDFTK
library.

%description fdf -l pl
Modu� PHP dodaj�cy obs�ug� formularzy PDF poprzez bibliotek� Adobe
FDFTK.

%package filepro
Summary:	filePro extension module for PHP
Summary(pl):	Modu� filePro dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description filepro
This is a dynamic shared object (DSO) for PHP that will add support
for read-only access to filePro databases.

%description filepro -l pl
Modu� PHP dodaj�cy mo�liwo�� dost�pu (tylko do odczytu) do baz danych
filePro.

%package ftp
Summary:	FTP extension module for PHP
Summary(pl):	Modu� FTP dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description ftp
This is a dynamic shared object (DSO) for PHP that will add FTP
support.

%description ftp -l pl
Modu� PHP dodaj�cy obs�ug� protoko�u FTP.

%package gd
Summary:	GD extension module for PHP
Summary(pl):	Modu� GD dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	gd >= 2.0.28-4
Provides:	%{name}-gd(gif) = %{epoch}:%{version}-%{release}

%description gd
This is a dynamic shared object (DSO) for PHP that will add GD
support, allowing you to create and manipulate images with PHP.

%description gd -l pl
Modu� PHP umo�liwiaj�cy korzystanie z biblioteki GD, pozwalaj�cej na
tworzenie i obr�bk� obrazk�w.

%package gettext
Summary:	gettext extension module for PHP
Summary(pl):	Modu� gettext dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description gettext
This is a dynamic shared object (DSO) for PHP that will add gettext
support.

%description gettext -l pl
Modu� PHP dodaj�cy obs�ug� lokalizacji przez gettext.

%package gmp
Summary:	gmp extension module for PHP
Summary(pl):	Modu� gmp dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description gmp
This is a dynamic shared object (DSO) for PHP that will add arbitrary
length number support with GNU MP library.

%description gmp -l pl
Modu� PHP umo�liwiaj�cy korzystanie z biblioteki gmp do oblicze� na
liczbach o dowolnej d�ugo�ci.

%package hwapi
Summary:	Hyperwave API extension module for PHP
Summary(pl):	Modu� API Hyperwave dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description hwapi
This is a dynamic shared object (DSO) for PHP that will add official
Hyperwave API support.

%description hwapi -l pl
Modu� PHP dodaj�cy obs�ug� Hyperwave.

%package iconv
Summary:	iconv extension module for PHP
Summary(pl):	Modu� iconv dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description iconv
This is a dynamic shared object (DSO) for PHP that will add iconv
support.

%description iconv -l pl
Modu� PHP dodaj�cy obs�ug� iconv.

%package imap
Summary:	IMAP extension module for PHP
Summary(pl):	Modu� IMAP dla PHP
Summary(pt_BR):	Um m�dulo para aplica��es PHP que usam IMAP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description imap
This is a dynamic shared object (DSO) for PHP that will add IMAP
support.

%description imap -l pl
Modu� PHP dodaj�cy obs�ug� skrzynek IMAP.

%description imap -l pt_BR
Um m�dulo para aplica��es PHP que usam IMAP.

%package interbase
Summary:	InterBase/Firebird database module for PHP
Summary(pl):	Modu� bazy danych InterBase/Firebird dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
%{?with_interbase_inst:Autoreq:	false}

%description interbase
This is a dynamic shared object (DSO) for PHP that will add InterBase
and Firebird database support.

%description interbase -l pl
Modu� PHP umo�liwiaj�cy dost�p do baz danych InterBase i Firebird.

%package ldap
Summary:	LDAP extension module for PHP
Summary(pl):	Modu� LDAP dla PHP
Summary(pt_BR):	Um m�dulo para aplica��es PHP que usam LDAP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description ldap
This is a dynamic shared object (DSO) for PHP that will add LDAP
support.

%description ldap -l pl
Modu� PHP dodaj�cy obs�ug� LDAP.

%description ldap -l pt_BR
Um m�dulo para aplica��es PHP que usam LDAP.

%package mbstring
Summary:	mbstring extension module for PHP
Summary(pl):	Modu� mbstring dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mbstring
This is a dynamic shared object (DSO) for PHP that will add multibyte
string support.

%description mbstring -l pl
Modu� PHP dodaj�cy obs�ug� ci�g�w znak�w wielobajtowych.

%package mcrypt
Summary:	mcrypt extension module for PHP
Summary(pl):	Modu� mcrypt dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mcrypt
This is a dynamic shared object (DSO) for PHP that will add mcrypt
support.

%description mcrypt -l pl
Modu� PHP dodaj�cy mo�liwo�� szyfrowania poprzez bibliotek� mcrypt.

%package mhash
Summary:	mhash extension module for PHP
Summary(pl):	Modu� mhash dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mhash
This is a dynamic shared object (DSO) for PHP that will add mhash
support.

%description mhash -l pl
Modu� PHP udost�pniaj�cy funkcje mieszaj�ce z biblioteki mhash.

%package mime_magic
Summary:	mime_magic extension module for PHP
Summary(pl):	Modu� mime_magic dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	/usr/share/file/magic.mime

%description mime_magic
This PHP module adds support for MIME type lookup via file magic
numbers using magic.mime database.

%description mime_magic -l pl
Modu� PHP dodaj�cy obs�ug� wyszukiwania typ�w MIME wed�ug magicznych
znacznik�w plik�w z u�yciem bazy danych magic.mime.

%package ming
Summary:	ming extension module for PHP
Summary(pl):	Modu� ming dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description ming
This is a dynamic shared object (DSO) for PHP that will add ming
(Flash - .swf files) support.

%description ming -l pl
Modu� PHP dodaj�cy obs�ug� plik�w Flash (.swf) poprzez bibliotek�
ming.

%package mnogosearch
Summary:	mnoGoSearch extension module for PHP
Summary(pl):	Modu� mnoGoSearch dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mnogosearch
This is a dynamic shared object (DSO) for PHP that will allow you to
access mnoGoSearch free search engine.

%description mnogosearch -l pl
Modu� PHP dodaj�cy pozwalaj�cy na dost�p do wolnodost�pnego silnika
wyszukiwarki mnoGoSearch.

%package msession
Summary:	msession extension module for PHP
Summary(pl):	Modu� msession dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description msession
This is a dynamic shared object (DSO) for PHP that will allow you to
use msession. msession is a high speed session daemon which can run
either locally or remotely. It is designed to provide consistent
session management for a PHP web farm.

%description msession -l pl
Modu� PHP dodaj�cy umo�liwiaj�cy korzystanie z demona msession. Jest
to demon szybkiej obs�ugi sesji, kt�ry mo�e dzia�a� lokalnie lub na
innej maszynie. S�u�y do zapewniania sp�jnej obs�ugi sesji dla farmy
serwer�w.

%package mssql
Summary:	MS SQL extension module for PHP
Summary(pl):	Modu� MS SQL dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mssql
This is a dynamic shared object (DSO) for PHP that will add MS SQL
databases support through FreeTDS library.

%description mssql -l pl
Modu� PHP dodaj�cy obs�ug� baz danych MS SQL poprzez bibliotek�
FreeTDS.

%package mysql
Summary:	MySQL database module for PHP
Summary(pl):	Modu� bazy danych MySQL dla PHP
Summary(pt_BR):	Um m�dulo para aplica��es PHP que usam bancos de dados MySQL
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description mysql
This is a dynamic shared object (DSO) for PHP that will add MySQL
database support.

%description mysql -l pl
Modu� PHP umo�liwiaj�cy dost�p do bazy danych MySQL.

%description mysql -l pt_BR
Um m�dulo para aplica��es PHP que usam bancos de dados MySQL.

%package mysqli
Summary:	MySQLi module for PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	mysql-libs >= 4.1.0

%description mysqli
This is a dynamic shared object (DSO) for PHP that will add MySQLi
(Improved MySQL) support. The difference between it and mysql module
is that it provides access to functionality of MySQL 4.1 and above.

%description mysqli -l pl
Modu� PHP umo�liwiaj�cy udoskonalony dost�p do bazy danych MySQL.
R�nic� mi�dzy nim a modu�em mysql jest dost�p do funkcjonalno�ci
MySQL 4.1 i wy�ej.

%package ncurses
Summary:	ncurses module for PHP
Summary(pl):	Modu� ncurses dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-cli = %{epoch}:%{version}-%{release}
Requires:	%{name}-cli = %{epoch}:%{version}-%{release}

%description ncurses
This PHP module adds support for ncurses functions (only for cli and
cgi SAPIs).

%description ncurses -l pl
Modu� PHP dodaj�cy obs�ug� funkcji ncurses (tylko do SAPI cli i cgi).

%package oci8
Summary:	Oracle 8 database module for PHP
Summary(pl):	Modu� bazy danych Oracle 8 dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Autoreq:	false

%description oci8
This is a dynamic shared object (DSO) for PHP that will add Oracle 7
and Oracle 8 database support through Oracle8 Call-Interface (OCI8).

%description oci8 -l pl
Modu� PHP umo�liwiaj�cy dost�p do bazy danych Oracle 7 i Oracle 8
poprzez interfejs Oracle8 Call-Interface (OCI8).

%package odbc
Summary:	ODBC extension module for PHP
Summary(pl):	Modu� ODBC dla PHP
Summary(pt_BR):	Um m�dulo para aplica��es PHP que usam bases de dados ODBC
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	unixODBC >= 2.1.1-3

%description odbc
This is a dynamic shared object (DSO) for PHP that will add ODBC
support.

%description odbc -l pl
Modu� PHP ze wsparciem dla ODBC.

%description odbc -l pt_BR
Um m�dulo para aplica��es PHP que usam ODBC.

%package openssl
Summary:	OpenSSL extension module for PHP
Summary(pl):	Modu� OpenSSL dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description openssl
This is a dynamic shared object (DSO) for PHP that will add OpenSSL
support.

Warning: this is an experimental module.

%description openssl -l pl
Modu� PHP umo�liwiaj�cy korzystanie z biblioteki OpenSSL.

Uwaga: to jest modu� eksperymentalny.

%package oracle
Summary:	Oracle 7 database module for PHP
Summary(pl):	Modu� bazy danych Oracle 7 dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Autoreq:	false

%description oracle
This is a dynamic shared object (DSO) for PHP that will add Oracle 7
database support.

%description oracle -l pl
Modu� PHP umo�liwiaj�cy dost�p do bazy danych Oracle 7.

%package pcntl
Summary:	Process Control extension module for PHP
Summary(pl):	Modu� Process Control dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-program = %{epoch}:%{version}-%{release}
Requires:	%{name}-program = %{epoch}:%{version}-%{release}

%description pcntl
This is a dynamic shared object (DSO) for PHP that will add process
spawning and control support. It supports functions like fork(),
waitpid(), signal() etc.

Warning: this is an experimental module. Also, don't use it in
webserver environment!

%description pcntl -l pl
Modu� PHP umo�liwiaj�cy tworzenie nowych proces�w i kontrol� nad nimi.
Obs�uguje funkcje takie jak fork(), waitpid(), signal() i podobne.

Uwaga: to jest modu� eksperymentalny. Ponadto nie jest przeznaczony do
u�ywania z serwerem WWW - nie pr�buj tego!

%package pcre
Summary:	PCRE extension module for PHP
Summary(pl):	Modu� PCRE dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description pcre
This is a dynamic shared object (DSO) for PHP that will add Perl
Compatible Regular Expression support.

%description pcre -l pl
Modu� PHP umo�liwiaj�cy korzystanie z perlowych wyra�e� regularnych
(Perl Compatible Regular Expressions)

%package pgsql
Summary:	PostgreSQL database module for PHP
Summary(pl):	Modu� bazy danych PostgreSQL dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description pgsql
This is a dynamic shared object (DSO) for PHP that will add PostgreSQL
database support.

%description pgsql -l pl
Modu� PHP umo�liwiaj�cy dost�p do bazy danych PostgreSQL.

%description pgsql -l pt_BR
Um m�dulo para aplica��es PHP que usam bancos de dados postgresql.

%package posix
Summary:	POSIX extension module for PHP
Summary(pl):	Modu� POSIX dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description posix
This is a dynamic shared object (DSO) for PHP that will add POSIX
functions support to PHP.

%description posix -l pl
Modu� PHP umo�liwiaj�cy korzystanie z funkcji POSIX.

%package pspell
Summary:	pspell extension module for PHP
Summary(pl):	Modu� pspell dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description pspell
This is a dynamic shared object (DSO) for PHP that will add pspell
support to PHP. It allows to check the spelling of a word and offer
suggestions.

%description pspell -l pl
Modu� PHP umo�liwiaj�cy korzystanie z pspella. Pozwala on na
sprawdzanie pisowni s�owa i sugerowanie poprawek.

%package readline
Summary:	readline extension module for PHP
Summary(pl):	Modu� readline dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-cli = %{epoch}:%{version}-%{release}
Requires:	%{name}-cli = %{epoch}:%{version}-%{release}

%description readline
This PHP module adds support for readline functions (only for cli and
cgi SAPIs).

%description readline -l pl
Modu� PHP dodaj�cy obs�ug� funkcji readline (tylko do SAPI cli i cgi).

%package recode
Summary:	recode extension module for PHP
Summary(pl):	Modu� recode dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	recode >= 3.5d-3

%description recode
This is a dynamic shared object (DSO) for PHP that will add recode
support.

%description recode -l pl
Modu� PHP dodaj�cy mo�liwo�� konwersji kodowania plik�w (poprzez
bibliotek� recode).

%package session
Summary:	session extension module for PHP
Summary(pl):	Modu� session dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description session
This is a dynamic shared object (DSO) for PHP that will add session
support.

%description session -l pl
Modu� PHP dodaj�cy obs�ug� sesji.

%package shmop
Summary:	Shared Memory Operations extension module for PHP
Summary(pl):	Modu� shmop dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description shmop
This is a dynamic shared object (DSO) for PHP that will add Shared
Memory Operations support.

Warning: this is an experimental module.

%description shmop -l pl
Modu� PHP umo�liwiaj�cy korzystanie z pami�ci dzielonej.

Uwaga: to jest modu� eksperymentalny.

%package snmp
Summary:	SNMP extension module for PHP
Summary(pl):	Modu� SNMP dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-sockets = %{epoch}:%{version}-%{release}

%description snmp
This is a dynamic shared object (DSO) for PHP that will add SNMP
support.

%description snmp -l pl
Modu� PHP dodaj�cy obs�ug� SNMP.

%package soap
Summary:	soap extension module for PHP
Summary(pl):	Modu� soap dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description soap
This is a dynamic shared object (DSO) for PHP that will add SOAP/WSDL
support.

%description soap -l pl
Modu� PHP dodaj�cy obs�ug� SOAP/WSDL.

%package sockets
Summary:	sockets extension module for PHP
Summary(pl):	Modu� socket dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description sockets
This is a dynamic shared object (DSO) for PHP that will add sockets
support.

Warning: this is an experimental module.

%description sockets -l pl
Modu� PHP dodaj�cy obs�ug� gniazdek.

Uwaga: to jest modu� eksperymentalny.

%package sqlite
Summary:	SQLite extension module for PHP
Summary(pl):	Modu� SQLite dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description sqlite
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database server.
SQLite is the server. The SQLite library reads and writes directly to
and from the database files on disk.

%description sqlite -l pl
SQLite jest napisan� w C bibliotek� implementuj�c� osadzalny silnik
bazodanowy SQL. Program linkuj�cy si� z bibliotek� SQLite mo�e mie�
dost�p do bazy SQL bez potrzeby uruchamiania dodatkowego procesu RDBMS.

SQLite to nie klient baz danych - biblioteka nie ��czy si� z serwerami
baz danych. SQLite sam jest serwerem. Biblioteka SQLite czyta i zapisuje
dane bezpo�rednio z/do plik�w baz danych znajduj�cych si� na dysku.

%package sybase
Summary:	Sybase DB extension module for PHP
Summary(pl):	Modu� Sybase DB dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	php-sybase-ct

%description sybase
This is a dynamic shared object (DSO) for PHP that will add Sybase and
MS SQL databases support through SYBDB library. Currently Sybase module
is not maintained. Using Sybase-CT module is recommended instead.

%description sybase -l pl
Modu� PHP dodaj�cy obs�ug� baz danych Sybase oraz MS SQL poprzez
bibliotek� SYBDB. W chwili obecnej modu� Sybase nie jest wspierany.
Zaleca si� u�ywanie modu�u Sybase-CT.

%package sybase-ct
Summary:	Sybase-CT extension module for PHP
Summary(pl):	Modu� Sybase-CT dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	php-sybase

%description sybase-ct
This is a dynamic shared object (DSO) for PHP that will add Sybase and
MS SQL databases support through CT-lib.

%description sybase-ct -l pl
Modu� PHP dodaj�cy obs�ug� baz danych Sybase oraz MS SQL poprzez
CT-lib.

%package sysvmsg
Summary:	SysV msg extension module for PHP
Summary(pl):	Modu� SysV msg dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description sysvmsg
This is a dynamic shared object (DSO) for PHP that will add SysV
message queues support.

%description sysvmsg -l pl
Modu� PHP umo�liwiaj�cy korzystanie z kolejek komunikat�w SysV.

%package sysvsem
Summary:	SysV sem extension module for PHP
Summary(pl):	Modu� SysV sem dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description sysvsem
This is a dynamic shared object (DSO) for PHP that will add SysV
semaphores support.

%description sysvsem -l pl
Modu� PHP umo�liwiaj�cy korzystanie z semafor�w SysV.

%package sysvshm
Summary:	SysV shm extension module for PHP
Summary(pl):	Modu� SysV shm dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description sysvshm
This is a dynamic shared object (DSO) for PHP that will add SysV
Shared Memory support.

%description sysvshm -l pl
Modu� PHP umo�liwiaj�cy korzystanie z pami�ci dzielonej SysV.

%package tidy
Summary:	Tidy extension module for PHP
Summary(pl):	Modu� Tidy dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description tidy
This is a dynamic shared object (DSO) for PHP that will add Tidy
support.

%description tidy -l pl
Modu� PHP umo�liwiaj�cy korzystanie z tidy.

%package wddx
Summary:	wddx extension module for PHP
Summary(pl):	Modu� wddx dla PHP
Group:		Libraries
PreReq:		%{name}-session = %{epoch}:%{version}-%{release}
PreReq:		%{name}-xml = %{epoch}:%{version}-%{release}
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description wddx
This is a dynamic shared object (DSO) for PHP that will add wddx
support.

%description wddx -l pl
Modu� PHP umo�liwiaj�cy korzystanie z wddx.

%package xml
Summary:	XML extension module for PHP
Summary(pl):	Modu� XML dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description xml
This is a dynamic shared object (DSO) for PHP that will add XML
support. This extension lets you create XML parsers and then define
handlers for different XML events.

%description xml -l pl
Modu� PHP umo�liwiaj�cy parsowanie plik�w XML i obs�ug� zdarze�
zwi�zanych z tymi plikami. Pozwala on tworzy� analizatory XML-a i
nast�pnie definiowa� procedury obs�ugi dla r�nych zdarze� XML.

%package xmlrpc
Summary:	xmlrpc extension module for PHP
Summary(pl):	Modu� xmlrpc dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description xmlrpc
This is a dynamic shared object (DSO) for PHP that will add XMLRPC
support.

Warning: this is an experimental module.

%description xmlrpc -l pl
Modu� PHP dodaj�cy obs�ug� XMLRPC.

Uwaga: to jest modu� eksperymentalny.

%package xsl
Summary:	xsl extension module for PHP
Summary(pl):	Modu� xsl dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	libxslt >= 1.0.18
# Maybe it would be nice to add it here?
#Provides:	php-xslt
# actually not true, functionality is similar, but API differs
Obsoletes:	php-xslt <= 3:4.3.8-1

%description xsl
This is a dynamic shared object (DSO) for PHP that will add new XSL
support (using libxslt).

%description xsl -l pl
Modu� PHP dodaj�cy now� obs�ug� XSLT (przy u�yciu libxslt).

%package yp
Summary:	NIS (yp) extension module for PHP
Summary(pl):	Modu� NIS (yp) dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description yp
This is a dynamic shared object (DSO) for PHP that will add NIS
(Yellow Pages) support.

%description yp -l pl
Modu� PHP dodaj�cy wsparcie dla NIS (Yellow Pages).

%package zlib
Summary:	Zlib extension module for PHP
Summary(pl):	Modu� zlib dla PHP
Group:		Libraries
Requires(post,preun):	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description zlib
This is a dynamic shared object (DSO) for PHP that will add zlib
compression support to PHP.

%description zlib -l pl
Modu� PHP umo�liwiaj�cy u�ywanie kompresji zlib.

%prep
%setup -q
# this patch is broken by design, breaks --enable-versioning for example
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
cp php.ini-dist php.ini
%patch10 -p1
# for ac2.53b/am1.6b - AC_LANG_CXX has AM_CONDITIONAL, so cannot be invoked
# conditionally...
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch28 -p1
%if "%{_lib}" == "lib64"
%patch22 -p1
%endif
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch29 -p1

%{?with_hardened:zcat %{SOURCE9} | patch -p1}

# conflict seems to be resolved by recode patches
rm -f ext/recode/config9.m4

# fix lib path in phpize
cd scripts/
sed -i -e 's,lib/php,%{_lib}/php,' phpize.in
cd ..

# new apr
sed -i -e 's#apr-config#apr-1-config#g' sapi/apache*/*.m4

%build
%if %{_apache2}
CFLAGS="%{rpmcflags} -DEAPI=1 -I/usr/X11R6/include `%{_bindir}/apr-1-config --includes` `%{_bindir}/apu-1-config --includes`"
%else
CFLAGS="%{rpmcflags} -DEAPI=1 -I/usr/X11R6/include"
%endif
EXTENSION_DIR="%{extensionsdir}"; export EXTENSION_DIR
./buildconf --force
%{__libtoolize}
%{__aclocal}
%{__autoconf}
PROG_SENDMAIL="/usr/lib/sendmail"; export PROG_SENDMAIL
for i in fcgi cgi cli apxs ; do
%configure \
	`[ $i = cgi ] && echo --enable-discard-path` \
	`[ $i = cli ] && echo --disable-cgi` \
	`[ $i = fcgi ] && echo --enable-fastcgi --with-fastcgi=/usr` \
%if %{_apache2}
	`[ $i = apxs ] && echo --with-apxs2=%{apxs}` \
	--enable-maintainer-zts \
%else
	`[ $i = apxs ] && echo --with-apxs=%{apxs}` \
%endif
	--with-config-file-path=%{_sysconfdir} \
	--with-exec-dir=%{_bindir} \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--enable-memory-limit \
	--enable-bcmath=shared \
	--enable-calendar=shared \
	--enable-ctype=shared \
	--enable-dba=shared \
	--enable-dbx=shared \
	--enable-dio=shared \
	--enable-dom=shared \
	--enable-exif=shared \
	--enable-filepro=shared \
	--enable-ftp=shared \
	--enable-gd-native-ttf \
	--enable-gd-jus-conf \
	--enable-magic-quotes \
	--enable-mbstring=shared,all \
	--enable-mbregex \
	--enable-pcntl=shared \
	--enable-posix=shared \
	--enable-session \
	--enable-shared \
	--enable-shmop=shared \
	--enable-sysvmsg=shared \
	--enable-sysvsem=shared \
	--enable-sysvshm=shared \
	--enable-track-vars \
	--enable-trans-sid \
	--enable-safe-mode \
	--enable-soap=shared \
	--enable-sockets=shared \
	--enable-ucd-snmp-hack \
	%{?with_wddx:--enable-wddx=shared} \
	--enable-xml=shared \
	--enable-yp=shared \
	--with-bz2=shared \
	%{?with_cpdf:--with-cpdflib=shared} \
	%{!?with_curl:--without-curl}%{?with_curl:--with-curl=shared} \
	%{?with_db3:--with-db3}%{!?with_db3:--with-db4} \
	--with-dbase=shared \
%if %{with xmlrpc}
	--with-expat-dir=shared,/usr \
%else
	--without-expat-dir \
%endif
	%{?with_fdf:--with-fdftk=shared} \
	--with-iconv=shared \
	%{?with_fam:--with-fam=shared} \
	--with-filepro=shared \
	--with-freetype-dir=shared \
	--with-gettext=shared \
	--with-gd=shared,/usr \
	--with-gdbm \
	--with-gmp=shared \
	%{?with_hwapi:--with-hwapi=shared} \
	%{?with_imap:--with-imap=shared --with-imap-ssl} \
	%{?with_interbase:--with-interbase=shared%{!?with_interbase_inst:,/usr}} \
	--with-jpeg-dir=/usr \
	%{?with_ldap:--with-ldap=shared} \
	--with-mcrypt=shared \
	%{?with_mhash:--with-mhash=shared} \
	--with-mime-magic=shared,/usr/share/file/magic.mime \
	%{?with_ming:--with-ming=shared} \
	%{?with_mm:--with-mm} \
	%{!?with_mnogosearch:--without-mnogosearch}%{?with_mnogosearch:--with-mnogosearch=shared,/usr} \
	%{?with_msession:--with-msession=shared}%{!?with_msession:--without-msession} \
	%{?with_mssql:--with-mssql=shared} \
	--with-mysql=shared,/usr \
	--with-mysql-sock=/var/lib/mysql/mysql.sock \
	%{?with_mysqli:--with-mysqli=shared} \
	--with-ncurses=shared \
	%{?with_oci8:--with-oci8=shared} \
	%{?with_openssl:--with-openssl=shared} \
	%{?with_oracle:--with-oracle=shared} \
	%{!?with_pcre:--without-pcre-regex}%{?with_pcre:--with-pcre-regex=shared} \
	--with-pear=%{php_pear_dir} \
	%{!?with_pgsql:--without-pgsql}%{?with_pgsql:--with-pgsql=shared,/usr} \
	--with-png-dir=/usr \
	%{?with_pspell:--with-pspell=shared} \
	--with-readline=shared \
	%{?with_recode:--with-recode=shared} \
	--with-regex=php \
	--without-sablot-js \
	%{?with_snmp:--with-snmp=shared} \
	%{?with_sybase:--with-sybase=shared,/usr} \
	%{?with_sybase_ct:--with-sybase-ct=shared,/usr} \
	%{?with_sqlite:--with-sqlite=shared,/usr} \
	--with-t1lib=shared \
	%{?with_tidy:--with-tidy=shared} \
	--with-tiff-dir=/usr \
	%{?with_odbc:--with-unixODBC=shared} \
	%{!?with_xmlrpc:--without-xmlrpc}%{?with_xmlrpc:--with-xmlrpc=shared,/usr} \
	--with-xsl=shared \
	--with-zlib=shared \
	--with-zlib-dir=shared,/usr

cp -f Makefile Makefile.$i
# left for debugging purposes
cp -f main/php_config.h php_config.h.$i
done

# for now session_mm doesn't work with shared session module...
# --enable-session=shared
# %{!?with_mm:--with-mm=shared,no}%{?with_mm:--with-mm=shared}

%{__make}

# fix install paths, avoid evil rpaths
%{__perl} -pi -e "s|^libdir=.*|libdir='%{_libdir}'|" libphp_common.la
%{__perl} -pi -e "s|^libdir=.*|libdir='%{apachelib}'|" libphp5.la
%{__perl} -pi -e 's|^(relink_command=.* -rpath )[^ ]*/libs |$1%{apachelib} |' libphp5.la

# for fcgi: -DDISCARD_PATH=0 -DENABLE_PATHINFO_CHECK=1 -DFORCE_CGI_REDIRECT=0
# -DHAVE_FILENO_PROTO=1 -DHAVE_FPOS=1 -DHAVE_LIBNSL=1(die) -DHAVE_SYS_PARAM_H=1
# -DPHP_FASTCGI=1 -DPHP_FCGI_STATIC=1 -DPHP_WRITE_STDOUT=1

%{__make} sapi/cgi/php -f Makefile.fcgi \
	CFLAGS_CLEAN="%{rpmcflags} -DDISCARD_PATH=0 -DENABLE_PATHINFO_CHECK=1 -DFORCE_CGI_REDIRECT=0 -DHAVE_FILENO_PROTO=1 -DHAVE_FPOS=1 -DHAVE_LIBNSL=1 -DHAVE_SYS_PARAM_H=1 -DPHP_FASTCGI=1 -DPHP_FCGI_STATIC=1 -DPHP_WRITE_STDOUT=1"
cp -r sapi/cgi sapi/fcgi
rm -rf sapi/cgi/.libs sapi/cgi/*.lo

# notes:
# -DENABLE_CHROOT_FUNC=1 (cgi,fcgi) is used in ext/standard/dir.c (libphp_common)
# -DPHP_WRITE_STDOUT is used also for cli, but not set by its config.m4

%{__make} sapi/cgi/php -f Makefile.cgi \
	CFLAGS_CLEAN="%{rpmcflags} -DDISCARD_PATH=1 -DENABLE_PATHINFO_CHECK=1 -DFORCE_CGI_REDIRECT=0 -DPHP_WRITE_STDOUT=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/php,%{apachelib},%{_sysconfdir}/{apache,cgi}} \
	$RPM_BUILD_ROOT%{httpdir}/icons \
	$RPM_BUILD_ROOT{%{_sbindir},%{_bindir}} \
	$RPM_BUILD_ROOT/var/run/php \
%if %{_apache2}
	$RPM_BUILD_ROOT/etc/httpd/httpd.conf
%else
	$RPM_BUILD_ROOT/etc/apache/apache.conf
%endif

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	INSTALL_IT="\$(LIBTOOL) --mode=install install libphp_common.la $RPM_BUILD_ROOT%{_libdir} ; \$(LIBTOOL) --mode=install install libphp5.la $RPM_BUILD_ROOT%{apachelib}; \$(LIBTOOL) --mode=install install sapi/cgi/php $RPM_BUILD_ROOT%{_bindir}/php.cgi ; \$(LIBTOOL) --mode=install install sapi/fcgi/php $RPM_BUILD_ROOT%{_bindir}/php.fcgi" \
	INSTALL_CLI="\$(LIBTOOL) --mode=install install sapi/cli/php $RPM_BUILD_ROOT%{_bindir}/php.cli"

# TODO:
# Why make install doesn't install libphp5.so ?
install libs/libphp5.so $RPM_BUILD_ROOT%{apachelib}

ln -sf php.cli $RPM_BUILD_ROOT%{_bindir}/php

install php.ini	$RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} php.gif $RPM_BUILD_ROOT%{httpdir}/icons
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}
%if %{_apache2}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/70_mod_php.conf
%endif

install %{SOURCE1} .

cp -f Zend/LICENSE{,.Zend}

rm -f $RPM_BUILD_ROOT%{apachelib}/libphp5.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if ! %{_apache2}
%{__perl} -pi -e 's|^#AddType application/x-httpd-php \.php|AddType application/x-httpd-php .php|' \
	/etc/apache/apache.conf
%{apxs} -e -a -n php5 %{_pkglibdir}/libphp5.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi
%else
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi
%endif

%if %{_apache2}
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi
%else
%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n php5 %{_pkglibdir}/libphp5.so 1>&2
	%{__perl} -pi -e \
		's|^AddType application/x-httpd-php \.php|#AddType application/x-httpd-php .php|' \
		/etc/apache/apache.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
%endif

%post	common -p /sbin/ldconfig
%postun	common -p /sbin/ldconfig

%post bcmath
%{_sbindir}/php-module-install install bcmath %{_sysconfdir}/php.ini

%preun bcmath
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove bcmath %{_sysconfdir}/php.ini
fi

%post bzip2
%{_sbindir}/php-module-install install bz2 %{_sysconfdir}/php.ini

%preun bzip2
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove bz2 %{_sysconfdir}/php.ini
fi

%post calendar
%{_sbindir}/php-module-install install calendar %{_sysconfdir}/php.ini

%preun calendar
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove calendar %{_sysconfdir}/php.ini
fi

%post cpdf
%{_sbindir}/php-module-install install cpdf %{_sysconfdir}/php.ini

%preun cpdf
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove cpdf %{_sysconfdir}/php.ini
fi

%post ctype
%{_sbindir}/php-module-install install ctype %{_sysconfdir}/php.ini

%preun ctype
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove ctype %{_sysconfdir}/php.ini
fi

%post curl
%{_sbindir}/php-module-install install curl %{_sysconfdir}/php.ini

%preun curl
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove curl %{_sysconfdir}/php.ini
fi

%post dba
%{_sbindir}/php-module-install install dba %{_sysconfdir}/php.ini

%preun dba
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove dba %{_sysconfdir}/php.ini
fi

%post dbase
%{_sbindir}/php-module-install install dbase %{_sysconfdir}/php.ini

%preun dbase
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove dbase %{_sysconfdir}/php.ini
fi

%post dbx
%{_sbindir}/php-module-install install dbx %{_sysconfdir}/php.ini

%preun dbx
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove dbx %{_sysconfdir}/php.ini
fi

%post dio
%{_sbindir}/php-module-install install dio %{_sysconfdir}/php.ini

%preun dio
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove dio %{_sysconfdir}/php.ini
fi

%post dom
%{_sbindir}/php-module-install install dom %{_sysconfdir}/php.ini

%preun dom
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove dom %{_sysconfdir}/php.ini
fi

%post exif
%{_sbindir}/php-module-install install exif %{_sysconfdir}/php.ini

%preun exif
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove exif %{_sysconfdir}/php.ini
fi

%post fam
%{_sbindir}/php-module-install install fam %{_sysconfdir}/php.ini

%preun fam
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove fam %{_sysconfdir}/php.ini
fi

%post fdf
%{_sbindir}/php-module-install install fdf %{_sysconfdir}/php.ini

%preun fdf
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove fdf %{_sysconfdir}/php.ini
fi

%post filepro
%{_sbindir}/php-module-install install filepro %{_sysconfdir}/php.ini

%preun filepro
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove filepro %{_sysconfdir}/php.ini
fi

%post ftp
%{_sbindir}/php-module-install install ftp %{_sysconfdir}/php.ini

%preun ftp
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove ftp %{_sysconfdir}/php.ini
fi

%post gd
%{_sbindir}/php-module-install install gd %{_sysconfdir}/php.ini

%preun gd
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove gd %{_sysconfdir}/php.ini
fi

%post gettext
%{_sbindir}/php-module-install install gettext %{_sysconfdir}/php.ini

%preun gettext
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove gettext %{_sysconfdir}/php.ini
fi

%post gmp
%{_sbindir}/php-module-install install gmp %{_sysconfdir}/php.ini

%preun gmp
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove gmp %{_sysconfdir}/php.ini
fi

%post hwapi
%{_sbindir}/php-module-install install hwapi %{_sysconfdir}/php.ini

%preun hwapi
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove hwapi %{_sysconfdir}/php.ini
fi

%post iconv
%{_sbindir}/php-module-install install iconv %{_sysconfdir}/php.ini

%preun iconv
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove iconv %{_sysconfdir}/php.ini
fi

%post imap
%{_sbindir}/php-module-install install imap %{_sysconfdir}/php.ini

%preun imap
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove imap %{_sysconfdir}/php.ini
fi

%post interbase
%{_sbindir}/php-module-install install interbase %{_sysconfdir}/php.ini

%preun interbase
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove interbase %{_sysconfdir}/php.ini
fi

%post ldap
%{_sbindir}/php-module-install install ldap %{_sysconfdir}/php.ini

%preun ldap
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove ldap %{_sysconfdir}/php.ini
fi

%post mbstring
%{_sbindir}/php-module-install install mbstring %{_sysconfdir}/php.ini

%preun mbstring
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mbstring %{_sysconfdir}/php.ini
fi

%post mcrypt
%{_sbindir}/php-module-install install mcrypt %{_sysconfdir}/php.ini

%preun mcrypt
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mcrypt %{_sysconfdir}/php.ini
fi

%post mhash
%{_sbindir}/php-module-install install mhash %{_sysconfdir}/php.ini

%preun mhash
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mhash %{_sysconfdir}/php.ini
fi

%post mime_magic
%{_sbindir}/php-module-install install mime_magic %{_sysconfdir}/php.ini

%preun mime_magic
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mime_magic %{_sysconfdir}/php.ini
fi

%post ming
%{_sbindir}/php-module-install install ming %{_sysconfdir}/php.ini

%preun ming
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove ming %{_sysconfdir}/php.ini
fi

%post mnogosearch
%{_sbindir}/php-module-install install mnogosearch %{_sysconfdir}/php.ini

%preun mnogosearch
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mnogosearch %{_sysconfdir}/php.ini
fi

%post msession
%{_sbindir}/php-module-install install msession %{_sysconfdir}/php.ini

%preun msession
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove msession %{_sysconfdir}/php.ini
fi

%post mssql
%{_sbindir}/php-module-install install mssql %{_sysconfdir}/php.ini

%preun mssql
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mssql %{_sysconfdir}/php.ini
fi

%post mysql
%{_sbindir}/php-module-install install mysql %{_sysconfdir}/php.ini

%preun mysql
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mysql %{_sysconfdir}/php.ini
fi

%post mysqli
%{_sbindir}/php-module-install install mysqli %{_sysconfdir}/php.ini

%preun mysqli
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mysqli %{_sysconfdir}/php.ini
fi

%post ncurses
if [ -f %{_sysconfdir}/php-cgi.ini ]; then
%{_sbindir}/php-module-install install ncurses %{_sysconfdir}/php-cgi.ini
fi
if [ -f %{_sysconfdir}/php-cli.ini ]; then
%{_sbindir}/php-module-install install ncurses %{_sysconfdir}/php-cli.ini
fi

%preun ncurses
if [ "$1" = "0" ]; then
	if [ -f %{_sysconfdir}/php-cgi.ini ]; then
	%{_sbindir}/php-module-install remove ncurses %{_sysconfdir}/php-cgi.ini
	fi
	if [ -f %{_sysconfdir}/php-cli.ini ]; then
	%{_sbindir}/php-module-install remove ncurses %{_sysconfdir}/php-cli.ini
	fi
fi

%post oci8
%{_sbindir}/php-module-install install oci8 %{_sysconfdir}/php.ini

%preun oci8
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove oci8 %{_sysconfdir}/php.ini
fi

%post odbc
%{_sbindir}/php-module-install install odbc %{_sysconfdir}/php.ini

%preun odbc
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove odbc %{_sysconfdir}/php.ini
fi

%post openssl
%{_sbindir}/php-module-install install openssl %{_sysconfdir}/php.ini

%preun openssl
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove openssl %{_sysconfdir}/php.ini
fi

%post oracle
%{_sbindir}/php-module-install install oracle %{_sysconfdir}/php.ini

%preun oracle
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove oracle %{_sysconfdir}/php.ini
fi

%post pcntl
if [ -f %{_sysconfdir}/php-cgi.ini ]; then
%{_sbindir}/php-module-install install pcntl %{_sysconfdir}/php-cgi.ini
fi
if [ -f %{_sysconfdir}/php-cli.ini ]; then
%{_sbindir}/php-module-install install pcntl %{_sysconfdir}/php-cli.ini
fi

%preun pcntl
if [ "$1" = "0" ]; then
	if [ -f %{_sysconfdir}/php-cgi.ini ]; then
	%{_sbindir}/php-module-install remove pcntl %{_sysconfdir}/php-cgi.ini
	fi
	if [ -f %{_sysconfdir}/php-cli.ini ]; then
	%{_sbindir}/php-module-install remove pcntl %{_sysconfdir}/php-cli.ini
	fi
fi

%post pcre
%{_sbindir}/php-module-install install pcre %{_sysconfdir}/php.ini

%preun pcre
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove pcre %{_sysconfdir}/php.ini
fi

%post pgsql
%{_sbindir}/php-module-install install pgsql %{_sysconfdir}/php.ini

%preun pgsql
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove pgsql %{_sysconfdir}/php.ini
fi

%post posix
%{_sbindir}/php-module-install install posix %{_sysconfdir}/php.ini

%preun posix
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove posix %{_sysconfdir}/php.ini
fi

%post pspell
%{_sbindir}/php-module-install install pspell %{_sysconfdir}/php.ini

%preun pspell
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove pspell %{_sysconfdir}/php.ini
fi

%post readline
if [ -f %{_sysconfdir}/php-cgi.ini ]; then
%{_sbindir}/php-module-install install readline %{_sysconfdir}/php-cgi.ini
fi
if [ -f %{_sysconfdir}/php-cli.ini ]; then
%{_sbindir}/php-module-install install readline %{_sysconfdir}/php-cli.ini
fi

%preun readline
if [ "$1" = "0" ]; then
	if [ -f %{_sysconfdir}/php-cgi.ini ]; then
	%{_sbindir}/php-module-install remove readline %{_sysconfdir}/php-cgi.ini
	fi
	if [ -f %{_sysconfdir}/php-cli.ini ]; then
	%{_sbindir}/php-module-install remove readline %{_sysconfdir}/php-cli.ini
	fi
fi

%post recode
%{_sbindir}/php-module-install install recode %{_sysconfdir}/php.ini

%preun recode
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove recode %{_sysconfdir}/php.ini
fi

%post session
%{_sbindir}/php-module-install install session %{_sysconfdir}/php.ini

%preun session
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove session %{_sysconfdir}/php.ini
fi

%post shmop
%{_sbindir}/php-module-install install shmop %{_sysconfdir}/php.ini

%preun shmop
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove shmop %{_sysconfdir}/php.ini
fi

%post snmp
%{_sbindir}/php-module-install install snmp %{_sysconfdir}/php.ini

%preun snmp
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove snmp %{_sysconfdir}/php.ini
fi

%post soap
%{_sbindir}/php-module-install install soap %{_sysconfdir}/php.ini

%preun soap
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove soap %{_sysconfdir}/php.ini
fi

%post sockets
%{_sbindir}/php-module-install install sockets %{_sysconfdir}/php.ini

%preun sockets
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sockets %{_sysconfdir}/php.ini
fi

%post sqlite
%{_sbindir}/php-module-install install sqlite %{_sysconfdir}/php.ini

%preun sqlite
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sqlite %{_sysconfdir}/php.ini
fi

%post sybase
%{_sbindir}/php-module-install install sybase %{_sysconfdir}/php.ini

%preun sybase
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sybase %{_sysconfdir}/php.ini
fi

%post sybase-ct
%{_sbindir}/php-module-install install sybase_ct %{_sysconfdir}/php.ini

%preun sybase-ct
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sybase_ct %{_sysconfdir}/php.ini
fi

%post sysvmsg
%{_sbindir}/php-module-install install sysvmsg %{_sysconfdir}/php.ini

%preun sysvmsg
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sysvmsg %{_sysconfdir}/php.ini
fi

%post sysvsem
%{_sbindir}/php-module-install install sysvsem %{_sysconfdir}/php.ini

%preun sysvsem
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sysvsem %{_sysconfdir}/php.ini
fi

%post sysvshm
%{_sbindir}/php-module-install install sysvshm %{_sysconfdir}/php.ini

%preun sysvshm
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove sysvshm %{_sysconfdir}/php.ini
fi

%post wddx
%{_sbindir}/php-module-install install wddx %{_sysconfdir}/php.ini

%preun wddx
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove wddx %{_sysconfdir}/php.ini
fi

%post xml
%{_sbindir}/php-module-install install xml %{_sysconfdir}/php.ini

%preun xml
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove xml %{_sysconfdir}/php.ini
fi

%post xmlrpc
%{_sbindir}/php-module-install install xmlrpc %{_sysconfdir}/php.ini

%preun xmlrpc
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove xmlrpc %{_sysconfdir}/php.ini
fi

%post xsl
%{_sbindir}/php-module-install install xsl %{_sysconfdir}/php.ini

%preun xsl
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove xsl %{_sysconfdir}/php.ini
fi

%post yp
%{_sbindir}/php-module-install install yp %{_sysconfdir}/php.ini

%preun yp
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove yp %{_sysconfdir}/php.ini
fi

%post zlib
%{_sbindir}/php-module-install install zlib %{_sysconfdir}/php.ini

%preun zlib
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove zlib %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%if %{_apache2}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/httpd/httpd.conf/*_mod_php.conf
%endif
%attr(755,root,root) %{apachelib}/libphp5.so
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php-apache.ini

%files fcgi
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php.fcgi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php-cgi-fcgi.ini

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php.cgi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php-cgi.ini

%files cli
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php.cli
%attr(755,root,root) %{_bindir}/php
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php-cli.ini
%{_mandir}/man1/php.1*

%files common
%defattr(644,root,root,755)
%doc php.ini-*
%doc CODING_STANDARDS CREDITS Zend/ZEND_CHANGES
%doc LICENSE Zend/LICENSE.Zend EXTENSIONS NEWS TODO*
%doc README.EXT_SKEL README.SELF-CONTAINED-EXTENSIONS

%dir %{_sysconfdir}
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php.ini
%attr(770,root,http) %dir %verify(not group mode) /var/run/php
%{httpdir}/icons/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libphp_common-*.so
%dir %{extensionsdir}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/phpextdist
%attr(755,root,root) %{_bindir}/phpize
%attr(755,root,root) %{_bindir}/php-config
%attr(755,root,root) %{_libdir}/libphp_common.so
%{_libdir}/libphp_common.la
%{_includedir}/php
%{_libdir}/php/build

%files bcmath
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/bcmath.so

%files bzip2
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/bz2.so

%files calendar
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/calendar.so

%if %{with cpdf}
%files cpdf
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/cpdf.so
%endif

%files ctype
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/ctype.so

%if %{with curl}
%files curl
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/curl.so
%endif

%files dba
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/dba.so

%files dbase
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/dbase.so

%files dbx
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/dbx.so

%files dio
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/dio.so

%files dom
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/dom.so

%if %{with fam}
%files fam
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/fam.so
%endif

%if %{with fdf}
%files fdf
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/fdf.so
%endif

%files exif
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/exif.so

%files filepro
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/filepro.so

%files ftp
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/ftp.so

%files gd
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/gd.so

%files gettext
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/gettext.so

%files gmp
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/gmp.so

%if %{with hwapi}
%files hwapi
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/hwapi.so
%endif

%files iconv
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/iconv.so

%if %{with imap}
%files imap
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/imap.so
%endif

%if %{with interbase}
%files interbase
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/interbase.so
%endif

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/ldap.so
%endif

%files mbstring
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mbstring.so

%files mcrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mcrypt.so

%if %{with mhash}
%files mhash
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mhash.so
%endif

%files mime_magic
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mime_magic.so

%if %{with ming}
%files ming
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/ming.so
%endif

%if %{with mnogosearch}
%files mnogosearch
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mnogosearch.so
%endif

%if %{with msession}
%files msession
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/msession.so
%endif

%if %{with mssql}
%files mssql
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mssql.so
%endif

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mysql.so

%if %{with mysqli}
%files mysqli
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/mysqli.so
%endif

%files ncurses
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/ncurses.so

%if %{with oci8}
%files oci8
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/oci8.so
%endif

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/odbc.so
%endif

%if %{with openssl}
%files openssl
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/openssl.so
%endif

%if %{with oracle}
%files oracle
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/oracle.so
%endif

%files pcntl
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/pcntl.so

%if %{with pcre}
%files pcre
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/pcre.so
%endif

%if %{with pgsql}
%files pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/pgsql.so
%endif

%files posix
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/posix.so

%if %{with pspell}
%files pspell
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/pspell.so
%endif

%files readline
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/readline.so

%if %{with recode}
%files recode
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/recode.so
%endif

# session_mm doesn't work with shared session
#%files session
#%defattr(644,root,root,755)
#%attr(755,root,root) %{extensionsdir}/session.so

%files shmop
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/shmop.so

%if %{with snmp}
%files snmp
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/snmp.so
%endif

%files soap
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/soap.so

%files sockets
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sockets.so

%if %{with sqlite}
%files sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sqlite.so
%endif

%if %{with sybase}
%files sybase
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sybase.so
%endif

%if %{with sybase_ct}
%files sybase-ct
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sybase_ct.so
%endif

%files sysvmsg
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sysvmsg.so

%files sysvsem
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sysvsem.so

%files sysvshm
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/sysvshm.so

%if %{with tidy}
%files tidy
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/tidy.so
%endif

%if %{with wddx}
%files wddx
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/wddx.so
%endif

%files xml
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/xml.so

%if %{with xmlrpc}
%files xmlrpc
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/xmlrpc.so
%endif

%files xsl
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/xsl.so

%files yp
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/yp.so

%files zlib
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/zlib.so
