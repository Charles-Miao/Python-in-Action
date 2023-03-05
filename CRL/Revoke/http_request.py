import requests
import json

class MyAPI(object):
    def __init__(self, username, password, token_url, api_url):
        self.username = username
        self.password = password
        self.token_url = token_url
        self.api_url=api_url
        self.token = self.get_token()

    def get_token(self):
        login_data = {
            "Issuer": self.username,
            "Password": self.password
        }
        login_headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }
        login_url = self.token_url
        login_response = requests.post(login_url, data=json.dumps(login_data), headers=login_headers)
        return json.loads(login_response.text)["result"]

    def call_api(self, method="POST", data=None, headers=None):
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/json; charset=UTF-8"
        headers["Authorization"] = "Bearer " + self.token
        url = self.api_url
        response = requests.request(method, url, data=json.dumps(data), headers=headers)
        return json.loads(response.text)["result"]

    # def get_data(self, id):
    #     endpoint = "/data/" + str(id)
    #     response = self.call_api(endpoint, method="GET")
    #     return response["data"]

    # def update_data(self, id, data):
    #     endpoint = "/data/" + str(id)
    #     headers = {
    #         "Content-Type": "application/json"
    #     }
    #     response = self.call_api(endpoint, method="PUT", data=data, headers=headers)
    #     return response["updated"]

# 使用示例
# api = MyAPI("your_username", "your_password", "http://example.com")
# data = api.get_data(123)
# print(data)

# new_data = {
#     "param1": "new_value1",
#     "param2": "new_value2"
# }
# updated = api.update_data(123, new_data)
# print(updated)

if __name__=='__main__':
    api=MyAPI(
       username="CIMAPI",
       password="123456",
       token_url="http://10.66.25.118:9999/cimapi/gettoken",
       api_url="http://10.66.25.118:9999/CIMAPI/DynamicInterfaceORA"
    )
    data={"SYSTEM": "SFCFA","ACTION": "GET","FUNCTIONNAME": "FUNC_GETCAMSN","PLANT":"F232","sss":"123" }
    data["sss"]="406388710002"
    print(api.call_api(data=data))