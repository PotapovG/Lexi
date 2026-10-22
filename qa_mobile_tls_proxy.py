"""Temporary localhost HTTPS proxy for isolated mobile QA; never serves production DB."""
import http.client
import ssl
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit

class Proxy(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
    def do_GET(self):self.forward()
    def do_POST(self):self.forward()
    def forward(self):
        parts=urlsplit(self.path)
        if not parts.path.startswith('/greek/'):
            self.send_error(404);return
        local_path='/'+parts.path.removeprefix('/greek/')
        if parts.query:local_path+='?'+parts.query
        body=self.rfile.read(int(self.headers.get('Content-Length','0')))
        headers={k:v for k,v in self.headers.items()
                 if k.lower() not in ('host','connection','accept-encoding','origin')}
        headers['Origin']='https://potapovfamily.com'
        headers['Host']='127.0.0.1:18561'
        conn=http.client.HTTPConnection('127.0.0.1',18561,timeout=7)
        try:
            conn.request(self.command,local_path,body=body,headers=headers)
            response=conn.getresponse()
            content=response.read()
            self.send_response(response.status)
            for name,value in response.getheaders():
                if name.lower() in ('connection','transfer-encoding','server','date'):continue
                self.send_header(name,value)
            self.end_headers()
            self.wfile.write(content)
        finally:conn.close()

server=ThreadingHTTPServer(('127.0.0.1',18443),Proxy)
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('/tmp/lexi-mobile-cert.pem','/tmp/lexi-mobile-key.pem')
server.socket=ctx.wrap_socket(server.socket,server_side=True)
server.serve_forever()
