%define themename deskos
%define set_theme %{_sbindir}/plymouth-set-default-theme

Name:           plymouth-theme-deskos
Version:        0.1
Release:        1
Summary:        Plymouth DeskOS Theme

Group:          System Environment/Base
License:        CC-BY-SA
URL:            https://github.com/deskosproject/plymouth-theme-deskos-rpm
Source0:        https://dl.deskosproject.org/sources/plymouth-theme-deskos/%{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       plymouth-plugin-two-step
Requires(post): plymouth-scripts

%description
This package contains the DeskOS boot splash theme for Plymouth.

%prep
%setup -q

%build

%install
targetdir=$RPM_BUILD_ROOT/%{_datadir}/plymouth/themes/%{themename}
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $targetdir
install -m 0644 %{themename}.plymouth *.png $targetdir

%post
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{set_theme} %{themename}
fi
if [ "$(%{set_theme})" == "%{themename}" ]; then
    %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
fi

%postun
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{set_theme})" == "%{themename}" ]; then
        %{set_theme} --reset
        %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%dir %{_datadir}/plymouth/themes/%{themename}
%{_datadir}/plymouth/themes/%{themename}/*.png
%{_datadir}/plymouth/themes/%{themename}/%{themename}.plymouth

%changelog
* Thu Mar 24 2016 Ricardo Arguello <rarguello@deskosproject.org> - 0.1-1
- Initial RPM release
