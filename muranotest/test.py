__author__ = 'henar'
import sys
import http
import murano_request
import json
import os
import instance
import murano_request

def test_murano ():

    requestm = murano_request.Request (KEYSTONE, "localhost:8082", TENANT_ID, USERNAME, PASSWORD)

    deploy_git(requestm, 'env2ddffffrfffd')
    deploy_orion_chef(requestm, 'env')
    deploy_puppet_git(requestm, 'env')
    deploy_orion_docker(requestm, 'ven')



def deploy_git(request, env_name):
    atts=[]
    atts.append({'repo': 'test'})
    prod = instance.Product('git', 'io.murano.apps.linux.Git', atts)
    deploy_normal_test2(request, 'git'+env_name, prod)

def deploy_tomcat(request, env_name):
    deploy_normal_test(request, 'tomcat'+env_name, 'tomcat', 'io.murano.apps.linux.Git')

def deploy_orion_chef(request, env_name):
    deploy_normal_test(request, 'orionchef'+env_name, 'orionchef', 'io.murano.conflang.fiware.OrionChef')

def deploy_puppet_git(request, env_name):
    deploy_normal_test(request, 'gitpuppet'+env_name, 'gitpuppet', 'io.murano.conflang.puppet.GitPuppet')



def deploy_normal_test(request, env_name, product_name, product_id):
    env = instance.Environment(env_name)
    inst = instance.Instance ('ubuntu', 'Ubuntu14.04init' )
    prod = instance.Product(product_name, product_id)
    service = instance.Service(product_name, prod)
    service.add_instance(inst)
    env.add_service (service)
    request.deploy_environment(env)

def deploy_normal_test2(request, env_name, product):
    env = instance.Environment(env_name)
    inst = instance.Instance ('ubuntu', 'Ubuntu14.04init' )
    service = instance.Service(product.name, product)
    service.add_instance(inst)
    env.add_service (service)
    request.deploy_environment(env)

def deploy_orion_docker(request, env_name, product_name, product_id):
    env = instance.Environment(env_name)
    inst = instance.Instance ('ubuntu', 'Ubuntu14.04init' )
    service = instance.Service('DockerOrion', 'docker', 'io.murano.apps.docker.DockerStandaloneHost')
    service.add_instance(inst)

    atts=[]
    atts.append({'publish': True})
    atts.append({'host': inst.id})
    service2 = instance.Service('dockerorion', 'dockerorion', 'io.murano.apps.docker.DockerOrion', atts)

    env.add_service (service)
    env.add_service (service2)
    request.deploy_environment(env)



def deploy_orion_docker2 (token, env_id, conf_id):

    payload="{\"instance\": {\"name\": \"vm\", \"flavor\": \"m1.small\", \"assignFloatingIp\": true, \"keyname\": \"nueva\", \"image\": \"Ubuntu14.04init\", \"?\": " \
            "{\"type\": \"io.murano.resources.ConfLangInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}}, \"name\": \"Docker standalone host\",  \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"Docker Standalone Host\"},\
    \"type\": \"io.murano.apps.docker.DockerStandaloneHost\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"},  \"dockerRegistry\": \"\"}"



def deploy_orion_docker2(token, env_id, conf_id):
    payload = "{\"host\": \"190c8705-5784-4782-83d7-0ab55a1449aa\", \"name\": \"DockerOrion\", \"?\":" \
              " {\"_26411a1861294160833743e45d0eaad9\": {\"name\": \"Orion \"}, \"type\": \"io.murano.apps.docker.DockerOrion\", " \
              "\"id\": \"df414676-4cb9-4135-9e34-5b7c2812489b\"}, \"publish\": true}"





def deploy_docker4 (token, env_id, conf_id):
    payload="{ "\
            " \"name\": \"dock\"}, \"name\": \"docker\", \"publish\": \"true\"," \
            " \"password\": \"dd\", \"host\": {" \
            "\"instance\": " \
            "{\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"Ubuntu14.04init\", \"?\":" \
            " {\"type\": \"io.murano.resources.ConfLangInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}," \
            " \"name\": \"dock\"}, \"?\":" \
            " {\"type\": \"io.murano.apps.docker.DockerStandaloneHost\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}} , \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.apps.docker.DockerTomcat\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"



def deploy_docker (token, env_id, conf_id):
    payload="{ \"name\": \"docker\", \"publish\": \"true\"," \
            " \"password\": \"dd\", \"host\":  " \
            "{\"instance\": {\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"Ubuntu14.04init\", \"?\":" \
            " {\"type\": \"io.murano.resources.LinuxMuranoInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"docker\", \"publish\": \"true\"," \
            " \"password\": \"dd\", \"host\": \"e91cdebf7ed94740bfe721afee5adedf\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.apps.docker.DockerStandaloneHost\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}, " \
            "\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.apps.docker.DockerTomcat\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"




def deploy_docker3 (token, env_id, conf_id):
    payload="{ \"name\": \"docker\", \"publish\": \"true\"," \
            " \"password\": \"dd\", \"host\": \"dd\" , \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.apps.docker.DockerTomcat\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"




def deploy_docker2 (token, env_id, conf_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"Ubuntu14.04init\", \"?\":" \
            " {\"type\": \"io.murano.resources.LinuxMuranoInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"muranodockerhost\", \"publish\": \"true\"," \
            " \"password\": \"dd\", \"host\": \"e91cdebf7ed94740bfe721afee5adedf\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"muranodockerhost\"},\
    \"type\": \"io.murano.apps.docker.DockerStandaloneHost\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"





def deploy_orion (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"CentOS-6.5-x64\", \"?\": {\"type\": \"io.murano.resources.ConfLangInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"orion\"}, \"name\": \"orion\", \"port\": \"1026\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.conflang.fiware.OrionChef\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"



def deploy_posgresql(token, env_id, conf_id):
    payload="{\"instance\": " \
                "{" \
                    "\"flavor\": \"m1.small\"," \
                    " \"image\": \" muranoimage\"," \
                    " \"?\": " \
                    "{" \
                        "\"type\": \"io.murano.resources.Instance\",\
                        \"id\":  \"instanceid\"" \
                    "}," \
                    " \"name\": \"vmname\"" \
                "}, " \
            "\"name\": \"postgresql\", " \
            "\"database\": \"mydatabase\", " \
            "\"username\": \"username\"," \
            "\"password\": \"password\"," \
            "\"?\": {\
                \"_26411a1861294160833743e45d0eaad9\": {\
                \"name\": \"git\"},\
            \"type\": \"io.murano.databases.PostgreSql\",\
            \"id\": \"idpostgresql\"}}"




def deploy_tomcat_chef (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"Ubuntu14.04init\", \"?\": {\"type\": \"io.murano.resources.ConfLangInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"tomcat\"}, \"name\": \"tomcat\", \"port\": 8080, \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.conflang.chef.TomcatChef\",\
    \"id\": \"idtomcat\"}}"



def deploy_tomcat_app (token, env_id, conf_id):

    payload="{\"name\": \"tomcat\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.apps.apache.Tomcat\",\
    \"id\": \"idtomcat\"}}"



def deploy_vm_cluster (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \" muranoimage\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"cluster\"}, \"name\": \"cluster\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"cluster\"},\
    \"type\": \"io.murano.apps.test.SimpleVMcluster\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"




def deploy_hello_world (token, env_id, conf_id):
    payload="{\"name\": \"helloworld\", " \
            "\"tomcat\": \"idtomcat\", " \
            "\"repository\": \"repository\"," \
            "\"dir\": \"dir\"," \
            "\"database\": \"idpostgresql\"," \
            "\"dbName\": \"dbName\"," \
            "\"dbUser\": \"dbUser\"," \
            "\"dbPassword\": \"dbPassword\"," \
            "\"?\": {\
                \"_26411a1861294160833743e45d0eaad9\": {\
                \"name\": \"git\"},\
            \"type\": \"io.murano.apps.java.HelloWorld\",\
            \"id\": \"idhello\"}}"




if __name__ == "__main__":
    test_murano ()

