__author__ = 'henar'

import model
import murano_request

def test_murano ():

    KEYSTONE = 'cloud.lab.fiware.org:4731'
    TENANT_ID = 'henar cloud'
    USERNAME = 'henar@tid.es'
    PASSWORD = 'vallelado'

    requestm = murano_request.Request (KEYSTONE, "192.168.99.100:8082", TENANT_ID, USERNAME, PASSWORD)
    
    template_base_name ='aaffffff'

    #deploy_git(requestm, 'git' + template_base_name)
    #
    #deploy_tomcat(requestm, 'tomcat' + template_base_name)
    deploy_orion_chef(requestm, 'orionchef' + template_base_name)
    #deploy_mysql_puppet(requestm, 'mysqlpupet' + template_base_name)
    #deploy_orion_docker(requestm, 'oriondocker' + template_base_name)

    deploy_no_network(requestm, 'nonet' + template_base_name)
    #deploy_vm_no_exiting_network(requestm, 'notexisting' + template_base_name, 'minuevared')
    #deploy_two_networks_in_vm(requestm, 'twonets' + template_base_name)
    deploy_two_products_in_vm(requestm, 'twoproducts' + template_base_name)
    deploy_two_products_in_two_vms(requestm, 'twovms' + template_base_name)



def deploy_git(request, template_name):
    atts=[]
    atts.append({'repo': 'test'})
    prod = model.Product('git', 'io.murano.apps.linux.Git', atts)
    deploy_blueprint_template(request, template_name, prod)


def deploy_tomcat(request, template_name):
    atts=[]
    atts.append({'port': '8080'})
    prod = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    deploy_blueprint_template(request, template_name, prod)

def deploy_orion_chef(request, template_name):
    atts=[]
    atts.append({'port': '1026'})
    product = model.Product('orionchef', 'io.murano.conflang.chef.GitChef', atts)
    template = model.Template(template_name)
    net = model.Network("node-int-net-01", True)
    inst = model.Instance ('centos', 'CentOS-6.5init_deprecated', '2' , 'demo4', False, [net] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)
    request.deploy_template(template)

def deploy_mysql_puppet(request, template_name):
    atts=[]
    atts.append({'port': '1026'})
    prod = model.Product('msyqlpuppet', 'io.murano.conflang.puppet.MySQLPuppet', atts)
    deploy_blueprint_template(request, template_name, prod)

def deploy_blueprint_template(request, template_name, product):
    template = model.Template(template_name)
    net = model.Network("node-int-net-01", True)
    inst = model.Instance ('ubuntu', 'murano_agent_ubuntu14.04', '2' , 'demo4', False, [net] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)
    request.deploy_template(template)

def deploy_vm_no_exiting_network(request, template_name, network):
    atts=[]
    atts.append({'port': '8080'})
    template = model.Template(template_name)
    product = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    net = model.Network(network, False)
    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , 'demo4', False, [net] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)
    request.deploy_template(template)

def deploy_two_networks_in_vm(request, template_name):
    atts=[]
    atts.append({'port': '8080'})
    template = model.Template(template_name)
    product = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    net1 = model.Network('new', False)
    net2 = model.Network("node-int-net-01", True)
    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False, [net1, net2] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)
    request.deploy_template(template)

def deploy_no_network(request, template_name):
    atts=[]
    atts.append({'port': '8080'})
    template = model.Template(template_name)
    product = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)
    request.deploy_template(template)

def deploy_two_products_in_vm(request, template_name):
    atts=[]
    atts.append({'port': '8080'})
    template = model.Template(template_name)
    product = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    net = model.Network("node-int-net-01", True)
    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False, [net] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)

    product2 = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    service2 = model.Service(product2.name, product2)
    service2.add_instance(inst, True)
    template.add_service(service2)
    request.deploy_template(template)

def deploy_two_products_in_two_vms(request, template_name):
    atts=[]
    atts.append({'port': '8080'})
    template = model.Template(template_name)
    product = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    net = model.Network("node-int-net-01", True)
    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False, [net] )
    service = model.Service(product.name, product)
    service.add_instance(inst)
    template.add_service(service)

    product2 = model.Product('tomcat', 'io.murano.apps.apache.Tomcat', atts)
    inst2 = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False, [net] )
    service2 = model.Service(product2.name, product2)
    service2.add_instance(inst2)
    template.add_service(service2)
    request.deploy_template(template)

def deploy_orion_docker(request, template_name):
    template = model.Template(template_name)
    net = model.Network("node-int-net-01", True)

    inst = model.Instance ('ubuntu', 'Ubuntu14.04init_deprecated', '2' , '', False, [net] )
    product = model.Product('docker', 'io.murano.apps.docker.DockerStandaloneHost')
    service = model.Service(product.name, product)
    service.add_instance(inst)

    atts=[]
    atts.append({'publish': True})
    atts.append({'host': product.id})
    product = model.Product('dockerorion', 'io.murano.apps.docker.DockerOrion', atts)
    service2 = model.Service(product.name, product)

    template.add_service (service)
    template.add_service (service2)
    request.deploy_template(template)


if __name__ == "__main__":
    test_murano ()

