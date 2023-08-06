from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred

class payload:
    def __init__(self):
        self.image= Py_version_manager.py_input("please enter OS you require ")
        self.name= Py_version_manager.py_input("please enter name of your bucket ")
        self.plan= Py_version_manager.py_input("please enter system requirements/plans ")
        self.region= Py_version_manager.py_input("region in which server is desired mumbai/ncr ")
        self.security_group_id= Py_version_manager.py_input("please security group id ")
        self.ssh_keys= []


class bucketCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
        

    def create_bucket(self):
        Py_version_manager.py_print("adding")
        my_payload= {}  
        bucket_name=Py_version_manager.py_input("input name of your new bucket : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        if (status['code'] == 200):
            x = PrettyTable()
            x.field_names = ["ID", "Name", "Created at"]
            x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
            Py_version_manager.py_print(x)
        else:
            Py_version_manager.py_print(status['errors'])



    def delete_bucket(self):
        my_payload={}
        bucket_name=Py_version_manager.py_input("input name of the bucket you want to delete : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        if(status['code']==200):
                Py_version_manager.py_print("Bucket successfully deleted")
        else :
                Py_version_manager.py_print("There seems to be an error, retry with the correct name")
                Py_version_manager.py_print(status['errors'])


    
    def list_bucket(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/?apikey="+ API_key+"&location=Delhi"
        req="GET"
        Py_version_manager.py_print("Your Buckets : ")
        list=Request(url, Auth_Token, my_payload, req).response.json()['data']
        i=1
        if (list):
            x = PrettyTable()
            x.field_names = ["index", "ID", "Name", "Created at", "bucket size"]
            for element in list:
                x.add_row([i, element['id'], element['name'], element['created_at'], element['bucket_size']])
                i = i+1
            Py_version_manager.py_print(x)
        else:
            Py_version_manager.py_print("Either list is empty or an error occurred!!")

    

