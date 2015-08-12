__author__ = 'henar'

import json
import uuid


class Instance:
    def __init__(self, name, image='694ae405-0731-4dab-a50f-d089d1cca04d',
                 flavor='m1.small', keyname='', floatingip='false', networks=[] ):
        self.name = name
        self.image = image
        self.flavor = flavor
        self.keyname = keyname
        self.assignFloatingIp = floatingip
        self.id=uuid.uuid4().hex
        self.networks=networks


    def to_json(self):
        instance_json = {}
        instance_json ['name'] = self.name
        instance_json ['image'] = self.image
        instance_json ['flavor'] = self.flavor
        instance_json ['keyname'] = self.keyname
        instance_json ['assignFloatingIp'] = self.assignFloatingIp
        instance_json["?"] = {'type' : 'io.murano.resources.ConfLangInstance', 'id': self.id}

        if self.networks is not None:
            networks = {}
            networks['useFlatNetwork'] = False
            networks['primaryNetwork'] = None
            networks['useEnvironmentNetwork'] = False
            networks['customNetworks'] = []

            for net in self.networks:
                networks['customNetworks'] .append(net.to_json())

            instance_json['networks'] = networks
        return instance_json

class Service:

    def __init__(self, name, prod):
        self.name = name
        self.product = prod
        self.attributes=prod.attributes
        self.id = uuid.uuid4().hex
        self.instance = None

    def add_instance(self, instance, existing_instance=False):
        self.instance = instance
        self.existing_instance = existing_instance

    def add_network(self, network):
        self.networks.append(network)


    def delete_product(self, product):
        self.products.pop(product)

    def to_json(self):
        service_json = {}
        service_json['name'] = self.name

        if self.instance is not None and self.existing_instance:
            service_json['instance'] = self.instance.id
        elif self.instance is not None and self.existing_instance is False:
            service_json['instance'] = self.instance.to_json()
        service_json['?'] = self.product.to_json()
        if self.attributes is not None:
            for att in self.attributes:
                service_json[att.keys()[0]] = att.values()[0]
        return service_json


class Product:
    def __init__(self, name, type, attributes=None):
        self.name = name
        self.type = type
        self.id = uuid.uuid4().hex
        self.attributes = attributes

    def to_json(self):
        product_json = {}
        product_json['_26411a1861294160833743e45d0eaad9'] = {"name": self.name}
        product_json['type'] = self.type
        product_json['id'] = self.id
        return product_json

class Network:
    def __init__(self, name, existing ):
        self.id = uuid.uuid4().hex
        self.name = name
        self.existing = existing

    def to_json(self):
        net_json = {}

        if self.existing:
            net_json['internalNetworkName'] = self.name
            net_json['?'] = {"type": "io.murano.resources.ExistingNeutronNetwork", "id": self.id}
        else:
            net_json['name'] = self.name
            net_json['autoUplink'] = True
            net_json['autogenerateSubnet'] = True
            net_json['?'] = {"type": "io.murano.resources.NeutronNetworkBase", "id": self.id}
        return net_json


class Template:
    def __init__(self, name, network=None):
        self.name = name
        self.network=network
        self.services = []
        self.id = uuid.uuid4().hex

    def add_service(self, service):
        self.services.append(service)

    def to_json(self):
        environment_json = {}
        environment_json['name'] = self.name

        if self.network is not None:
            net_network={}
            net_network['internalNetworkName'] = self.network
            net_network['?']={'id': 'id', 'type': 'io.murano.resources.ExistingNeutronNetwork'}
            env_json2={'environment': net_network}
            environment_json['defaultNetworks']=env_json2

        if self.services is not None:
            for service in self.services:
               environment_json['?']  = service.to_json()
        return environment_json


