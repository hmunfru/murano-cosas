git fetch https://review.openstack.org/openstack/murano refs/changes/$REVISION && git checkout FETCH_HEAD
apt-get install -y curl host syslinux
host="murano"
ip="`gethostip -d "$host"`"
echo $ip
echo "$ip murano.lab.fiware.org" >> /etc/hosts
while ! nc -z murano 8082; do sleep 8; done
curl http://$ip:8082
sed -i -e "s/XXX/${PASSWORD}/" /etc/tempest/tempest.conf
