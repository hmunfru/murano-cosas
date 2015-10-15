tox -e venv -- murano-db-manage \
  --config-file ./etc/murano/murano.conf upgrade
cd  ./meta/io.murano
zip -r ../../io.murano.zip *
cd ./../../
tox -e venv -- murano-api --config-file ./etc/murano/murano.conf &
tox -e venv -- murano --murano-url http://localhost:8082 --os-username admin --os-password XXX \
  --os-tenant-name admin --os-auth-url=http://cloud.lab.fi-ware.org:4730/v2.0 \
  package-import --exists-action u  --is-public io.murano.zip
git clone https://github.com/openstack/murano-apps
cd murano-apps/Chef/OrionChef/package
zip -r ./../../../cheforion.zip *
cd ./../../../../
tox -e venv -- murano --murano-url http://localhost:8082  --os-username admin --os-password XXX \
  --os-tenant-name admin --os-auth-url=http://cloud.lab.fi-ware.org:4730/v2.0 \
  package-import --exists-action u --is-public murano-apps/cheforion.zip
cd murano-apps/Chef/GitChef/package
zip -r ./../../../gitchef.zip *
cd ./../../../../
tox -e venv -- murano --murano-url http://localhost:8082  --os-username admin --os-password XXX \
  --os-tenant-name admin --os-auth-url=http://cloud.lab.fi-ware.org:4730/v2.0 \
  package-import --exists-action u --is-public murano-apps/gitchef.zip
