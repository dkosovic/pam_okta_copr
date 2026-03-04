# pam_okta

VCS pam_okta repository for :
* https://copr.fedorainfracloud.org/coprs/dkosovic/pam-okta/

**pam_okta** is a Pluggable Authentication Module (PAM) that enables authentication against Okta:
* https://github.com/dgwynne/pam_okta


### Building on Fedora Copr

Select **Custom** for the source type.

Copy and paste the following script into the custom script text box:
```sh
#! /bin/sh

set -x # verbose output
set -e # fail the whole script if some command fails

git clone https://github.com/dkosovic/pam_okta_copr.git
mv pam_okta_copr/* .
rm -rf pam_okta_copr

commit=`grep "^%global commit" pam_okta.spec | awk '{ print $3 }'`
shortcommit=`echo "$commit" | cut -c1-7`
url=`grep "^URL:" pam_okta.spec | awk '{ print $2 }'`
name="pam_okta"
source0=`grep Source0: pam_okta.spec| awk '{ print $2 }' | sed -e "s#%{url}#$url#g" -e "s/%{name}/$name/g" -e "s/%{commit}/$commit/g" -e "s/%{shortcommit}/$shortcommit/g"`

curl -OL $source0
```

Copy and paste the following into the build dependencies field:
```
git
gcc
meson
ninja-build
byacc
pam-devel
jansson-devel
libbsd-devel
libcurl-devel
libjwt-devel
systemd-units
```

