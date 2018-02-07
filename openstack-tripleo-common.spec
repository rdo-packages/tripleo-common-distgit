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
BuildRequires:  openstack-macros

Requires: GitPython
Requires: python-jinja2
Requires: python-gitdb
Requires: python-glanceclient >= 2.7.0
Requires: python-heatclient >= 1.6.1
Requires: python-ironic-inspector-client >= 1.5.0
Requires: python-ironicclient >= 1.14.0
Requires: python-keystoneclient
Requires: python-novaclient >= 1:9.0.0
Requires: python-mistral-lib >= 0.2.0
Requires: python-mistralclient >= 3.1.0
Requires: python-netaddr
Requires: python-netifaces
Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-log >= 3.22.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-six >= 1.9.0
Requires: python-docker >= 2.0.0
Requires: python-passlib
Requires: %{name}-containers = %{version}-%{release}
Requires: python-paramiko
Requires: skopeo
Requires: ansible
Requires: python-keystoneauth1

Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

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

if [ -d playbooks ]; then
  cp -ar playbooks %{buildroot}/%{_datadir}/%{name}/
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/playbooks
fi

if [ -d healthcheck ]; then
  cp -ar healthcheck %{buildroot}/%{_datadir}/%{name}/
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/healthcheck
fi

if [ ! -d roles ]; then
  mkdir -p %{buildroot}/%{_datadir}/ansible/roles
fi

mkdir -p %{buildroot}/%{_datadir}/%{name}-containers
mv %{buildroot}/%{_datadir}/%{name}/container-images %{buildroot}/%{_datadir}/%{name}-containers/
# compat symlink
ln -s ../%{name}-containers/container-images  %{buildroot}/%{_datadir}/%{name}/

if [ -d heat_docker_agent ]; then
  cp -ar heat_docker_agent %{buildroot}/%{_datadir}/%{name}/
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/heat_docker_agent
fi

install -p -D -m 440 sudoers %{buildroot}%{_sysconfdir}/sudoers.d/%{upstream_name}

%description
Python library for code used by TripleO projects.

%package containers
Summary: Files for building TripleO containers

%description containers
This package installs the files used to build containers for TripleO.

%package container-base
Summary: Package for the TripleO base container image
Requires: puppet
Requires: lsof
Requires: hostname

%description container-base
This package installs the dependencies and files which are required on the base
TripleO container image.

%package devtools
Summary: A collection of tools for TripleO developers and CI
Requires: %{name} = %{version}-%{release}

%description devtools
This package installs the TripleO tools for developers and CI that typically
don't fit in a product.

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*
%{_prefix}/lib/heat/undercloud_heat_plugins
%{_bindir}/upgrade-non-controller.sh
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/run-validation
%{_bindir}/tripleo-config-download
%{_bindir}/create_freeipa_enroll_envfile.py
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}
%{_sysconfdir}/sudoers.d/%{upstream_name}
%{_datadir}/ansible/roles

%files containers
%{_datadir}/%{name}-containers/container-images

%files container-base
%{_bindir}/bootstrap_host_exec
%{_bindir}/bootstrap_host_only_eval
%{_bindir}/bootstrap_host_only_exec
%{_datadir}/%{name}/healthcheck

%files devtools
%{_bindir}/pull-puppet-modules

%changelog
