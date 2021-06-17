Summary: PBR Monitor Spec
Name: PbrMon
Version: 1.5.1
Release: 1
License: Arista Networks
Group: EOS/Extension
Source0: %{name}-%{version}-%{release}.tar
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}.tar
BuildArch: noarch

%description
This EOS extenstion will monitor IPs and adjust PBR Nexthop Group Policies.

%prep
%setup -q -n source

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mkdir -p $RPM_BUILD_ROOT/usr/lib/SysdbMountProfiles
cp PbrMon $RPM_BUILD_ROOT/usr/local/bin/
cp PbrMon.mp $RPM_BUILD_ROOT/usr/lib/SysdbMountProfiles/PbrMon

%files
%defattr(-,root,root,-)
/usr/lib/SysdbMountProfiles/PbrMon
%attr(0775,root,root) /usr/local/bin/PbrMon
