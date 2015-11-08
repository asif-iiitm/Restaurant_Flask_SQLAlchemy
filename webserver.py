from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import cgi
class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello!</body></html>"
            self.wfile.write(message)
            print message
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile , pdict)
                messagecontent = fields.get('message')

            output = ""
            output+="<html><body>"
            output+="<h2> okay , </h2>"
            output+= "<h1> %s </h1>" % messagecontent[0]
        except:



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
