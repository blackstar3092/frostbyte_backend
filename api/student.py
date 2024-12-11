from flask import Blueprint
from flask_restful import Api, Resource # used for REST API building

student_api = Blueprint('student_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

class StudentAPI:        
    class _Abby(Resource): 
        def get(self):     
            InfoDb = []
            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Abby",
                "LastName": "Manalo",
                "FavoriteColor": "Purple",
                "FavoriteFruit": "Mango",
                "FavoriteSport": "Dance", 
                "Hobbies": ["Baking", "Watching Shows", "Reading", "Coloring",]
            })
            pass                                                                               
    
    class _Aranya(Resource): 
        def get(self):
            
             pass
 
 
    class _Ava(Resource): 
        def get(self):
            InfoDb = []
            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Ava",
                "LastName": "Shalon",
                "Favorite_Color": "blue",
                "Favorite_Fruit": "Avocado",
                "Email": "jmortensen@powayusd.com",
                "Hobbies": ["Watching TV", "cooking", "swimming", "going to the beach"]
            })
            pass
           
    class _Elliot(Resource):
        def get(self):
            InfoDb = []
            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Elliot",
                "LastName": "Yang",
                "Favorite_Color": "---",
                "Favorite_Fruit": "San Diego",
                "Email": "jmortensen@powayusd.com",
                "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
            })
            pass

    class _Risha(Resource): 
        def get(self):
            InfoDb = []

            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Risha",
                "LastName": "Guha",
                "FavoriteColor": "Blue",
                "FavoriteFruit": "mango",
                "FavoriteSport": "badminton", 
                "Hobbies": ["Reading", "Piano", "Cybersecurity", "Video Games", "Debate"]
            })
            pass

    class _Shriya(Resource): 
        def get(self):
            InfoDb = []

            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Shriya",
                "LastName": "Paladugu",
                "FavoriteColor": "Pink",
                "FavoriteFruit": "Orange",
                "FavoriteSport": "Basketball",
                "Hobbies": ["Basketball", "CyberSecurity", "Hanging out with friends", "", "Speech and Debate"]
            })
            pass
    
    # building RESTapi endpoint
    api.add_resource(_Abby, '/student/abby')          
    api.add_resource(_Aranya, '/student/aranya')
    api.add_resource(_Ava, '/student/ava')
    api.add_resource(_Elliot, '/student/elliot')
    api.add_resource(_Risha, '/student/risha')
    api.add_resource(_Shriya, '/student/shriya')