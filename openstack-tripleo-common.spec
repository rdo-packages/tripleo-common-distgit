# guard for package OSP does not support
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-common

%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%endif

%global common_desc Python library for code used by TripleO projects.

%{?!_licensedir:%global license %%doc}

Name:           openstack-tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        11.4.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/rdo-management/tripleo-common

Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

Requires: golang-github-vbatts-tar-split >= 0.11.1
Requires: skopeo
Requires: ansible >= 2.9.10
# Ansible roles used by TripleO
Requires: ansible-role-container-registry
Requires: ansible-role-tripleo-modify-image
Requires: ansible-pacemaker
Requires: ansible-tripleo-ipa
Requires: ansible-tripleo-ipsec
%if 0%{rhosp} == 1
Requires: ansible-role-redhat-subscription
%endif

Requires: buildah
%if 0%{?fedora}
Requires: fuse-overlayfs
%endif

Requires: %{name}-containers = %{version}-%{release}
%if 0%{?with_python3}
Requires: python3-%{upstream_name} = %{version}-%{release}
%else
Requires: python2-%{upstream_name} = %{version}-%{release}
%endif

Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

%description
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{upstream_name}
Summary:        Python library for code used by TripleO projects.

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-eventlet
BuildRequires:  python3-pbr
BuildRequires:  python3-cryptography
BuildRequires:  python3-GitPython
BuildRequires:  python3-fixtures
BuildRequires:  python3-glanceclient
BuildRequires:  python3-heatclient
BuildRequires:  python3-ironicclient
BuildRequires:  python3-ironic-inspector-client
BuildRequires:  python3-jinja2
BuildRequires:  python3-metalsmith
BuildRequires:  python3-mistral-lib
BuildRequires:  python3-mistralclient
BuildRequires:  python3-novaclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-rootwrap
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslotest
BuildRequires:  python3-paramiko
BuildRequires:  python3-passlib
BuildRequires:  python3-requests-mock
BuildRequires:  python3-swiftclient
BuildRequires:  python3-tenacity
BuildRequires:  python3-testtools
BuildRequires:  python3-zaqarclient
BuildRequires:  python3-yaml

Requires: python3-GitPython
Requires: python3-jinja2
Requires: python3-glanceclient >= 1:2.8.0
Requires: python3-heatclient >= 1.10.0
Requires: python3-ironic-inspector-client >= 1.5.0
Requires: python3-ironicclient >= 2.3.0
Requires: python3-keystoneclient
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-metalsmith >= 0.9.0
Requires: python3-mistral-lib >= 0.3.0
Requires: python3-mistralclient >= 3.1.0
Requires: python3-netaddr
Requires: python3-netifaces
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-rootwrap >= 5.8.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-six >= 1.10.0
Requires: python3-passlib >= 1.7.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-pbr >= 2.0.0
Requires: python3-zaqarclient >= 1.0.0
Requires: python3-paramiko
Requires: python3-eventlet >= 0.20.0
Requires: python3-jsonschema >= 2.6.0
Requires: python3-requests >= 2.18.0

Requires: python3-tenacity >= 4.4.0
Requires: python3-cryptography

%{?python_provide:%python_provide python3-%{upstream_name}}

%description -n python3-%{upstream_name}
%{common_desc}
%else

%package -n python2-%{upstream_name}
Summary:        Python library for code used by TripleO projects.

BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-eventlet
BuildRequires:  python2-pbr
BuildRequires:  python2-cryptography
BuildRequires:  python2-futures
BuildRequires:  GitPython
BuildRequires:  python2-fixtures
BuildRequires:  python2-glanceclient
BuildRequires:  python2-heatclient
BuildRequires:  python2-ironicclient
BuildRequires:  python2-ironic-inspector-client
BuildRequires:  python2-jinja2
BuildRequires:  python2-metalsmith
BuildRequires:  python2-mistral-lib
BuildRequires:  python2-mistralclient
BuildRequires:  python2-novaclient
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-oslo-rootwrap
BuildRequires:  python2-oslotest
BuildRequires:  python2-paramiko
BuildRequires:  python2-passlib
BuildRequires:  python2-swiftclient
BuildRequires:  python2-tenacity
BuildRequires:  python2-testtools
BuildRequires:  python2-zaqarclient
BuildRequires:  python-requests-mock
BuildRequires:  python-yaml

Requires: GitPython
Requires: python2-jinja2
Requires: python2-glanceclient >= 1:2.8.0
Requires: python2-heatclient >= 1.10.0
Requires: python-ironic-inspector-client >= 1.5.0
Requires: python2-ironicclient >= 2.3.0
Requires: python2-keystoneclient
Requires: python2-novaclient >= 1:9.1.0
Requires: python2-metalsmith >= 0.13.0
Requires: python2-mistral-lib >= 0.3.0
Requires: python2-mistralclient >= 3.1.0
Requires: python2-netaddr
Requires: python-netifaces
Requires: python2-oslo-concurrency >= 3.26.0
Requires: python2-oslo-config >= 2:5.2.0
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-rootwrap >= 5.8.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-six >= 1.10.0
Requires: python2-passlib >= 1.7.0
Requires: python2-keystoneauth1 >= 3.4.0
Requires: python2-pbr >= 2.0.0
Requires: python2-zaqarclient >= 1.0.0
Requires: python-paramiko
Requires: python2-tenacity >= 4.4.0
Requires: python2-cryptography
Requires: python2-futures
Requires: python2-eventlet >= 0.20.0
Requires: python2-jsonschema >= 2.6.0
Requires: python2-requests >= 2.18.0

%{?python_provide:%python_provide python2-%{upstream_name}}

%description -n python2-%{upstream_name}
%{common_desc}

%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%if 0%{?with_python3}
%py3_build
%else
%py2_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%else
%py2_install
%endif

# TODO remove this when https://review.openstack.org/#/c/591346/ merges
touch %{buildroot}%{_bindir}/create_freeipa_enroll_envfile.py

# TODO remove this when https://review.openstack.org/#/c/675136/ merges
touch %{buildroot}%{_bindir}/tripleo-deploy-openshift

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
%if 0%{?with_python3}
export PYTHON=/usr/bin/python3
# (TODO) ignoring unit test errors as reported in https://bugs.launchpad.net/tripleo/+bug/1778903
%{__python3} setup.py test||true
%else
%{__python2} setup.py test
%endif

%package containers
Summary: Files for building TripleO containers

%description containers
This package installs the files used to build containers for TripleO.

%package container-base
Summary: Package for the TripleO base container image
Requires: crudini
Requires: curl
Requires: hostname
Requires: iproute
Requires: lsof
Requires: procps-ng
Requires: puppet
Requires: sudo

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
%{_prefix}/lib/heat/undercloud_heat_plugins
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
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/run-validation
%{_bindir}/tripleo-config-download
%{_bindir}/tripleo-container-image-prepare
%if 0%{rhosp} == 0
%{_bindir}/tripleo-deploy-openshift
%else
%exclude %{_bindir}/tripleo-deploy-openshift
%endif
%{_bindir}/create_freeipa_enroll_envfile.py
%else
%files -n python2-%{upstream_name}
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/run-validation
%{_bindir}/tripleo-config-download
%{_bindir}/tripleo-container-image-prepare
%if 0%{rhosp} == 0
%{_bindir}/tripleo-deploy-openshift
%else
%exclude %{_bindir}/tripleo-deploy-openshift
%endif
%{_bindir}/create_freeipa_enroll_envfile.py
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
* Mon Jun 22 2020 RDO <dev@lists.rdoproject.org> 11.4.0-1
- Update to 11.4.0

* Mon Jan 06 2020 RDO <dev@lists.rdoproject.org> 11.3.2-1
- Update to 11.3.2

* Fri Oct 25 2019 RDO <dev@lists.rdoproject.org> 11.3.1-1
- Update to 11.3.1

* Mon Oct 21 2019 RDO <dev@lists.rdoproject.org> 11.3.0-1
- Update to 11.3.0


