Summary: PBR Monitor Spec
Name: PbrMon
Version: 0.15
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
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/lib/python3.7/site-packages
mkdir -p $RPM_BUILD_ROOT/opt/EosIntfs
cp scripts/swIntf.py $RPM_BUILD_ROOT/usr/bin/swIntf
cp -r usr/lib/python3.7/site-packages/* $RPM_BUILD_ROOT/usr/lib/python3.7/site-packages/
cp -r opt/EosIntfs/* $RPM_BUILD_ROOT/opt/EosIntfs/

%files
%defattr(-,root,root,-)
/usr/bin/swIntf
/usr/lib/python2.7/site-packages
/etc/nginx/external_conf/EosIntfs.conf
/opt/EosIntfs
%attr(0755,root,root) /usr/bin/swIntf
