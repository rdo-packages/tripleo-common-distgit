%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-common

%{?!_licensedir:%global license %%doc}
%define _unpackaged_files_terminate_build 0

Name:           openstack-tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        XXX
Release:        XXX
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://github.com/rdo-management/tripleo-common

Source0:        https://pypi.python.org/packages/source/t/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires: python-heatclient
Requires: python-oslo-config >= 2:2.3.0
Requires: python-oslo-log >= 1.8.0


Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

%prep
%autosetup -n %{upstream_name}-%{version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
if [ -d workbooks ]; then
  install -d -m 755 %{buildroot}/%{_datadir}/%{name}
  cp -ar workbooks %{buildroot}/%{_datadir}/%{name}
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/workbooks
fi

%description
Python library for code used by TripleO projects.

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*
%{_prefix}/lib/heat/undercloud_heat_plugins
%{_bindir}/upgrade-non-controller.sh
%{_bindir}/tripleo-build-images
%{_datadir}/%{name}

%changelog

