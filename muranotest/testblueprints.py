__author__ = 'henar'
import sys
import http
import murano_request
import json
import os

def test_murano ():
    #KEYSTONE = '130.206.80.57:4731'
    #TENANT_ID = '00000000000000000000000000001'
    #USERNAME = 'admin'
    #PASSWORD = '8fa3c69e4c3e9fafa61'


    KEYSTONE = 'cloud.lab.fiware.org:4731'
    TENANT_ID = 'henar cloud'
    USERNAME = 'henar@tid.es'
    PASSWORD = 'vallelado'


    #TENANT_ID = 'b6d13f2f805a491b9ca1d9aefdf78540'
    #USERNAME = 'henarv32'
    #PASSWORD = 'henarv32'

    token = get_token(KEYSTONE,
                      TENANT_ID,
                      USERNAME,
                      PASSWORD)
    print token
    template_name = 'henartemplates'
    template = create_blueprint(token, template_name)
    print '-----------------------------------'
    add_service_puppet(token, template)
    print '-----------------------------------'
    result = convert_to_environment(token, template, template_name+'env')
    print result

    deploy_env(token, result[0], result[1])

def add_service_chef (token, env_id):
    payload="{\n\"instance\": {\n" \
            "   \"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"murano12\", \"?\": {\n" \
            "       \"type\": \"io.murano.resources.LinuxMuranoInstance\",\n " \
            "      \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"\n"  \
            "   },\n   \"name\": \"vmchef\"},\n\"name\": \"chef\", \n\"port\": \"80\",\n\"?\": {\n\
    \"_26411a1861294160833743e45d0eaad9\": {\n\
        \"name\": \"chef\"\n     },\n\
    \"type\": \"io.murano.conflang.test.ChefExample\",\n\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"\n}}"
    add_service(token, env_id, payload)

def add_service_puppet (token, env_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"centos2\", \"?\": {\"type\": \"io.murano.resources.ConfLangInstance\",\
           \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"chef\"}, \"name\": \"chef\",    \"port\": \"80\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\n   \"type\": \"io.murano.conflang.test.PuppetExample\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    add_service(token, env_id, payload)

def add_service_git (token, env_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"murano12\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"git\", \"repo\": \"repo\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"git\"},\
    \"type\": \"io.murano.apps.linux.Git\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    add_service(token, env_id, payload)

def add_service_tomcat (token, env_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"murano12\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"tomcat\"}, \"name\": \"git\", \"repo\": \"repo\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.apps.apache.Tomcat\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    add_service(token, env_id, payload)


def convert_to_environment(token, template_id, env_name):
    url = "http://130.206.84.6:8082/v1/templates/"+template_id+"/create-environment"
    headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}
    payload="{\"name\": \""+env_name+"\", \"network\": \"dd\"}"
    response = http.post(url, headers, payload)

    print "Convert template into environment " + url
    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        exit ()
    else:
        result = []
        response_json = json.load(response)
        result.append(response_json['environment_id'])
        result.append(response_json['session_id'])
        return result


def deploy_env (token, env_id, conf_id):
    url = "http://130.206.84.6:8082/v1/environments/"+env_id+"/sessions/"+conf_id+"/deploy"
    headers = {'X-Auth-Token': token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

    print "Deploying the environment " + url
    payload=""
    response = http.post(url, headers, payload)

    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        return

def deploy_git (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"murano11\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"git\", \"repo\": \"repo\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"git\"},\
    \"type\": \"io.murano.apps.linux.Git\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    deploy_software(token, env_id, conf_id, payload)

def deploy_chef (token, env_id, conf_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"murano11\", \"?\": {\"type\": \"io.murano.resources.LinuxMuranoInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"git\", \"port\": \"80\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.conflang.test.ChefExample\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    deploy_software(token, env_id, conf_id, payload)

def deploy_puppet (token, env_id, conf_id):
    payload="{\"instance\": {\"flavor\": \"m1.small\", \"keypair\": \"henar\", \"image\": \"murano11\", \"?\": {\"type\": \"io.murano.resources.LinuxMuranoInstance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"git\"}, \"name\": \"git\", \"port\": \"80\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.conflang.test.PuppetExample\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    deploy_software(token, env_id, conf_id, payload)

def deploy_orion (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \" muranoimage\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"orion\"}, \"name\": \"orion\", \"port\": \"1026\", \"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"orion\"},\
    \"type\": \"io.murano.apps.apache.Orion\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    deploy_software(token, env_id, conf_id, payload)


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
    deploy_software(token, env_id, conf_id, payload)



def deploy_tomcat (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \"murano11\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"tomcat\"}, \"name\": \"tomcat\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.apps.apache.Tomcat\",\
    \"id\": \"idtomcat\"}}"

    deploy_software(token, env_id, conf_id, payload)

def deploy_tomcat_app (token, env_id, conf_id):

    payload="{\"name\": \"tomcat\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.apps.apache.Tomcat\",\
    \"id\": \"idtomcat\"}}"

    deploy_software(token, env_id, conf_id, payload)

def deploy_vm_cluster (token, env_id, conf_id):

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \" muranoimage\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"cluster\"}, \"name\": \"cluster\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"cluster\"},\
    \"type\": \"io.murano.apps.test.SimpleVMcluster\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"

    deploy_software(token, env_id, conf_id, payload)


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
    deploy_software(token, env_id, conf_id, payload)



def deploy_software (token, env_id, conf_id, payload):
    url = "http://130.206.84.6:8082/v1/environments/"+env_id+"/services"
    headers = {'X-Auth-Token': token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

    response = http.post(url, headers, payload)

    print "Deploying services in the environment " + url
    print payload
    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        exit ()

def add_service (token, template_id, payload):
    url = "http://130.206.84.6:8082/v1/templates/"+template_id+"/services"
    headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

    response = http.post(url, headers, payload)

    print "Deploying services in the template " + url
    print payload
    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        exit ()

def deploy_service (token, env_id, conf_id):
    url = "http://130.206.84.6:8082/v1/environments/"+env_id+"/services"
    headers = {'X-Auth-Token': token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

    payload="{\"instance\": {\"flavor\": \"m1.small\", \"image\": \" muranoimage\", \"?\": {\"type\": \"io.murano.resources.Instance\",\
            \"id\":  \"5843836d2a4145f0895d7e66ee8ccf43\"}, \"name\": \"henartestq\"}, \"name\": \"sdf34sadf\",\"?\": {\
    \"_26411a1861294160833743e45d0eaad9\": {\
      \"name\": \"tomcat\"},\
    \"type\": \"io.murano.apps.apache.Tomcat\",\
    \"id\": \"190c8705-5784-4782-83d7-0ab55a1449aa\"}}"
    response = http.post(url, headers, payload)

    print "Deploying services in the environment " + url
    print payload
    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        return
    else:
         response_json = json.load(response)
         return

def configure_env (token, env_id):
    url = "http://130.206.84.6:8082/v1/environments/"+env_id+"/configure"
    headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}
    payload=''
    response = http.post(url, headers, payload)
    print "Creating a sessions " + url

    if response.status != 200:
        print 'error to get the product ' + str(response.status)
        return
    else:
         response_json = json.load(response)
         id = response_json['id']
         return id

def create_blueprint( token, env_name):
    url = "http://130.206.84.6:8082/v1/templates"
    headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}
    payload="{\"name\": \""+env_name+"\", \"network\": \"dd\"}"
    print "Creating a blueprint template " + url
    print payload
    response = http.post(url, headers, payload)

    if response.status != 200:
        print 'error to create the environment ' + str(response.status)
        return
    else:

         response_json = json.load(response)
         id = response_json['id']
         return id


def get_token(url_base, tenant_id, user, password):

    """It obtains a valid token.
    :param url_base: keystone url
    :param tenand_id: the id of the tenant
    :param user: the user
    :param paassword: the password
    """
    url = 'http://' + url_base + '/v2.0/tokens'
    headers = {'Content-Type': 'application/json'}
    payload = '{"auth":{"tenantName":"' + tenant_id +\
              '","passwordCredentials":{"username":"'\
              + user + '","password":"' + password + '"}}}'
    print payload
    print headers

    response = murano_request.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        print 'error to obtain the token ' + str(response.status_code)
        exit(1)
    response_json = response.json()
    token = response_json['access']['token']['id']
    return token

if __name__ == "__main__":
    test_murano ()

