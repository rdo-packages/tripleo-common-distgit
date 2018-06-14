# guard for package OSP does not support
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-common

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc Python library for code used by TripleO projects.

%{?!_licensedir:%global license %%doc}

Name:           openstack-tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://github.com/rdo-management/tripleo-common

Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n python2-%{upstream_name}
Summary:        Python library for code used by TripleO projects.

BuildRequires:  git
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  openstack-macros
BuildRequires:  python2-cryptography
BuildRequires:  python2-futures

Requires: GitPython
Requires: python2-jinja2
Requires: python2-glanceclient >= 1:2.8.0
Requires: python2-heatclient >= 1.10.0
Requires: python-ironic-inspector-client >= 1.5.0
Requires: python2-ironicclient >= 2.2.0
Requires: python2-keystoneclient
Requires: python2-novaclient >= 1:9.1.0
Requires: python2-mistral-lib >= 0.3.0
Requires: python2-mistralclient >= 3.1.0
Requires: python2-netaddr
Requires: python-netifaces
Requires: python2-oslo-concurrency >= 3.25.0
Requires: python2-oslo-config >= 2:5.1.0
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-six >= 1.10.0
Requires: python2-docker >= 2.4.2
Requires: python2-passlib
Requires: python2-keystoneauth1 >= 3.3.0
Requires: python2-pbr >= 2.0.0
Requires: python2-zaqarclient >= 1.0.0
Requires: %{name}-containers = %{version}-%{release}
Requires: python-paramiko
Requires: skopeo
Requires: ansible

# Ansible roles used by TripleO
Requires: ansible-role-container-registry
Requires: ansible-role-tripleo-modify-image
Requires: ansible-pacemaker
Requires: ansible-tripleo-ipsec
%if 0%{rhosp} == 1
Requires: ansible-role-redhat-subscription
%endif

Requires: python2-tenacity >= 3.2.1
Requires: python2-cryptography
Requires: python2-futures

Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

Provides: openstack-tripleo-common = %{version}-%{release}
Obsoletes: openstack-tripleo-common < %{version}-%{release}

%{?python_provide:%python_provide python2-%{upstream_name}}

%description -n python2-%{upstream_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{upstream_name}
Summary:        Python library for code used by TripleO projects.

BuildRequires:  git
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  openstack-macros
BuildRequires:  python3-cryptography

Requires: GitPython
Requires: python3-jinja2
Requires: python3-glanceclient >= 1:2.8.0
Requires: python3-heatclient >= 1.10.0
Requires: python3-ironic-inspector-client >= 1.5.0
Requires: python3-ironicclient >= 2.2.0
Requires: python3-keystoneclient
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-mistral-lib >= 0.3.0
Requires: python3-mistralclient >= 3.1.0
Requires: python3-netaddr
Requires: python3-netifaces
Requires: python3-oslo-concurrency >= 3.25.0
Requires: python3-oslo-config >= 2:5.1.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-six >= 1.10.0
Requires: python3-docker >= 2.4.2
Requires: python3-passlib
Requires: python3-keystoneauth1 >= 3.3.0
Requires: python3-pbr >= 2.0.0
Requires: python3-zaqarclient >= 1.0.0
Requires: %{name}-containers = %{version}-%{release}
Requires: python3-paramiko
Requires: skopeo
Requires: ansible

# Ansible roles used by TripleO
Requires: ansible-role-container-registry
Requires: ansible-role-tripleo-modify-image
Requires: ansible-pacemaker
Requires: ansible-tripleo-ipsec
%if 0%{rhosp} == 1
Requires: ansible-role-redhat-subscription
%endif

Requires: python3-tenacity >= 3.2.1
Requires: python3-cryptography

%{?python_provide:%python_provide python3-%{upstream_name}}

%description -n python3-%{upstream_name}
%{common_desc}
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%py3_build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
%if 0%{?with_python3}
%py3_install
%endif

# TODO remove when https://review.openstack.org/554926 is merged
touch %{buildroot}%{_bindir}/tripleo-overcloud-cert

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

if [ ! -d ansible_plugins ]; then
  mkdir -p %{buildroot}/%{_datadir}/ansible/plugins
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

if [ -f %{buildroot}%{_bindir}/upgrade-non-controller.sh ]; then
  rm -rf %{buildroot}%{_bindir}/upgrade-non-controller.sh
fi

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%description
%{common_desc}

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

%files -n python2-%{upstream_name}
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*
%{_prefix}/lib/heat/undercloud_heat_plugins
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/run-validation
%{_bindir}/tripleo-config-download
%{_bindir}/tripleo-overcloud-cert
%{_bindir}/create_freeipa_enroll_envfile.py
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}
%{_sysconfdir}/sudoers.d/%{upstream_name}
%{_datadir}/ansible/roles
%{_datadir}/ansible/plugins

%if 0%{?with_python3}
%files -n python3-%{upstream_name}
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python3_sitelib}/tripleo_common*
%exclude %{python3_sitelib}/tripleo_common/test*
%{_prefix}/lib/heat/undercloud_heat_plugins
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/run-validation
%{_bindir}/tripleo-config-download
%{_bindir}/tripleo-overcloud-cert
%{_bindir}/create_freeipa_enroll_envfile.py
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}
%{_sysconfdir}/sudoers.d/%{upstream_name}
%{_datadir}/ansible/roles
%{_datadir}/ansible/plugins
%endif

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
