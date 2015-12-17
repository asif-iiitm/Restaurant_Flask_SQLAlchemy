from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        restaurants = session.query(Restaurant).all()
        try:
            if self.path.endswith("/restaurants"):
                output = ""
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href =' %s/edit' >Edit </a> " % restaurant.id
                    output += "</br>"
                    output += "<a href =' %s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br></br>"
                
                output += "<a href = /new > Make a New Restaurant Here </a>"
                output += "</body></html>"
                self.wfile.write(output)

                return
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new' >"
                output += "<input name= 'newRestaurantName' type='text' placeholder = 'New Resaurant Name' >" 
                output += "<input type= 'submit' value='Rename'>"
                output += "</html></body>"
                self.wfile.write(output)



            if self.path.endswith("/edit"):
               
                restaurantIDPath =  self.path.split("/")[1]
                
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one() 
                if myRestaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type',    'text/html')
                    self.end_headers()
                    output = ""
                    output += myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name= 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type= 'submit' value='Rename'>"
                    output += "</form>"

                    self.wfile.write(output)
                else:
                    print "empty query!"

            if self.path.endswith("/delete"):

               
                restaurantIDPath =  self.path.split("/")[1]
                
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one() 
                if myRestaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type',    'text/html')
                    self.end_headers()
                    output = ""
                    output = "<html><body>"
                    output = "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete' >" % restaurantIDPath
                    output += "<input type= 'submit' value='Delete'>"
                    output += "</form>"

                    self.wfile.write(output)

                    
                return

            
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        #global rootnode
        try:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    query=cgi.parse_multipart(self.rfile, pdict)
                upfilecontent = query.get('newRestaurantName')
               
                newRestaurant = Restaurant(name = upfilecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type',    'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    query=cgi.parse_multipart(self.rfile, pdict)
                upfilecontent = query.get('newRestaurantName')
               
                restaurantPath =  self.path.split("/")[2]
                print restaurantPath
                myRestaurant = urllib2.unquote(restaurantPath)
                myRestaurantQuery = session.query(Restaurant).filter_by(id = myRestaurant).one() 
                if myRestaurantQuery != [] :
                    myRestaurantQuery.name = upfilecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type',    'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

             
                
            
                
            if self.path.endswith("/delete"):
                print "In delete block"
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                
                restaurantPath =  self.path.split("/")[2]
                print restaurantPath
                myRestaurant = urllib2.unquote(restaurantPath)
                myRestaurantQuery = session.query(Restaurant).filter_by(id = myRestaurant).one() 
                print "made it here"

                if myRestaurantQuery != [] :
                    print "inside the if statement"
                    session.delete(myRestaurantQuery)
                    print "deleting %s" % myRestaurantQuery.name
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type',    'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'Web server running...open localhost:8080/restaurants in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()