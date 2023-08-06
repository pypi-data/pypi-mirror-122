%global srcname nexusformat

%define debug_package %{nil}

Name:           python-%{srcname}
Version:        0.3.1
Release:        1%{?dist}
Summary:        Python API to NeXus files using h5py

License:        BSD
URL:            https://nexpy.github.io/nexpy/
Source0:        https://github.com/nexpy/nexusformat/archive/v%{version}.zip

Requires:       h5py
Requires:	numpy

BuildRequires:  numpy
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Python API to NeXus files using h5py

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%install
%py2_install


%files
%doc README.rst README.md README
%{python2_sitelib}/nexusformat/*
%{python2_sitelib}/nexusformat-%{version}-py2*.egg-info/*
%{_bindir}/nxstack
%{_bindir}/nxstartserver

%changelog
* Thu Apr  7 2016 Stuart Campbell <campbellsi@ornl.gov> - 0.2.2-1
- Initial package
