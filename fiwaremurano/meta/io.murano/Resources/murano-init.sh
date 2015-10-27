#!/bin/bash

set -eu


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


if [ ${platform:0:6} == 'centos' ]; then
    echo $platform_version
    if [[ ${platform_version:0:1} = "6" ]]; then

        rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm 
        rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm
    fi
    if [[ ${platform_version:0:1} = "7" ]]; then
        rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
        rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
    fi
    if [[ ${platform_version:0:1} = "5" ]]; then
       rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-5.noarch.rpm
    fi
    yum -y install subversion git-core wget make gcc python-pip python-dev python-setuptools python-virtualenv  puppet
else
    apt-get update 
    apt-get install subversion  git-core wget make gcc python-pip python-dev python-setuptools python-virtualenv puppet -y
fi


name=murano-agent
svc_root=${DIB_MURANO_AGENT_SVC_ROOT:-/opt/stack/$name}
install_dir=${DIB_MURANO_AGENT_INSTALL_DIR:-/opt/stack/venvs/$name}
repo=${DIB_MURANO_AGENT_REPO:-git://git.openstack.org/openstack/murano-agent.git}
branch=${DIB_MURANO_AGENT_BRANCH:-master}
ref=${DIB_MURANO_AGENT_REF:-''}

# clone murano-agent source code into /opt/stack/murano-agent
mkdir -p $svc_root
git clone --depth=1 -b $branch $repo $svc_root
if [ -n "$ref" ]; then
    pushd $svc_root
    git fetch $repo $ref && git checkout FETCH_HEAD
    popd
fi

# install murano-agent into virtualenv at /ops/stack/venvs/murano-agent
virtualenv $install_dir
$install_dir/bin/pip install $svc_root

# setup config file at /etc/murano/agent.conf
mkdir -p /etc/murano

pushd ${svc_root}
${install_dir}/bin/oslo-config-generator --config-file ${svc_root}/etc/oslo-config-generator/muranoagent.conf
popd

cp ${svc_root}/etc/muranoagent/muranoagent.conf.sample /etc/murano/agent.conf.sample

dir_folder=${svc_root}/contrib/elements/murano-agent/install.d/
# install upstart script for murano-agent
if [ -d "/etc/init/" ]; then
    install -D -g root -o root -m 0755 ${dir_folder}/murano-agent.conf /etc/init/
fi
if [ -d "/etc/systemd/system/" ]; then
    install -D -g root -o root -m 0755 ${dir_folder}/murano-agent.service /etc/systemd/system/
fi

if [ ${platform:0:6} == 'centos' ]; then
    if [[ ${platform_version:0:1} = "6" ]]; then
     cd /etc/init.d
wget http://repositories.testbed.fi-ware.org/webdav/murano-agent 
chmod 777 murano-agent 
   fi
fi
service murano-agent start
