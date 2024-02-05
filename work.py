from http.server import HTTPServer, BaseHTTPRequestHandler
import json 
from hashlib import sha256
import random,string

global cookieJar
global UserList
UserList = {'admin':'admin', 'user':'user', 'guest':'guest'}
cookieJar = {}


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




class RequestHandler(BaseHTTPRequestHandler):

    def sendPageHeaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def sendIconHeaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/x-icon')
        self.end_headers()

    def do_GET(self):
        global cookieJar
        cookie = self.headers.get('Cookie')
        admin = False
        if cookie:
            try:
                if cookie.split("=")[1] in cookieJar:                    
                    admin = True
                    USERNAME = cookieJar[cookie.split("=")[1]]
                else:
                    admin = False
                    USERNAME = "NULL"
            except Exception as e:
              admin = False
        
        if self.path == "/":
            self.sendPageHeaders() 
            self.wfile.write(bytes(open("index.html", "r").read(), "utf8"))
        elif self.path == "/login":
            self.sendPageHeaders() 
            self.wfile.write(bytes(open("loginpage.html", "r").read(), "utf8"))
        elif self.path == "/profile":
            self.sendPageHeaders()
            if admin:
                self.wfile.write(bytes(open("success.html", "r").read().replace("{*USERNAME*}",USERNAME), "utf8"))
            else:
                self.wfile.write(bytes(open("nologin.html", "r").read(), "utf8"))
        else:
            self.wfile.write(bytes("This is not the page you're looking for", "utf8"))
    
    def Auth(self, postJson):
        username=postJson['username']
        password=postJson['password']
        auth = False
        passer = sha256(id_generator().encode('utf-8')).hexdigest() 
        if username in UserList:
            if UserList[username] == password:
                passer = passer
                cookieJar[passer] = username
                auth = True

        reply = str("auth" + "=" + passer + ';' +"same-site=strict" + ";" + "secure" + ";" + "httponly" + ";" + "samesite=strict" + ";" + "path=/")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header("set-cookie", reply)
        self.end_headers()
        if auth:
            self.wfile.write(bytes("Login Successful", "utf8"))
        else:
            self.wfile.write(bytes("Login Failed", "utf8"))
        


    def do_POST(self):         
        global cookieJar, UserList          
        content_length = int(self.headers['Content-Length']) # Gets the size of data
        post_data = self.rfile.read(content_length) # Gets the data itself
        postJson = json.loads(post_data.decode('utf-8'))
        print(postJson)
        RequestType = postJson['type']
        if RequestType == "AUTHENTICATE":
            self.Auth(postJson)
        


def main():
    port = 80
    server_address = ('', port)
    server = HTTPServer(server_address, RequestHandler)
    print('Server running on port %s' % port)
    server.serve_forever()




if  __name__ == '__main__':
    main()

