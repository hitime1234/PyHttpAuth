import time
from typing import Any 
class CookieJar:
    
    
    def __init__(self):
        self._cookies = {}
        self._expiry = {}

    def add_cookie(self, cookie, username):
        self.sweep()
        self._cookies[cookie] = username
        #set expiry for 24 hours in seconds
        self._expiry[cookie] = time.time() + 86400

    def get_username(self, cookie):
        self.sweep()
        hold = self._cookies.get(cookie)
        if hold:
            return hold
        else:
            return "NULL"

    def has_cookie(self, cookie):
        self.sweep()
        return cookie in self._cookies
    
    def remove_cookie(self, cookie):
        if cookie in self._cookies:
            del self._cookies[cookie]
            del self._expiry[cookie]

    def sweep(self):
        for cookie in list(self._cookies):
            if time.time() > self._expiry[cookie]:
                self.remove_cookie(cookie)

    def mainThread(self):
        while True:
            self.sweep()
            time.sleep(10)

    


