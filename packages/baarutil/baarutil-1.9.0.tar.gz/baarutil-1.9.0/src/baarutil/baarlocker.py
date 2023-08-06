# -- coding: ISO-8859-2 --

import requests
import json
import os
import traceback


class BaarLocker:
    """This class contains all the functionalities to interact with BAARLocker APIs and performs operations like -
    Encrypt, Decrypt, Update and Delete"""
    def __init__(self, tenant: str, api_key: str, username: str, env_var: str ='BAAR_PATH', custom_url_dict: dict ={}):
        self.tenant = tenant
        self.api_key = api_key
        self.username = username
        self.env_var = env_var
        self.custom_url_dict = custom_url_dict
        self.service_url = self.get_service_url()
        self.url_dict = {
            'update_url': r'__SERVICE_URL__/rest/admin/UpdatePrisonBaar/1?tenant=__TENANT__',
            'create_url': r'__SERVICE_URL__/rest/admin/CreatePrisonBaar/1?tenant=__TENANT__',
            'get_url': r'__SERVICE_URL__/rest/admin/GetPrisonBaar/1?tenant=__TENANT__',
            'delete_url': r'__SERVICE_URL__/rest/admin/DeletePrisonBaar/1/?tenant=__TENANT__'
        }
        for key in self.url_dict:
            self.url_dict[key] = self.url_dict.get(key, '').replace('__SERVICE_URL__', self.service_url).replace(
                '__TENANT__', self.tenant)

    def get_specific_url(self, url_type):
        # This function will filter the exact url based on the url_type from the self.url_dict
        final_url = ''
        if url_type in self.url_dict.keys():
            if len(self.custom_url_dict) == 0:
                main_url_dict = self.url_dict
                final_url = main_url_dict.get(url_type, '')
            else:
                main_url_dict = self.custom_url_dict
                final_url = main_url_dict.get(url_type, '')
        else:
            print(f'''Configuration: custom_url_dict is missing required field "{url_type}"
            to perform the required operation.''', flush=True)
        return final_url

    def path_fetcher(self):
        # This function will fetch the Baar installation path from environment variables
        file_path = os.getenv(self.env_var)
        return file_path

    def get_service_url(self):
        # This function will automatically fetch the service url from the BAAR Properties files
        service_url = ''
        path = self.path_fetcher()
        if os.path.isdir(path):
            config_path = os.path.join(path, r'studio\config\studio-web.properties')
            if os.path.isfile(config_path):
                with open(config_path, 'r') as text_file:
                    for line in text_file:
                        if str(line).strip() != '' and str(line).strip() != '\n':
                            if 'service.url=' in line:
                                service_url = line.split('service.url=')[1].replace('\n', '')
                if service_url == '':
                    print('Service URL Not Found!', flush=True)
            else:
                print('Config File does not exist.', flush=True)
        else:
            print(f'BAAR Studio Installation Path not found - {path}', flush=True)
        return service_url

    def verify_response(self, response):
        # This function will verify the responses received from API Communication
        good_response = False
        response_dict = {}
        if response:
            response_dict = json.loads(response.text)
            status_code = response_dict.get('statusCode', 0)
            message = response_dict.get('message', '')
            if status_code == 200 and 'successful' in str(message).lower().strip():
                good_response = True
            else:
                good_response = False
                print('Unable to connect to server!', flush=False)
        else:
            print('Unable to connect to server!', flush=False)
        return good_response, response_dict

    def encrypt(self, data: str):
        # This function will encrypt the provided data using BAARLocker API
        url = self.get_specific_url('create_url')
        final_unique_id = ''
        detailed_message = ''
        operation_status = False
        payload = json.dumps({
            "id": "",
            "refId": "",
            "uniqueId": "",
            "data": "",
            "password": data,
            "message": "",
            "statusCode": ""
        })
        headers = {
            'username': self.username,
            'API-KEY': self.api_key,
            'X-NO-LOGIN-MODE': '',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            good_response, response_dict = self.verify_response(response)
            if response and good_response:
                detailed_message = response_dict.get('message', '')
                unique_id = response_dict.get('uniqueId', '')
                if unique_id != '':
                    final_unique_id = unique_id
                    operation_status = True
                else:
                    print('Encryption Failed. Unique ID is empty!', flush=True)
                    detailed_message = response.text
            else:
                print('Encryption Failed!', flush=True)
                detailed_message = response.text
        except Exception as e:
            print('Encryption Failed!', flush=True)
            print(traceback.format_exc(), flush=True)
            detailed_message = 'Unable to connect to server and execute operation.'
        return final_unique_id, operation_status, detailed_message

    def decrypt(self, id):
        # This function will decrypt the provided id using BAARLocker API
        url = self.get_specific_url('get_url')
        final_data = ''
        detailed_message = ''
        operation_status = False
        payload = json.dumps({
            "id": "",
            "refId": "",
            "uniqueId": id,
            "data": "",
            "password": "",
            "message": "",
            "statusCode": ""
        })
        headers = {
            'username': self.username,
            'API-KEY': self.api_key,
            'X-NO-LOGIN-MODE': '',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            good_response, response_dict = self.verify_response(response)
            if response and good_response:
                detailed_message = response_dict.get('message', '')
                decrypted_data = response_dict.get('password', '')
                if decrypted_data != '':
                    final_data = decrypted_data
                    operation_status = True
                else:
                    print('Decryption Failed. Decrypted data is empty!', flush=True)
                    detailed_message = response.text
            else:
                print('Decryption Failed!', flush=True)
                detailed_message = response.text
        except Exception as e:
            print('Decryption Failed!', flush=True)
            print(traceback.format_exc(), flush=True)
            detailed_message = 'Unable to connect to server and execute decryption operation.'
        return final_data, operation_status, detailed_message

    def update(self, id, data):
        # This function will Update the provided data against the provided if using BAARLocker API
        url = self.get_specific_url('update_url')
        final_unique_id = ''
        detailed_message = ''
        operation_status = False
        payload = json.dumps({
            "id": "",
            "refId": "",
            "uniqueId": id,
            "data": "",
            "password": data,
            "message": "",
            "statusCode": ""
        })
        headers = {
            'username': self.username,
            'API-KEY': self.api_key,
            'X-NO-LOGIN-MODE': '',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("PUT", url, headers=headers, data=payload)
            good_response, response_dict = self.verify_response(response)
            if response and good_response:
                detailed_message = response_dict.get('message', '')
                unique_id = response_dict.get('uniqueId', '')
                if unique_id != '':
                    final_unique_id = unique_id
                    operation_status = True
                else:
                    print('Update Failed. Unique ID is empty!', flush=True)
                    detailed_message = response.text
            else:
                print('Update Failed!', flush=True)
                detailed_message = response.text
        except Exception as e:
            print('Update Failed!', flush=True)
            print(traceback.format_exc(), flush=True)
            detailed_message = 'Unable to connect to server and execute update operation.'
        return final_unique_id, operation_status, detailed_message

    def delete(self, id):
        # This function will delete the provided id using BAARLocker API
        url = self.get_specific_url('delete_url')
        detailed_message = ''
        final_unique_id = id
        operation_status = False
        payload = json.dumps({
            "id": "",
            "refId": "",
            "uniqueId": id,
            "data": "",
            "password": "",
            "message": "",
            "statusCode": ""
        })
        headers = {
            'username': self.username,
            'API-KEY': self.api_key,
            'X-NO-LOGIN-MODE': '',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("DELETE", url, headers=headers, data=payload)
            good_response, response_dict = self.verify_response(response)
            if response and good_response:
                detailed_message = response_dict.get('message', '')
                operation_status = True
            else:
                print('Deletion Failed!', flush=True)
                detailed_message = response.text
        except Exception as e:
            print('Deletion Failed!', flush=True)
            print(traceback.format_exc(), flush=True)
            detailed_message = 'Unable to connect to server and execute deletion operation.'
        return final_unique_id, operation_status, detailed_message
