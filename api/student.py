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
            return InfoDb, 200
            pass                                                                               
    
    class _Aranya(Resource): 
         def get(self):     
            InfoDb = []
            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Aranya",
                "LastName": "Bhattacharya",
                "FavoriteColor": "Orange",
                "FavoriteFruit": "Mango",
                "FavoriteSport": "Boxing", 
                "Hobbies": ["Watching Movies", "Walking Dog", "Machine Learning", "Excercise",]
            })
            return InfoDb, 200
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
            return InfoDb, 200
            pass
           
    class _Elliot(Resource):
        def get(self):
            InfoDb = []
            # add a row to list, an Info record
            InfoDb.append({
                "FirstName": "Elliot",
                "LastName": "Yang",
                "Favorite_Color": "purple",
                "Favorite_Fruit": "watermelon",
                "Favorite Sport": "jmortensen@powayusd.com",
                "Hobbies": ["reading", "exercising", "going to the beach", "hiking", "singing", "playing instruments"]
            })  
            return InfoDb, 200
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
            return InfoDb, 200
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
                "Hobbies": ["Basketball", "CyberSecurity", "Hanging out with friends", "Speech and Debate"]
            })
            return InfoDb, 200
            pass
    
    # building RESTapi endpoint
    api.add_resource(_Abby, '/student/abby')          
    api.add_resource(_Aranya, '/student/aranya')
    api.add_resource(_Ava, '/student/ava')
    api.add_resource(_Elliot, '/student/elliot')
    api.add_resource(_Risha, '/student/risha')
    api.add_resource(_Shriya, '/student/shriya')