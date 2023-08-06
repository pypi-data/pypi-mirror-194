from typing import NewType

def quicktext():
    print('Hello, welcome to QuickSample package.')


class ShorthandValue:
    def __init__(self, topic_id):
        self.__topic_id = topic_id
        return
    
    def id(self):
        return self.__topic_id
    
    def value(self):
        return
    
    def info(self):
        return

class ShorthandAI:
    def __init__(self, token: str):
        self.__token = token
        return
    
    def value(
            self, 
            topic_id
            ):
        return ShorthandValue(topic_id)
    
    def get(
            self, 
            topic_id, 
            tag="latest",
            take_header=True,
            ):
        pass

    def hget(self, topic_id, since=None):
        pass
    
    def set(
            self, 
            topic_id, 
            value,
            tag=None
            ):
        
        tag_name = None if (tag == 'latest') else tag

        pass

    def info(self):
        pass