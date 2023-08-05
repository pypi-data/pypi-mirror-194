
import datetime
from typing import List,Callable
import requests
import hashlib
import sys
import asyncio
from dataclasses import dataclass
from threading import Thread
from PIL import Image
import numpy as np
from queue import SimpleQueue
import io

import time




def image_to_byte_array(image: Image.Image) -> str:
  # BytesIO is a fake file stored in memory
    mem_file = io.BytesIO()
    image = image.resize((512,512))
    image.save(mem_file, "PNG", quality=100)
    return list(bytearray(mem_file.getvalue()))

def buttons_transform(buttons):
    requestedButtons = []
    actual_buttons = []
    for row in buttons:
        rowButtons = []
        for column in row:
            
            
            rowButtons.append({
                "callback_name":column.callback.__name__,
                "text":column.text
            })
            actual_buttons.append(column)
            
        requestedButtons.append(rowButtons)
    return requestedButtons,actual_buttons



alive_messages = []

class InternalPytificationsQueuedTask:
    def __init__(self,function,extra_functions: list,args:tuple) -> None:
        self._function = function
        self._extra_functions = extra_functions
        self._args = args
    
    def evaluate(self):
        self._function(*self._args)
        for queued_task in self._extra_functions:
            queued_task.evaluate()


@dataclass
class PytificationButton:
    text: str
    callback: Callable

class PytificationsMessageWithPhoto:
    def __init__(self,message_id,image = None):
        self._image = image

        self._message_id = message_id
        alive_messages.append(self)
    def __del__(self):
        if self in alive_messages:
            alive_messages.remove(self)

    

    def edit(self,text: str = "",buttons: List[List[PytificationButton]] =[],photo: Image.Image = None): 
        """
        Method to edit this message in Telegram

        if only the buttons are passed, the text will be kept the same

        if no photo is passed, the old one will be kept
        
        Args:
            text: (:obj:`str`) message to send instead
            buttons: (:obj:`List[List[PytificationButton]]`) a list of rows each with a list of columns in that row to be used to align the buttons
            photo: (:obj:`PIL.Image`) an image if you wish to change it
        Returns:
            :obj:`True` if change added to the editing queue and :obj:`False` if an error was found
        """


        if not Pytifications._check_login() or self._message_id == -1:
            return False
        
        
        if isinstance(self._message_id,InternalPytificationsQueuedTask):
            self._message_id._extra_functions.append(InternalPytificationsQueuedTask(self.edit,[],[self,text,buttons,photo]))
            return True

        text = Pytifications._options.format_string(text)
        buttons,buttons_list = buttons_transform(buttons)
        for button in buttons_list:
            Pytifications._registered_callbacks[button.callback.__name__] = {"function":button.callback,"args":[self]}
        

        request_data = {
            "username":Pytifications._login,
            "password_hash":hashlib.sha256(Pytifications._password.encode('utf-8')).hexdigest(),
            "message_id":self._message_id,
            "buttons":buttons,
            "process_id":Pytifications._process_id
        }

        if photo != None:
            request_data['photo'] = image_to_byte_array(photo)
            self._image = photo
        else:
            request_data['photo'] = image_to_byte_array(self._image)
        
        if text != "": 
            request_data["message"] = text
        
        Pytifications._add_to_message_pool(edit_message,request_data,self)
        
        return True



class PytificationsMessage:
    def __init__(self,message_id):

        self._message_id = message_id
        alive_messages.append(self)
    def __del__(self):
        if self in alive_messages:
            alive_messages.remove(self)

    

    def edit(self,text: str = "",buttons: List[List[PytificationButton]] =[]): 
        """
        Method to edit this message in Telegram

        if only the buttons are passed, the text will be kept the same

        Args:
            text: (:obj:`str`) message to send instead
            buttons: (:obj:`List[List[PytificationButton]]`) a list of rows each with a list of columns in that row to be used to align the buttons
        Returns:
            :obj:`True` if change added to the editing queue and :obj:`False` if an error ocurred
        """


        if not Pytifications._check_login() or self._message_id == -1:
            return False
        
        if isinstance(self._message_id,InternalPytificationsQueuedTask):
            self._message_id._extra_functions.append(InternalPytificationsQueuedTask(self.edit,[],[self,text,buttons]))
            return True

        text = Pytifications._options.format_string(text)
        buttons,buttons_list = buttons_transform(buttons)
        for button in buttons_list:
            Pytifications._registered_callbacks[button.callback.__name__] = {"function":button.callback,"args":[self]}
        

        request_data = {
            "username":Pytifications._login,
            "password_hash":hashlib.sha256(Pytifications._password.encode('utf-8')).hexdigest(),
            "message_id":self._message_id,
            "buttons":buttons,
            "process_id":Pytifications._process_id
        }

        

        if text != "":
            request_data["message"] = text
        
        
        
        Pytifications._add_to_message_pool(edit_message,request_data,self)
        
        return True



class PytificationsRemoteController:
    def __init__(self,name) -> None:
        pass

    

def update_message_id(old_message_id,new_message_id):
    for i in alive_messages:
        if int(i._message_id) == int(old_message_id):
            i._message_id = (str(new_message_id))

def datetime_diff(diff: datetime.timedelta):
    format = "%H:%M:%S"
    if diff > datetime.timedelta(hours=24):
        format = f'%j {"days" if diff > datetime.timedelta(hours=48) else "day"} %H:%M:%S'
        diff -= datetime.timedelta(hours=24)
    diff = diff + datetime.timedelta(hours=3)
    return datetime.datetime.fromtimestamp(diff.total_seconds()).strftime(format)

class PytificationsOptions:
    _start_time = datetime.datetime.now()
    def __init__(self,send_current_time_on_message=False,send_app_run_time_on_message = False,script_alias = "") -> None:
        """
        Data class for the options in Pytifications

        Args:
            send_app_run_time_on_message: (:obj:`bool`) whether to send the current app runtime on the bottom of messages sent and edits
            send_current_time_on_message: (:obj:`bool`) whether to send the current time on the bottom of messages sent and edited
            script_alias: (:obj:`str`) alias to use when sending the message. Will appear on the top of the messages as "Message sent from __alias_here__:" 
        """
        
        self._send_app_run_time_on_message = send_app_run_time_on_message
        self._script_alias = script_alias
        self._send_current_time_on_message = send_current_time_on_message
        
    

    def format_string(self,string):
        if self._send_app_run_time_on_message or self._send_current_time_on_message:
            string = f'{string}\n'
        if self._send_app_run_time_on_message:
            string = f'{string}\nrun_time:\n{datetime_diff(datetime.datetime.now() - PytificationsOptions._start_time)}'
        if self._send_current_time_on_message:
            string = f'{string}\ncurrent_time:\n{datetime.datetime.now().strftime("%H:%M:%S")}'

        if self._script_alias != "":
            string = f'Message sent from "{self._script_alias}":\n\n{string}'
        
        return string

def send_message(request_data,photo: Image,return_data: PytificationsMessage | PytificationsMessageWithPhoto):
    try:
        res = requests.post('https://pytifications.herokuapp.com/send_message',json=request_data)
    except Exception as e:
        print(f"Found error when sending message: {e}")
        return False
    

    if res.status_code != 200:
        print(f'could not send message. reason: {res.reason}')
        return False

    Pytifications._last_message_id = int(res.text)

    
    return_data._message_id = int(res.text)
    if photo != None:
        print(f'sent message with photo: "{request_data["message"]}"')
        return_data._image = photo

    else:
        print(f'sent message: "{request_data["message"]}"')

def edit_message(request_data,return_data: PytificationsMessage | PytificationsMessageWithPhoto):

    
    try:     
        requests.patch('https://pytifications.herokuapp.com/edit_message',json=request_data)
    except Exception as e:
        print(f'Found exception while editing message: {e}')
        return False

    print(f'edited message with id {return_data._message_id} to "{request_data["message"]}"')   

class Pytifications:
    _login = None
    _logged_in = False
    _password = None
    _loop = None
    _registered_callbacks = {
        "__set_message_id":{"function":lambda *args: Pytifications._add_to_message_pool(update_message_id,*args),"args":[]}
    }
    _message_pool: SimpleQueue[InternalPytificationsQueuedTask] = SimpleQueue()
    _last_message_id = 0
    _process_id = 0
    _callbacks_to_call_synchronous = []
    _synchronous = False
    _options = PytificationsOptions()

    @staticmethod
    def _add_to_message_pool(function,*args):
        task = InternalPytificationsQueuedTask(function,[],args)
        Pytifications._message_pool.put(task)

        return task

    @staticmethod
    def run_callbacks_sync():
        """
        Use this method to run all the callbacks that were registered to be called since last time you called this function or started the process
        
        Returns:
            :obj:`True` if any callbacks where called, :obj:`False` otherwise
        """
        
        called_any = False
        for callback in Pytifications._callbacks_to_call_synchronous:
            called_any = True
            callback["function"](*callback["args"])
        Pytifications._callbacks_to_call_synchronous.clear()

        return called_any
    
    @staticmethod
    def set_options(options: PytificationsOptions):
        """
        Sets the options to use during the script operation,
        
        for more information on the available options check :obj:`PytificationsOptions`
        """
        Pytifications._options = options
    
    @staticmethod
    def set_synchronous():
        """
        Use this method to set the callbacks registered in buttons to be called synchronously*
        
        *when you call the function Pytifications.run_callbacks_sync()
        """

        Pytifications._synchronous = True

    @staticmethod
    def set_asynchronous():
        """
        Use this method to set the callbacks registered in buttons to be called asynchronously whenever the process receives the request to call them

        This is the default option
        """
        Pytifications._synchronous = False
    
    @staticmethod
    def login(login:str,password:str) -> bool:
        """
        Use this method to login to the pytifications network,

        if you don't have a login yet, go to https://t.me/pytificator_bot and talk to the bot to create your account

        Args:
            login (:obj:`str`) your login credentials created at the bot
            password (:obj:`str`) your password created at the bot

        Returns:
            :obj:`True`if login was successful else :obj:`False`
        """

        Pytifications._logged_in = False

        try:
            res = requests.post('https://pytifications.herokuapp.com/initialize_script',json={
                "username":login,
                "password_hash":hashlib.sha256(password.encode('utf-8')).hexdigest(),
                "process_name":sys.argv[0],
                "process_language":'python'
            })
        except Exception as e:
            print(f'Found exception while logging in: {e}')
            return False
        
        Pytifications._login = login
        Pytifications._password = password
        if res.status_code != 200:
            print(f'could not login... reason: {res.text}')
            return False
        else:
            Pytifications._logged_in = True
            Pytifications._process_id = res.text
            print(f'success logging in to pytifications! script id = {Pytifications._process_id}')

        Thread(target=Pytifications._check_if_any_callbacks_to_be_called,daemon=True).start()
        
        return True

    
    @staticmethod
    def _check_if_any_callbacks_to_be_called():
        while True:
            time.sleep(0.5)
            if not Pytifications.am_i_logged_in():
                continue
            
            try:
                while not Pytifications._message_pool.empty():
                    Pytifications._message_pool.get().evaluate()
                    
            except Exception as e:
                print(f'Error found while updating message pool, please report to the developer! {e}')
                pass

            time.sleep(2)
            try:
                res = requests.get('https://pytifications.herokuapp.com/get_callbacks',json={
                    "username":Pytifications._login,
                    "password_hash":hashlib.sha256(Pytifications._password.encode('utf-8')).hexdigest(),
                    "process_id":Pytifications._process_id
                })
            except Exception as e:
                print(f'Error found while requesting to get callbacks, please contact the developer! {e}')
                continue
            if res.status_code == 200:
                json = res.json()
                for item in json:
                    if Pytifications._synchronous:
                        Pytifications._callbacks_to_call_synchronous.append({
                            "function":Pytifications._registered_callbacks[item["function"]]["function"],
                            "args":(Pytifications._registered_callbacks[item['function']]['args'] + item["args"])
                        })
                    else:
                        Pytifications._registered_callbacks[item["function"]]["function"](*(Pytifications._registered_callbacks[item['function']]['args'] + item["args"]))





    @staticmethod
    def send_message(message: str,buttons: List[List[PytificationButton]] = [],photo : Image.Image=None):
        """
        Use this method to send a message to yourself/your group,

        make sure to have called Pytifications.login() before,


        Args:
            message: (:obj:`str`) message to be sent
            buttons: (:obj:`List[List[PytificationButton]]`) a list of rows each with a list of columns in that row to be used to align the buttons
            photo: (:obj:`PIL.Image`) an image if you wish to send it
        Return:
            False if any errors ocurred, :obj:`PytificationsMessage` if photo is not specified and :obj:`PytificationsMessageWithPhoto` if photo is specified
        """
        message = Pytifications._options.format_string(message)

        if not Pytifications._check_login():
            return False

        return_data = PytificationsMessage(-1)

        if photo != None:
            return_data = PytificationsMessageWithPhoto(-1)

        buttons,buttons_list = buttons_transform(buttons)
        for button in buttons_list:
            Pytifications._registered_callbacks[button.callback.__name__] = {"function":button.callback,"args":[return_data]}
        

        request_data = {
                "username":Pytifications._login,
                "password_hash":hashlib.sha256(Pytifications._password.encode('utf-8')).hexdigest(),
                "message":message,
                "buttons":buttons,
                "process_id":Pytifications._process_id
        }

        if photo != None:
            request_data['photo'] = image_to_byte_array(photo)

        task = Pytifications._add_to_message_pool(send_message,request_data,photo,return_data)
        return_data._message_id = task

        return return_data

    @staticmethod
    def __edit_last_message(message_return: PytificationsMessage | PytificationsMessageWithPhoto,message:str = "",buttons: List[List[PytificationButton]] = []):
        message = Pytifications._options.format_string(message)
        


        buttons,buttons_list = buttons_transform(buttons)
        for button in buttons_list:
            Pytifications._registered_callbacks[button.callback.__name__] = {"function":button.callback,"args":[message_return]}
        
        request_data = {
            "username":Pytifications._login,
            "password_hash":hashlib.sha256(Pytifications._password.encode('utf-8')).hexdigest(),
            "message_id":Pytifications._last_message_id,
            "buttons":buttons,
            "process_id":Pytifications._process_id
        }

        

        if message != "":
            request_data["message"] = message

        task = Pytifications._add_to_message_pool(edit_message,request_data,message_return)
        message_return._message_id = task
        

    @staticmethod
    def edit_last_message(message:str = "",buttons: List[List[PytificationButton]] = []):
        """
        Use this method to edit the last sent message from this script

        if only the buttons are passed, the text will be kept the same

        Args:
            message: (:obj:`str`) message to be sent
            buttons: (:obj:`List[List[PytificationButton]]`) a list of rows each with a list of columns in that row to be used to align the buttons
        Returns:
            :obj:`PytificationsMessage` message object that can be further edited if needed
        """
        if not Pytifications._check_login():
            return False
        
        message_return = PytificationsMessage()
        task = Pytifications._add_to_message_pool(Pytifications.__edit_last_message,message_return,message,buttons)
        message_return._message_id = task
        

        return message_return
        
    @staticmethod
    def _check_login():
        if not Pytifications._logged_in:
            print('could not send pynotification, make sure you have called Pytifications.login("username","password")')
            return False
        return True

    @staticmethod
    def am_i_logged_in():
        """
        Checks if already logged in
        """
        return Pytifications._logged_in
    
    @staticmethod
    def enable_remote_control(name):
        """
        EXPERIMENTAL: DO NOT USE
        """
        return PytificationsRemoteController(name)