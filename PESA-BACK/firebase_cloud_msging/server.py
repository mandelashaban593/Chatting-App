from pyfcm import FCMNotification

import remitapi.settings as settings


class FirebaseCloudMessaging():
    """Firebase push notifications"""

    def __init__(self):
        self.push_service = False

    #notify single device
    def single_device(self,**kwargs):
        registration_id = kwargs['registration_id']
        message_title = kwargs['message_title']
        message_body = kwargs['message_body']
        api_key = kwargs['api_key']
        data_message = kwargs.get('data_message','')
        result = False

        self.init_push_service(api_key)

        if data_message:
            import json
            json_acceptable_string = data_message.replace("'", "\"")
            data_message = json.loads(json_acceptable_string)
            result = self.push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body,data_message=data_message)
        else:

            result = self.push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        return result

    #notify multiple devices.supply registration id's in a list
    def multiple_devices(self,registration_ids,data_msg=None, **kwargs):
        message_title = kwargs['message_title']
        message_body = kwargs['message_body']
        api_key = kwargs['api_key']

        self.init_push_service(api_key)

        result = self.push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

        return result

    #create FCMNotification instance
    def init_push_service(self,api_key):
        self.push_service = FCMNotification(api_key=api_key)
        #return FCMNotification(api_key=self.api_key)
