# TODO
# - http://yara.readthedocs.org/en/latest/gettingstarted.html#compiling-and-installing-yara
#   --enable-cuckoo --enable-magic

# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	python2		# CPython 2.x module
%bcond_without	crypto		# build without tests

Summary:	The pattern matching swiss knife for malware researchers (and everyone else)
Name:		yara
Version:	3.4.0
Release:	5
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/plusvic/yara/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b3f9d4e00c1da4d37af05b1f4488255f
Patch0:		cflags.patch
URL:		http://plusvic.github.io/yara/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_crypto:BuildRequires:	openssl-devel}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
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

%package -n python-%{name}
Summary:	Python bindings to yara library
Group:		Development/Languages/Python
Requires:	python-modules

%description -n python-%{name}
This is a Python extension that gives you access to YARA's powerful
features from your own Python scripts.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__with_without crypto} \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with python2}
cd yara-python
%py_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libyara.la

%if %{with python2}
cd yara-python
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

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

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%doc yara-python/README
%attr(755,root,root) %{py_sitedir}/yara.so
%{py_sitedir}/yara_python-*.egg-info
%endif
