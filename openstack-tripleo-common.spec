%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-common

%{?!_licensedir:%global license %%doc}

Name:           openstack-tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://github.com/rdo-management/tripleo-common

Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires: python-heatclient
Requires: python-oslo-config >= 2:3.14.0
Requires: python-oslo-log >= 1.14.0
Requires: python-oslo-utils >= 3.16.0
Requires: python-docker-py
Requires: instack-undercloud
Requires: python-passlib


Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
if [ -d %{buildroot}/%{_datadir}/%{upstream_name} ]; then
  mv %{buildroot}/%{_datadir}/%{upstream_name} %{buildroot}/%{_datadir}/%{name}
else
  # Before https://review.openstack.org/#/c/327830/3/setup.cfg
  mkdir -p %{buildroot}/%{_datadir}/%{name}
  if [ -d image-yaml ]; then
    install -d -m 755 %{buildroot}/%{_datadir}/%{name}
    cp -ar image-yaml %{buildroot}/%{_datadir}/%{name}
  fi
fi
ln -s %{name} %{buildroot}%{_datadir}/%{upstream_name}

if [ -d workbooks ]; then
  cp -ar workbooks %{buildroot}/%{_datadir}/%{name}/
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/workbooks
fi

install -p -D -m 440 sudoers %{buildroot}%{_sysconfdir}/sudoers.d/%{upstream_name}

%description
Python library for code used by TripleO projects.

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*
%{_prefix}/lib/heat/undercloud_heat_plugins
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}
%{_sysconfdir}/sudoers.d/%{upstream_name}

%changelog

