#
# spec file for package make
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           make
Version:        4.1
Release:        0
Summary:        GNU make
License:        GPL-2.0+
Group:          Development/Tools/Building
Url:            http://www.gnu.org/software/make/make.html
Source:         http://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2
Source1:        http://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2.sig
# keyring downloaded from http://savannah.gnu.org/project/memberlist-gpgkeys.php?group=make
Source2:        %{name}.keyring
Patch1:         make-testcases_timeout.diff
Patch2:         make-4.1-fix_null_returns_from_ttyname.patch
Patch64:        make-library-search-path.diff
Requires(post): %{install_info_prereq}
Recommends:     %{name}-lang
Provides:       gmake
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The GNU make command with extensive documentation.

%lang_package

%prep
%setup -q
%patch1 -p1
%patch2 -p1
if [ %{_lib} == lib64 ]; then
%patch64 -p1
fi

%build
export CFLAGS="%{optflags}"
%configure
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
ln -s make %{buildroot}%{_bindir}/gmake
%find_lang %{name}
# gnumake.h was introduced in 4.0, looks useless
rm %{buildroot}%{_includedir}/gnumake.h

%files
%defattr(-,root,root)
%{_bindir}/make
%{_bindir}/gmake
%doc %{_infodir}/make.info-*.gz
%doc %{_infodir}/make.info.gz
%doc %{_mandir}/man1/make.1.gz

%files lang -f %{name}.lang
%defattr(-,root,root)

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%changelog
