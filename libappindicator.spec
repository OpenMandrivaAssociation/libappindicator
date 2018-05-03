%define _disable_rebuild_configure 1

# As soon as EVRD macro really works I won't disable linting.Sflo
%define _build_pkgcheck_set %{nil}
%define major 1
%define girmajor 0.1

%define gtk3 1
%{?_without_gtk3: %global gtk3 0}
%{?_with_gtk3: %global gtk3 1}

%define gtk2 0
%{?_without_gtk3: %global gtk2 0}
%{?_with_gtk3: %global gtk2 1}

%if %gtk3
%define libname %mklibname appindicator 3 %{major}
%define libdevel %mklibname appindicator3 -d
%define girname %mklibname appindicator3-gir %{girmajor}
%endif

%if %gtk2
%define libgtk2name %mklibname appindicator 2 %{major}
%define libgtk2devel %mklibname appindicator2 -d
%define girgtk2name %mklibname appindicator2-gir %{girmajor}
%endif

%define build_mono 0

Summary:		A library to allow applications to export a menu into the Unity Menu bar
Name:			libappindicator
Version:		12.10.0
Release:		5
Group:			System/Libraries
License:		GPLv3
URL:			http://launchpad.net/libappindicator
Source0:		http://launchpad.net/libappindicator/12.10/%{version}/+download/%{name}-%{version}.tar.gz
#Patch0:			libappindicator-mono-nunit-fix.patch
Patch2:			libappindicator-12.10.0-mga-no-werror.patch
Patch3:			libappindicator-mono.patch

%if %gtk3
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4) >= 0.5.90
BuildRequires:	pkgconfig(indicator3-0.4) >= 0.4.93
%endif
%if %gtk2
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(dbusmenu-gtk-0.4) >= 0.5.90
BuildRequires:	pkgconfig(indicator-0.4) >= 0.4.93
BuildRequires:	pkgconfig(python2)
%endif
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	perl-XML-SAX
BuildRequires:	vala-tools
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(libpng)
%if %build_mono
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(gapi-2.0)
%endif
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(pygtk-2.0)

%description
A library to allow applications to export a menu into the Unity Menu bar.
Based on KSNI, it also works in KDE, and will fallback to generic Systray
support, if none of those are available.

%if %gtk3
#--------------------------------------------------------------------
%package -n %{libname}
Summary:		libappindicator library
Group:			System/Libraries

%description -n %{libname}
Library for libappindicator.

%files -n %{libname}
%{_libdir}/libappindicator3.so.%{major}
%{_libdir}/libappindicator3.so.%{major}.*

#--------------------------------------------------------------------
%package -n %{girname}
Summary:		GObject Introspection interface description for %{name}3
Group:			System/Libraries
Requires:		%{libname} = %{EVRD}
Obsoletes:		%{_lib}appindicator1 < 12.10.0-5

%description -n %{girname}
GObject Introspection interface description for %{name}3.

%files -n %{girname}
%{_libdir}/girepository-1.0/AppIndicator3-%{girmajor}.typelib

#--------------------------------------------------------------------
%package -n %{libdevel}
Summary:		libappindicator development files
Group:			Development/GNOME and GTK+
Requires:		%{libname} = %{EVRD}
Requires:		%{girname} = %{EVRD}
Provides:		%{name}3-devel = %{EVRD}
Obsoletes:		%{_lib}appindicator-devel < 12.10.0-4

%description -n %{libdevel}
Development files needed by libappindicator.

%files -n %{libdevel}
%doc %{_datadir}/gtk-doc/html/libappindicator/
%{_includedir}/libappindicator3-0.1/
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%if %build_mono
%{_libdir}/pkgconfig/appindicator-sharp-0.1.pc
%endif
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.*
%endif

%if %gtk2
#--------------------------------------------------------------------
%package -n %{libgtk2name}
Summary:		libappindicator gtk+2 library
Group:			System/Libraries

%description -n %{libgtk2name}
Gtk+2 library for libappindicator.

%files -n %{libgtk2name}
%{_libdir}/libappindicator.so.%{major}
%{_libdir}/libappindicator.so.%{major}.*

#--------------------------------------------------------------------
%package -n %{libgtk2devel}
Summary:		libappindicator gtk+2 development files
Group:			Development/GNOME and GTK+
Requires:		%{libgtk2name} = %{EVRD}
Requires:		%{girgtk2name} = %{EVRD}
Provides:		%{name}-devel = %{EVRD}
Obsoletes:		%{_lib}appindicator-devel < 12.10.0-3

%description -n %{libgtk2devel}
Development files needed by libappindicator for gtk+2.

%files -n %{libgtk2devel}
%doc %{_datadir}/gtk-doc/html/libappindicator/
%{_includedir}/libappindicator-0.1/
%{_libdir}/libappindicator.so
%{_libdir}/pkgconfig/appindicator-0.1.pc
%{_datadir}/gir-1.0/AppIndicator-0.1.gir
%{_datadir}/vala/vapi/appindicator-0.1.*

#--------------------------------------------------------------------
%package -n %{girgtk2name}
Summary:		GObject Introspection interface description for %{name}3
Group:			System/Libraries
Requires:		%{libgtk2name} = %{EVRD}
Conflicts:		%{_lib}appindicator1 < 12.10.0-3

%description -n %{girgtk2name}
GObject Introspection interface description for %{name}3.

%files -n %{girgtk2name}
%{_libdir}/girepository-1.0/AppIndicator-%{girmajor}.typelib

#--------------------------------------------------------------------
%package -n python2-appindicator
Summary:		Python 2 bindings for %{name}
Group:			Development/Python
Requires:		%{libgtk2name} = %{EVRD}

%description -n python2-appindicator
This package contains the Python 2 bindings for the appindicator library.

%files -n python2-appindicator
%dir %{python_sitearch}/appindicator/
%{py2_sitearch}/appindicator/__init__.py*
%{py2_sitearch}/appindicator/_appindicator.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/appindicator.defs

%endif
#--------------------------------------------------------------------
%if %build_mono
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
%setup -q -c

pushd %{name}-%{version}
%apply_patches
sed -i "s#gmcs#mcs#g" configure.ac
popd

cp -a %{name}-%{version} %{name}-gtk2
mv -f %{name}-%{version} %{name}-gtk3

%build
#export CC=gcc
#export CXX=g++
export PYTHON=%{__python2}
export CFLAGS+=" -fno-strict-aliasing -Wno-error=deprecated-declarations"

%if %gtk2
pushd %{name}-gtk2
sed -i "s#gmcs#mcs#g" configure.ac
sed -i -e 's/ -Werror//' {src,tests}/Makefile.{am,in}
autoreconf -vfi
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure \
        --with-gtk=2 \
        --disable-static
# Parallel make, crash the build
%make -j1
popd
%endif

%if %gtk3
pushd %{name}-gtk3
sed -i "s#gmcs#mcs#g" configure.ac
sed -i -e 's/ -Werror//' {src,tests}/Makefile.{am,in}
autoreconf -vfi
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure \
        --with-gtk=3 \
        --disable-static
# Parallel make, crash the build
%make -j1
popd
%endif

%install
%if %gtk2
pushd %{name}-gtk2
%makeinstall_std
popd
%endif

%if %gtk3
pushd %{name}-gtk3
%makeinstall_std
popd
%endif

# Clean .la files
find %{buildroot} -name '*.la' -delete
