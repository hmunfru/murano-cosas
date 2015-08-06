#!/bin/bash

set -eu

if [ -f "/etc/redhat-release" ]; then
  wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
  rpm -ivh epel-release-6-8.noarch.rpm
  yum install subversion git-core wget make gcc python-pip python-dev python-setuptools python-virtualenv -y
# Check for debian_version
elif [ -f "/etc/debian_version" ]; then
  apt-get update 
  apt-get install subversion  git-core wget make gcc python-pip python-dev python-setuptools python-virtualenv -y

else
  install-packages git-core wget make gcc python-pip python-dev python-setuptools python-virtualenv
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

#cp ${svc_root}/etc/muranoagent/muranoagent.conf.sample /etc/murano/agent.conf.sample

dir_folder=${svc_root}/contrib/elements/murano-agent/install.d/
# install upstart script for murano-agent
if [ -d "/etc/init/" ]; then
    install -D -g root -o root -m 0755 ${dir_folder}/murano-agent.conf /etc/init/
fi
if [ -d "/etc/systemd/system/" ]; then
    install -D -g root -o root -m 0755 ${dir_folder}/murano-agent.service /etc/systemd/system/
fi
cd /etc/init.d
wget http://repositories.testbed.fi-ware.org/webdav/murano-agent 
chmod 777 murano-agent
