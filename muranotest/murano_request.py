__author__ = 'henar'
import http
import json
import requests

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

    def deploy_env (self, token, env_id, conf_id):
        url = "http://{0}/v1/environments/{1}/sessions/{2}/deploy".format(self.murano_url, env_id, conf_id)
        headers = {'X-Auth-Token': token,
               'X-Configuration-Session': conf_id,
               'Accept': "application/json",
               'Content-Type': 'application/json'}

        print "Deploying the environment " + url
        payload=""
        response = http.post(url, headers, payload)

        if response.status != 200:
            print 'error to deploy the env ' + str(response.status)
            return


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