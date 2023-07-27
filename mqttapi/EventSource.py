from flask import Flask,Response,Blueprint
from flask_cors import CORS

class ServerSideEvents:
    def __init__(self,app_name = __name__):
        self.app_name = app_name
        self.app = Flask(app_name)
        self.configureEventSource()
        
    def configureEventSource(self,port=5000,debug=True):
        self.port = port
        self.debug = debug
        CORS(self.app)
        
    def createBlueprint(self,name):
        name = Blueprint(name,self.app_name)
        return name
    
    def associateRoutesBlueprint(self,BlueprintName,route_name,function):
        @BlueprintName.route(f'/{route_name}')
        def route_function():
            return function()
        
    def start_server(self):
        self.app.run()
    
    def createRoute(self,route_name,function):
        @self.app.route(f'/{route_name}')
        def route_function():
            return function()
    
    
    
    
        