%define major 1
%define libname %mklibname appindicator %{major}
%define develname %mklibname appindicator -d

Summary:	Application indicators library
Name:		libappindicator
Version:	0.4.1
Release:	2
License:	LGPLv2,LGPLv3
Url:		https://launchpad.net/libappindicator
Group:		System/Libraries
Source0:	%{name}-%{version}.tar.gz
# PATCH-FIX-OPENSUSE 001_opensuse_build_fix_all.patch nmarques@opensuse.org 
#-- This patch fixes python links and  eplaces pkgconfig() calls from "nunit" to "mono-nunit"
# PATCH-FIX-OPENSUSE - libappindicator-mono-nunit-fix.patch nmarques@opensuse.org 
#-- use mono-nunit for pkgconfig() calls instead of nunit
Patch0:	libappindicator-mono-nunit-fix.patch
# PATCH-FIX-OPENSUSE - libappindicator-header-fixes.patch nmarques@opensuse.org 
#-- fixe header includes
Patch1:	libappindicator-header-fixes.patch
#-- fix .pc file
Patch2:	libappindicator-pkgconfig-fix.patch

BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  perl-XML-SAX
BuildRequires:  vala-devel
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(gapi-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gnome-doc-utils)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-sharp-2.0)
BuildRequires:  pkgconfig(indicate-0.6)
BuildRequires:  pkgconfig(indicator3-0.4)
BuildRequires:  pkgconfig(libpng15)
BuildRequires:  pkgconfig(mono)
BuildRequires:  pkgconfig(mono-nunit)
BuildRequires:  pkgconfig(pygobject-2.0)
BuildRequires:  pkgconfig(pygtk-2.0)

%description
A library and indicator to take menus from applications and place them in
the panel.

%package -n %{libname}
Summary:	Application indicator library - shared libraries
Group:		System/Libraries

%description -n %{libname}
A library and indicator to take menus from applications and place them in
the panel.

This package provides the shared libraries to be used by applications.

%package -n appindicator-sharp
Summary:	Application indicator library - assembly CLI
Group:		Development/Other

%description -n appindicator-sharp
This package provides the appindicator-sharp assembly that allows CLI (.NET)
programs to take menus from applications and place them in the panel.

This package provides assemblies to be used by applications

%package -n %{develname}
Summary:	Application indicator library - development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
A library and indicator to take menus from the applications and place them in
the panel.

This package provides the files that are needed to build applications.

%prep
%setup -q
%apply_patches

%build
# Warning, patch requires reconf
NOCONFIGURE=1 autoreconf -fi
%configure2_5x \
  --disable-static \
  --with-gtk=3

make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print

%files -n %{libname}
%doc README COPYING COPYING.LGPL.2.1
%{_libdir}/*.so.%{major}*
%{_libdir}/girepository-1.0/*.typelib

%files -n appindicator-sharp
%{_prefix}/lib/mono/appindicator-sharp/
%{_prefix}/lib/mono/gac/
%{_libdir}/cli/appindicator-sharp*

%files -n %{develname}
%{_includedir}/libappindicator3-0.1/
%{_datadir}/gtk-doc/html/libappindicator/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/
