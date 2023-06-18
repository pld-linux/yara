# TODO
# - http://yara.readthedocs.org/en/latest/gettingstarted.html#compiling-and-installing-yara

# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	crypto		# OpenSSL crypto support (in PE module)

Summary:	The pattern matching swiss knife for malware researchers (and everyone else)
Summary(pl.UTF-8):	Narzędzie do dopasowywania wzorców dla wyszukujących złośliwe oprogramowanie (i nie tylko)
Name:		yara
Version:	4.3.2
Release:	2
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/VirusTotal/yara/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cace2a274542e9c611c90b92b406a188
Patch0:		cflags.patch
URL:		https://virustotal.github.io/yara/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	jansson-devel
BuildRequires:	libmagic-devel
BuildRequires:	libtool >= 2:2
%{?with_crypto:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YARA is a tool aimed at (but not limited to) helping malware
researchers to identify and classify malware samples. With YARA you
can create descriptions of malware families (or whatever you want to
describe) based on textual or binary patterns. Each description, a.k.a
rule, consists of a set of strings and a boolean expression which
determine its logic.

%description -l pl.UTF-8
YARA to narzędzie, którego celem jest (głównie, ale nie tylko) pomoc
wyszukującym złośliwe oprogramowanie w identyfikacji i klasyfikacji
próbek takiego kodu. Przy użyciu YARA można tworzyć opisy rodzin
złośliwego oprogramowania (lub czegokolwiek innego) w oparciu o wzorce
tekstowe lub binarne. Każdy opis (reguła) składa się ze zbioru
łańcuchów i wyrażeń logicznych określających logikę.

%package devel
Summary:	Header files for yara library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki yara
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jansson-devel
Requires:	libmagic-devel
%{?with_crypto:Requires:	openssl-devel}

%description devel
Header files for yara library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki yara.

%package static
Summary:	Static yara library
Summary(pl.UTF-8):	Statyczna biblioteka yara
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static yara library.

%description static -l pl.UTF-8
Statyczna biblioteka yara.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__with_without crypto} \
	--enable-cuckoo \
	--enable-dex \
	--enable-macho \
	--enable-magic \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libyara.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS CONTRIBUTORS
%attr(755,root,root) %{_bindir}/yara
%attr(755,root,root) %{_bindir}/yarac
%attr(755,root,root) %{_libdir}/libyara.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libyara.so.10
%{_mandir}/man1/yara.1*
%{_mandir}/man1/yarac.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/yara.h
%{_includedir}/yara
%{_libdir}/libyara.so
%{_pkgconfigdir}/yara.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libyara.a
%endif
