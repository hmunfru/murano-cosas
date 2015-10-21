FROM ubuntu
RUN apt-get update && sudo apt-get -y install python-pip python-dev \
  libmysqlclient-dev libpq-dev \
  libxml2-dev libxslt1-dev git \
  libffi-dev zip python-mysqldb mysql-server
RUN pip install tox
RUN git clone https://github.com/openstack/murano /opt/
COPY fiwar-murano/test-requirements.txt /opt/murano/test-requirements.txt
COPY fiware-murano/murano.conf /opt/murano/etc/murano/murano.conf
COPY fiware-murano/start.sh /opt/murano/start.sh
WORKDIR /opt/murano
EXPOSE 8082
RUN virtualenv .tox/venv
RUN /opt/murano/.tox/venv/bin/python .tox/venv/bin/pip install -U -r/opt/murano/requirements.txt
RUN /opt/murano/.tox/venv/bin/python .tox/venv/bin/pip install -U -r/opt/murano/test-requirements.txt
CMD ./start.sh; tox -e venv -- murano-engine --config-file ./etc/murano/murano.conf
