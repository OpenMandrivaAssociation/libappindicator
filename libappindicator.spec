%define _disable_rebuild_configure 1

# As soon as EVRD macro really works I won't disable linting.Sflo
%define _build_pkgcheck_set %{nil}
%define major 1
%define girmajor 0.1

%bcond_with	python
%bcond_with	mono

%define libname		%mklibname appindicator
%define libdevel	%mklibname appindicator -d
%define girname		%mklibname appindicator-gir

%define oldlibname	%mklibname appindicator 3 1
%define oldgirname	%mklibname appindicator3-gir 0.1

Summary:	A library to allow applications to export a menu into the Unity Menu bar
Name:		libappindicator
Version:	12.10.1
Release:	1
Group:		System/Libraries
License:	GPLv3
URL:		https://launchpad.net/libappindicator
# see https://launchpad.net/ubuntu/+source/libappindicator/12.10.1+20.10.20200706.1-0ubuntu1
Source0:	https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/%{name}/%{version}+20.10.20200706.1-0ubuntu1/%{name}_%{version}+20.10.20200706.1.orig.tar.gz
#Source0:	https://launchpad.net/libappindicator/12.10/%{version}/+download/%{name}-%{version}.tar.gz
#Patch0:	libappindicator-mono-nunit-fix.patch
#Patch2:		libappindicator-12.10.0-mga-no-werror.patch
#Patch3:		libappindicator-mono.patch

BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4) >= 0.5.90
BuildRequires:	pkgconfig(indicator3-0.4) >= 0.4.93
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	perl-XML-SAX
BuildRequires:	vala-tools
BuildRequires:	vala-devel
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(libpng)
%if %{with mono}
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(gapi-2.0)
%endif
%if %{with python}
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(python2)
%endif

%description
A library to allow applications to export a menu into the Unity Menu bar.
Based on KSNI, it also works in KDE, and will fallback to generic Systray
support, if none of those are available.

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	libappindicator library
Group:		System/Libraries
Obsoletes:	%{oldlibname}
%description -n %{libname}
Library for libappindicator.

%files -n %{libname}
%{_libdir}/libappindicator3.so.%{major}
%{_libdir}/libappindicator3.so.%{major}.*

#--------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}3
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Obsoletes:	%{_lib}appindicator1 < 12.10.0-5
Obsoletes:	%{oldgirname}

%description -n %{girname}
GObject Introspection interface description for %{name}3.

%files -n %{girname}
%{_libdir}/girepository-1.0/AppIndicator3-%{girmajor}.typelib

#--------------------------------------------------------------------

%package -n %{libdevel}
Summary:	libappindicator development files
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Provides:	%{name}3-devel = %{EVRD}
Obsoletes:	%{_lib}appindicator-devel < 12.10.0-4

%description -n %{libdevel}
Development files needed by libappindicator.

%files -n %{libdevel}
%doc %{_datadir}/gtk-doc/html/libappindicator/
%{_includedir}/libappindicator3-0.1/
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%if %{with mono}
%{_libdir}/pkgconfig/appindicator-sharp-0.1.pc
%endif
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.*

#--------------------------------------------------------------------

%if %{with python}
%package -n python2-appindicator
Summary:		Python 2 bindings for %{name}
Group:			Development/Python
Requires:		%{libname} = %{EVRD}

%description -n python2-appindicator
This package contains the Python 2 bindings for the appindicator library.

%files -n python2-appindicator
%dir %{python2_sitearch}/appindicator/
%{python2_sitearch}/appindicator/__init__.py*
%{python2_sitearch}/appindicator/_appindicator.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/appindicator.defs
%endif

#--------------------------------------------------------------------

%if %{with mono}
%package -n %{name}-sharp
Summary:		libappindicator tool
Group:			Development/Other
%rename			appindicator-sharp

%description -n %{name}-sharp
Tool to load libappindicator plugins.

%files -n %{name}-sharp
%{_usr}/lib/mono/appindicator-sharp/
%{_usr}/lib/mono/gac/appindicator-sharp/
%{_usr}/lib/mono/gac/policy.0.0.appindicator-sharp/
%endif

#--------------------------------------------------------------------

%prep
%autosetup -p0 -c

sed -i "s#gmcs#mcs#g" configure.ac
#sed -i -e 's/ -Werror//' {src,tests}/Makefile.{am,in}

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=deprecated-declarations"
%if %{with python}
export PYTHON=%{__python2}
%else
export PYTHON=
%endif


autoreconf -fiv
%configure \
	--with-gtk=3 \
	--enable-gtk-doc \
	--disable-static
# Parallel make, crash the build
%make -j1


%install
%make_install

# Clean .la files
find %{buildroot} -name '*.la' -delete

