import json
import requests
import time

class TestBotCommands():
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        self._sent_mesage_id = 0

        channel_id = "1090771155163549796"
        self._url = f"https://discordapp.com/api/channels/{channel_id}/messages"
    
        self._headers = { 
            "authorization": f'Bot {TOKEN}',
            "Content-Type":"application/json"
        }

    def send_message(self, message):
        '''
        Sends message to testingbot channel
        '''
        data = {'content' : message}
        r = requests.post(self._url, headers=self._headers, data=json.dumps(data))
        if r.status_code == 200:
            data = json.loads(r.text)
            self._sent_mesage_id = data['id']
        else:
            raise Exception(f"could not send message: {r.text}")

    def read_reply(self):
        '''
        Get the message sent after the last message sent by this class.
        Will timeout and raise Exception if there has been no reply for a while
        '''
        last_message = self.read_last_message()

        if self._sent_mesage_id:
            i = 0
            while last_message['id'] == self._sent_mesage_id:
                time.sleep(0.15)
                last_message = self.read_last_message()
                i += 1
                if i > 5:
                    raise Exception("Reply time limit exceeded")
                
        return last_message


    def read_last_message(self):
        '''
        Get the last message sent to the testingbot channel
        '''
        r = requests.get(self._url, headers=self._headers)

        if r.status_code == 200:
            return json.loads(r.text)[0]
        else:
            raise Exception(f"Could not read message: {r.text}")
