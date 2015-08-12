__author__ = 'henar'
import http
import json
import requests
import time

class Request:
    def __init__(self, keystone_url, murano_url, tenant, user, password):
        self.murano_url = murano_url
        self.keystone_url = keystone_url
        self.user = user
        self.password = password
        self.tenant = tenant

        self.token = self.get_token()
        self.environments = []



    def __get__token(self):
        return http.get_token("http://"+self.keystone_url + '/tokens', self.tenant, self.user, self.password)

    def deploy_environment(self, env):
        env_id = self.create_env(self.token, env)
        print env_id
        conf_id = self.configure_env(self.token, env_id)
        print conf_id
        for service in env.services:
            self.deploy_software (self.token, env_id, conf_id, service)

        self.deploy_env(self.token, env_id, conf_id)

    def deploy_template(self, template):
        template_id = self.create_template(template.name)

        for service in template.services:
            self.add_service ( template_id, service)

        result= self.convert_to_environment(template_id, template.name+'env')

        self.deploy_env(result[0], result[1])

        self.get_status(result[0])

        self.delete_env(result[0])

        self.delete_template(template_id)

    def create_env(self, token, env):

        url = "http://{0}/v1/environments".format(self.murano_url)
        headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        payload=json.dumps(env.to_json())
        #payload="{\"name\": \""+env_name+"\", \"defaultNetworks\": { \"environment\": {\"?\": {\"id\": 234, \"type\": \"io.murano.resources.ExistingNeutronNetwork\"}, \"internalNetworkName\": \"node-int-net-01\" }}}"
        print "---------------------------------------------"
        print "Creating an empty environment " + url
        print "---------------------------------------------"
        response = http.post(url, headers, payload)

        if response.status != 200:
            print 'error to create the environment ' + str(response.status)
            exit()
        else:
            response_json = json.load(response)
            print response_json
            id = response_json['id']
            return id

    def configure_env (self,token, env_id):
        url = "http://{0}/v1/environments/{1}/configure".format(self.murano_url, env_id)
        headers = {'X-Auth-Token': token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}
        payload=''
        response = http.post(url, headers, payload)

        if response.status != 200:
            print 'error to get the product ' + str(response.status)
            return
        else:
            response_json = json.load(response)
            id = response_json['id']
            return id

    def deploy_software (self, token, env_id, conf_id, service):
        url = "http://{0}/v1/environments/{1}/services".format(self.murano_url, env_id)
        headers = {'X-Auth-Token': token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}
        payload = json.dumps(service.to_json())
        response = http.post(url, headers, payload)
        print "---------------------------------------------"
        print "Deploying services in the environment " + url
        print payload
        print "---------------------------------------------"
        if response.status != 200:
            print 'error to get the product ' + str(response.status)
            exit ()

    def deploy_env (self, env_id, conf_id):
        url = "http://{0}/v1/environments/{1}/sessions/{2}/deploy".format(self.murano_url, env_id, conf_id)
        headers = {'X-Auth-Token': self.token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        print "Deploying the environment " + url
        payload=""
        response = http.post(url, headers, payload)

        if response.status != 200:
            print 'error to deploy the env ' + str(response.status)
            return

    def delete_env (self, env_id):
        url = "http://{0}/v1/environments/{1}".format(self.murano_url, env_id)
        headers = {'X-Auth-Token': self.token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        print "Deleting the environment " + url
        response = http.delete(url, headers)

        if response.status != 200:
            print 'error to delete the env ' + str(response.status)
            exit()

    def get_status(self, env_id):
        status = self.get_env_status(env_id)
        while status == 'deploying':
            status = self.get_env_status(env_id)
            if status == 'error':
                print 'ERROR'
                exit()
            elif status=='ready':
                print 'Deployed'
            time.sleep(10)
        self.get_env_deployment(env_id)

    def get_env_status (self, env_id):
        url = "http://{0}/v1/environments/{1}".format(self.murano_url, env_id)
        headers = {'X-Auth-Token': self.token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        print "Get the environment " + url
        response = http.get(url, headers)

        if response.status != 200:
            print 'error to get the env ' + str(response.status)
            exit()
        else:
            response_json = json.load(response)
            return response_json['status']

    def get_env_deployment (self, env_id):
        url = "http://{0}/v1/environments/{1}/deployments".format(self.murano_url, env_id)
        headers = {'X-Auth-Token': self.token,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        print "Get the environment " + url
        response = http.get(url, headers)

        if response.status != 200:
            print 'error to get the env ' + str(response.status)
            exit()
        else:
            response_json = json.load(response)
            if response_json['deployments'][0]['result']['isException'] == True:
                print "error " + response_json['deployments'][0]['result']['result'] ['message']
                exit()
            return response_json['deployments'][0]['state']

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

    def create_template(self, template_name):
        url = "http://{0}/v1/templates".format(self.murano_url)
        headers = {'X-Auth-Token': self.token,
                   'Accept': "application/json",
                   'Content-Type': 'application/json'}
        payload="{\"name\": \""+template_name+"\"}"
        print "Creating a blueprint template " + url
        print payload
        response = http.post(url, headers, payload)

        if response.status != 200:
            print 'error to create the environment ' + str(response.status)
            exit()
        else:
             response_json = json.load(response)
             id = response_json['id']
             return id

    def delete_template(self, template_id):
        url = "http://{0}/v1/templates/{1}".format(self.murano_url, template_id)
        headers = {'X-Auth-Token': self.token,
                   'Accept': "application/json",
                   'Content-Type': 'application/json'}

        print "Deleting a blueprint template " + url
        response = http.delete(url, headers)

        if response.status != 200:
            print 'error deleting the template' + str(response.status)
            exit()

    def add_service (self, template_id, service):
        url = "http://{0}/v1/templates/{1}/services".format(self.murano_url, template_id)
        headers = {'X-Auth-Token': self.token,
                   'Accept': "application/json",
                   'Content-Type': 'application/json'}
        payload = json.dumps(service.to_json())
        response = http.post(url, headers, payload)

        print "Deploying services in the template " + url
        print payload
        if response.status != 200:
            print 'error to deploy service in template ' + str(response.status)
            exit ()

    def convert_to_environment(self, template_id, env_name):
        url = "http://{0}/v1/templates/{1}/create-environment".format(self.murano_url, template_id)
        headers = {'X-Auth-Token': self.token,
                   'Accept': "application/json",
                   'Content-Type': 'application/json'}
        payload="{\"name\": \""+env_name+"\"}"
        response = http.post(url, headers, payload)

        print "Convert template into environment " + url
        if response.status != 200:
            print 'error convert to environment' + str(response.status)
            exit ()
        else:
            result = []
            response_json = json.load(response)
            result.append(response_json['environment_id'])
            result.append(response_json['session_id'])
            return result

    def get_token(self):

        """It obtains a valid token.
        :param url_base: keystone url
        :param tenand_id: the id of the tenant
        :param user: the user
        :param paassword: the password
        """
        url = 'http://' + self.keystone_url + '/v3/auth/tokens'
        headers = {'Content-Type': 'application/json'}


        payload = '{"auth":{"tenantName":"' + self.tenant +\
                  '","passwordCredentials":{"username":"'\
                  + self.user + '","password":"' + self.password + '"}}}'

        payload = '{ "auth": { \
        "scope": { \
          "project": { \
            "name": "' + self.tenant  + '",\
            "domain": { "id": "default" }\
          }\
        },\
        "identity": { \
          "methods": ["password"], \
          "password": { \
            "user": { \
              "name": "' + self.user + '", \
              "domain": { "id": "default" },\
              "password": "' + self.password + '"\
            } \
          } \
        } \
      } \
    }'
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200 and response.status_code != 201:
            print 'error to obtain the token ' + str(response.status_code)
            exit(1)
        response_json = response.json()
        token = response.headers['x-subject-token']
        return token