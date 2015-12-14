%{?!_licensedir:%global license %%doc}
%define _unpackaged_files_terminate_build 0

Name:           tripleo-common
Summary:        Python library for code used by TripleO projects.
Version:        0.1
Release:        3%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://github.com/rdo-management/tripleo-common

Source0: https://pypi.python.org/packages/source/t/tripleo-common/tripleo-common-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires: python-heatclient
Requires: python-oslo-config >= 2:2.3.0
Requires: python-oslo-log >= 1.8.0


%prep
%autosetup -v -p 1 -n %{name}-%{upstream_version}
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%description
Python library for code used by TripleO projects.

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_common*
%exclude %{python2_sitelib}/tripleo_common/test*


%changelog

