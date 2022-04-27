%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
# guard for package OSP does not support
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-common

%global common_desc Python library for code used by TripleO projects.

%{?!_licensedir:%global license %%doc}

Name:           openstack-tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://github.com/rdo-management/tripleo-common

Source0:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

Requires: golang-github-vbatts-tar-split >= 0.11.1
Requires: (python3dist(ansible) >= 2.9.10 or ansible-core)
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

Requires: %{name}-containers = %{version}-%{release}
Requires: python3-%{upstream_name} = %{version}-%{release}

Provides:  tripleo-common = %{version}-%{release}
Obsoletes: tripleo-common < %{version}-%{release}

%description
%{common_desc}

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
BuildRequires:  python3-novaclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-rootwrap
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslotest
BuildRequires:  python3-passlib
BuildRequires:  python3-requests-mock
BuildRequires:  python3-swiftclient
BuildRequires:  python3-tenacity
BuildRequires:  python3-testtools
BuildRequires:  python3-yaml
BuildRequires:  python3-ansible-runner
BuildRequires:  python3-stestr

Requires: python3-GitPython
Requires: python3-jinja2
Requires: python3-glanceclient >= 1:2.8.0
Requires: python3-heatclient >= 1.10.0
Requires: python3-ironic-inspector-client >= 1.5.0
Requires: python3-ironicclient >= 2.3.0
Requires: python3-keystoneclient
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-metalsmith >= 0.13.0
Requires: python3-netaddr
Requires: python3-netifaces
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-rootwrap >= 5.8.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-passlib >= 1.7.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-pbr >= 2.0.0
Requires: python3-eventlet >= 0.20.0
Requires: python3-jsonschema >= 3.2.0
Requires: python3-requests >= 2.18.0
Requires: python3-tenacity >= 6.1.0
Requires: python3-cryptography
Requires: python3-ansible-runner >= 1.4.4


%{?python_provide:%python_provide python3-%{upstream_name}}

%description -n python3-%{upstream_name}
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{upstream_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

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

if [ -d healthcheck ]; then
  cp -ar healthcheck %{buildroot}/%{_datadir}/%{name}/
else
  mkdir -p %{buildroot}/%{_datadir}/%{name}/healthcheck
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

# TODO(aschultz): remove once this once the file is removed from tripleo-common
if [ -f sudoers ] ; then
  rm -rf sudoers
fi

if [ -f %{buildroot}%{_bindir}/upgrade-non-controller.sh ]; then
  rm -rf %{buildroot}%{_bindir}/upgrade-non-controller.sh
fi

# Remove this when removed from tripleo-common
if [ -d %{buildroot}/%{_prefix}/lib/heat/undercloud_heat_plugins ]; then
  rm -rf %{buildroot}/%{_prefix}/lib/heat/undercloud_heat_plugins
fi

%check
export PYTHON=%{__python3}
stestr run

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
# (bandini) ruby3 split out rexml to a rubygem, some puppet modules need this
%if 0%{?rhel} > 8
Requires: rubygem-rexml
%endif
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
%{_datadir}/%{name}
%{_datadir}/%{upstream_name}

%files -n python3-%{upstream_name}
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python3_sitelib}/tripleo_common*
%exclude %{python3_sitelib}/tripleo_common/test*
%exclude %{_bindir}/run-validation
%exclude %{_bindir}/tripleo-container-image-prepare
%{_bindir}/tripleo-build-images
%{_bindir}/upload-puppet-modules
%{_bindir}/upload-swift-artifacts
%{_bindir}/upload-artifacts
%{_bindir}/tripleo-config-download
%{_bindir}/tripleo-mount-image
%{_bindir}/tripleo-unmount-image
%if 0%{rhosp} == 0
%{_bindir}/tripleo-deploy-openshift
%else
%exclude %{_bindir}/tripleo-deploy-openshift
%endif
%{_bindir}/create_freeipa_enroll_envfile.py

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
