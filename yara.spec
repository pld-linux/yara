# TODO
# - http://yara.readthedocs.org/en/latest/gettingstarted.html#compiling-and-installing-yara
#   --with-crypto
#   --enable-cuckoo --enable-magic

# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	The pattern matching swiss knife for malware researchers (and everyone else)
Name:		yara
Version:	3.4.0
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/plusvic/yara/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b3f9d4e00c1da4d37af05b1f4488255f
URL:		http://plusvic.github.io/yara/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YARA is a tool aimed at (but not limited to) helping malware
researchers to identify and classify malware samples. With YARA you
can create descriptions of malware families (or whatever you want to
describe) based on textual or binary patterns. Each description, a.k.a
rule, consists of a set of strings and a boolean expression which
determine its logic.

%package devel
Summary:	Header files for yara library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki yara
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pcre-devel

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

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libyara.la

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
%attr(755,root,root) %ghost %{_libdir}/libyara.so.3
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
