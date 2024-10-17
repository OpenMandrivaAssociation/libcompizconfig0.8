%define __noautoprov 'pkgconfig(.*)'
%define __noautoreq 'pkgconfig\\(compiz\\)'

%define shortname compizconfig
%define oname libcompizconfig
%define oversion 0.8

%define git 20130330

%define major 8
%define libname %mklibname %{shortname} %{oversion} %{major}
%define devname %mklibname -d %{shortname}%{oversion}

%if %{git}
%define srcname %{oname}-compiz-%{oversion}.tar.bz2
%define distname %{oname}-compiz-%{oversion}
%define rel 0.%{git}.1
%else
%define srcname %{name}-%{version}.tar.bz2
%define distname %{name}-%{version}
%define rel 1
%endif

Summary:	Backend configuration library from Compiz Fusion
Name:		%{oname}%{oversion}
Version:	0.8.9
Release:	%{rel}
License:	GPL
Group:		System/X11
URL:		https://www.compiz.org/
Source0:	http://cgit.compiz.org/compiz/%{shortname}/%{oname}/snapshot/%{srcname}
# Make sure we don't conflict with main libcompizconfig
Patch0:		libcompizconfig0.8-soversion.patch
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	compiz0.8-devel
BuildRequires:	gettext-devel
BuildRequires:	intltool

%description
Backend configuration library from Compiz Fusion.

#----------------------------------------------------------------------------

%package -n compizconfig-backends%{oversion}
Summary:	Common files for backend configuration library from Compiz Fusion
Group:		System/X11
Conflicts:	%{_lib}%{shortname}0
Conflicts:	compizconfig-backends > 0.9

%description -n compizconfig-backends%{oversion}
Common files for backend configuration library from Compiz Fusion.

%files -n compizconfig-backends%{oversion}
%dir %{_sysconfdir}/compizconfig
%{_sysconfdir}/compizconfig/config
%{_libdir}/compiz/libccp.so
%{_libdir}/%{shortname}/backends/libini.so
%{_datadir}/compiz/ccp.xml

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Backend configuration library from Compiz Fusion
Group:		System/X11
Requires:	compizconfig-backends%{oversion} = %{version}-%{release}

%description -n %{libname}
Backend configuration library from Compiz Fusion.

%files -n %{libname}
%{_libdir}/%{oname}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for libcompizconfig
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Requires:	compiz0.8-devel
Provides:	%{shortname}%{oversion}-devel = %{version}-%{release}
Conflicts:	%{_lib}%{shortname}-devel

%description -n %{devname}
Development files for libcompizconfig.

%files -n %{devname}
%dir %{_includedir}/%{shortname}
%{_includedir}/%{shortname}/ccs.h
%{_includedir}/%{shortname}/ccs-backend.h
%{_libdir}/%{oname}.so
%{_libdir}/pkgconfig/%{oname}.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{distname}
%patch0 -p1

%build
%if %{git}
# This is a git snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif

# Needed due to X11 link cockup in src/Makefile.in
aclocal
automake
export LIBS="-ldl -lpthread"
%configure2_5x --disable-static
%make

%install
%makeinstall_std

