#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	A malware identification and classification tool
Name:		yara
Version:	1.4
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://yara-project.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	ecc744a67482dc9d717936ccd69dc39f
URL:		http://code.google.com/p/yara-project/
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YARA is a tool aimed at helping malware researchers to identify and
classify malware samples. With YARA you can create descriptions of
malware families based on textual or binary patterns contained on
samples of those families. Each description consists of a set of
strings and a Boolean expression which determines its logic.

%package devel
Summary:	Header files for yara library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki yara
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/yara
%attr(755,root,root) %{_libdir}/libyara.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libyara.so.0
%{_mandir}/man1/yara.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/yara.h
%{_libdir}/libyara.so

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libyara.a
%endif
