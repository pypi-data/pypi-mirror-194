import json
from prettytable import PrettyTable


from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.node.node_creation_service import NodeCreation

class payload:
    def __init__(self, alias):
        node_specifications=NodeCreation(alias).node_listing()
       
        self.image = node_specifications['image']
        self.plan = node_specifications['plan']
        if(node_specifications['location']=='Delhi'):
                self.region='ncr'
        else:
                self.region='mumbai'
        self.security_group_id = Py_version_manager.py_input("please enter security group id : ")
        self.name = Py_version_manager.py_input("please enter name of your node : ")
        self.ssh_keys = []


class NodeCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False


    def create_node(self):
        Py_version_manager.py_print("adding")
        my_payload = payload(self.kwargs['alias'])
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, json.dumps(
            my_payload.__dict__), req).response.json()
        if (status['code'] == 200):
            x = PrettyTable()
            x.field_names = ["ID", "Name", "Created at", "disk"]
            x.add_row([status['data']['id'], status['data']['name'],
                      status['data']['created_at'], status['data']['disk']])
            Py_version_manager.py_print(x)
        else:
            Py_version_manager.py_print("oops errors !!")
            Py_version_manager.py_print(status['errors'])


    def delete_node(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_id = Py_version_manager.py_input("please enter node id : ")
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/" + str(node_id) + "/?apikey="+API_key
        req = "DELETE"
        confirmation =Py_version_manager.py_input("are you sure you want to delete press y for yes, else any other key : ")
        if(confirmation.lower()=="y"):
            status = Request(url, Auth_Token, my_payload, req).response.json()
            if (status['code'] == 200):
                Py_version_manager.py_print("Bucket successfully deleted")
            else:
                Py_version_manager.py_print(status['errors'])
        


    def get_node_by_id(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_id = Py_version_manager.py_input("please enter node id ")
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/" + str(node_id) + "/?apikey="+API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()
        if (status['code'] == 200):
            x = PrettyTable()
            x.field_names = ["VM id", "Name", "Created at", "disk", "RAM", "Public IP"]
            x.add_row([ status['data']['vm_id'], status['data']['name'], status['data']['created_at'], status['data']['disk'],  status['data']['memory'], status['data']['public_ip_address'] ])
            Py_version_manager.py_print(x)
        else:
            Py_version_manager.py_print(status['errors'])


    def list_node(self, parameter=0):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "GET"
        list = Request(url, Auth_Token, my_payload,
                       req).response.json()['data']
        
        if parameter == 0:               
            i = 1
            Py_version_manager.py_print("Your Nodes : ")
            if (list):
                x = PrettyTable()
                x.field_names = ["index", "ID", "Name", "Created at", "disk"]
                for element in list:
                    x.add_row([i, element['id'], element['name'],
                            element['created_at'], element['disk']])
                    i = i+1
                Py_version_manager.py_print(x)
            else:
                Py_version_manager.py_print("Either list is empty or an error occurred!!")
        else:
            return list


    def update_node(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        Py_version_manager.py_print("update call")
