import requests
import json
import re


class SMMS(object):
    # init with username and password
    def __init__(self):
        self.baseurl="https://smms.app/api/v2/"
        self.username = None
        self.password = None
        self.token = None
        self.profile = None
        self.history = None
        self.upload_history = None
        self.url = None



    # token
    def get_api_token(self, username, password):
        self.username=username
        self.password=password
        data = {
            'username': self.username,
            'password': self.password,
        }
        url = self.baseurl+'token'
        res = requests.post(url, data=data).json()
        if res['success']==False:
            print("Sorry Login error!!!")
        else:
            self.token = res['data']['token']
            self.headers = {'Authorization': self.token}
            # print(json.dumps(res, indent=4))

    # profile
    def get_user_profile(self):
        url = self.baseurl+'profile'
        res = requests.post(url, headers=self.headers).json()
        self.profile = res['data']
        return res
        print(json.dumps(res, indent=4))

    # clear
    def clear_temporary_history(self):
        data = {
            'format': 'json'
        }
        url = self.baseurl+'clear'
        res = requests.get(url, data=data).json()
        print(json.dumps(res, indent=4))

    # history
    def view_temporary_history(self):
        url = self.baseurl+'history'
        res = requests.get(url,headers=self.headers).json()
        self.history = res['data']
        print(res)
        print(json.dumps(res, indent=4))

    # delete
    def delete_image(self, hash):
        url = self.baseurl+'delete/'+hash
        res = requests.get(url,headers=self.headers).json()
        return res['message']

    # upload_history
    def get_TotalPages(self):
        url = self.baseurl+'upload_history'
        res = requests.get(url,headers=self.headers).json()
        TotalPages=res['TotalPages']
        return TotalPages


    # upload_history
    def view_upload_history(self,page):
        page=int(page)
        url = self.baseurl+'upload_history'
        payload = {'page': page}
        res = requests.get(url,params=payload,headers=self.headers).json()
        self.upload_history = res['data']
        #print(json.dumps(res, indent=4))
        return self.upload_history

    # upload
    def upload_image(self, path):
        try:
            files = {'smfile': open(path, 'rb')}
            url = self.baseurl+'upload'
            res = requests.post(url, files=files, headers=self.headers).json()
            if res['success']:
                self.url = res['data']['url']
                # print(json.dumps(res, indent=4))
                return self.url
                # upload repeated， get the url
            elif 'Image upload repeated' in res['message']:
                self.url = re.findall('(http.*\.(?:jpg|jpeg|png|webp|gif))', res['message'])[0]
                return self.url
            else:
                return None
        except Exception as e:
            print(e)


# if __name__ == "__main__":
#     root = 'https://sm.ms/api/v2/'
#     smms = SMMS('username', 'password')
#     smms.get_api_token()
#     smms.upload_image('xx.jpg')