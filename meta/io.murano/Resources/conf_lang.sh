#!/bin/sh

# We obtain the Operative system distribution
if test -f "/etc/lsb-release" && grep -q DISTRIB_ID /etc/lsb-release; then
  platform=`grep DISTRIB_ID /etc/lsb-release | cut -d "=" -f 2 | tr '[A-Z]' '[a-z]'`
  platform_version=`grep DISTRIB_RELEASE /etc/lsb-release | cut -d "=" -f 2`
elif test -f "/etc/debian_version"; then
  platform="debian"
  platform_version=`cat /etc/debian_version`
elif test -f "/etc/redhat-release"; then
  platform=`sed 's/^\(.\+\) release.*/\1/' /etc/redhat-release | tr '[A-Z]' '[a-z]'`
  echo $platform
  platform_version=`sed 's/^.\+ release \([.0-9]\+\).*/\1/' /etc/redhat-release`
  echo $platform_version
fi

# We obtain the Operative system version

major_version=`echo $platform_version | cut -d. -f1`
case $platform in
  # FIXME: should remove this case statement completely
  "el")
    # FIXME:  "el" is deprecated, should use "redhat"
    platform_version=$major_version
    ;;
  "debian")
    # FIXME: remove client-side yolo here
    case $major_version in
      "5") platform_version="6";;  # FIXME: need to port this "reverse-yolo" into platform.rb
      "6") platform_version="6";;
      "7") platform_version="6";;
    esac
    ;;
  "freebsd")
    platform_version=$major_version
    ;;
  "sles")
    platform_version=$major_version
    ;;
  "suse")
    platform_version=$major_version
    ;;
esac

curl -L https://www.opscode.com/chef/install.sh | bash

if [ ${platform:0:6} == 'centos' ]; then
    echo $platform_version
    if [[ ${platform_version:0:1} = "6" ]]; then 
        rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm
    fi
    if [[ ${platform_version:0:1} = "7" ]]; then
        rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
    fi
    if [[ ${platform_version:0:1} = "5" ]]; then
       rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-5.noarch.rpm
    fi
    yum -y install puppet
else
    apt-get -y install puppet
fi

