__author__ = 'henar'

import json
import uuid


class Instance:
    def __init__(self, name, image='694ae405-0731-4dab-a50f-d089d1cca04d',
                 flavour='m1.small', keyname='', floatingip='false' ):
        self.name = name
        self.image = image
        self.flavour = flavour
        self.keyname = keyname
        self.assignFloatingIp = floatingip
        self.id=uuid.uuid4().hex

    def to_json(self):
        instance_json = {}
        instance_json ['name'] = self.name
        instance_json ['image'] = self.image
        instance_json ['flavour'] = self.flavour
        instance_json ['keyname'] = self.keyname
        instance_json ['assignFloatingIp'] = self.assignFloatingIp
        instance_json["?"] = {'type' : 'io.murano.resources.ConfLangInstance', 'id': self.id}
        return instance_json

class Service:

    def __init__(self, name, prod):
        self.name = name
        self.product = prod
        self.attributes=prod.attributes

    def add_instance(self, instance):
        self.instance = instance

    def add_network(self, network):
        self.networks.append(network)


    def delete_product(self, product):
        self.products.pop(product)

    def to_json(self):
        service_json = {}
        service_json['name'] = self.name

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
        product_json['name'] = self.name
        product_json['type'] = self.type
        product_json['id'] = self.id



        return product_json



class Environment:
    def __init__(self, name):
        self.name = name
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    def to_json(self):
        environment_json = {}
        environment_json['name'] = self.name

        if self.services is not None:
            for service in self.services:
               environment_json['dd']  = service.to_json()
        return environment_json


