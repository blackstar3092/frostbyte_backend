from flask import Flask, jsonify 
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/data')
def get_data():
    # start a list, to be used like a information database
    InfoDb = []
    # add a row to list, an Info record
    InfoDb.append({
            "FirstName": "Ava",
            "LastName": "Shalon",
            "Favorite_Color": "blue",
            "Favorite_Fruit": "Avocado",
            "Hobbies": ["Watching TV", "cooking", "swimming", "going to the beach"]
            })

    # add a row to list, an Info record
    InfoDb.append({
            "FirstName": "Elliot",
            "LastName": "Yang",
            "Favorite_Color": "purple",
            "Favorite_Fruit": "watermelon",
            "Favorite Sport": "jmortensen@powayusd.com",
            "Hobbies": ["reading", "exercising", "going to the beach", "hiking", "singing", "playing instruments"]
            })  
    
    InfoDb.append({
            "FirstName": "Risha",
            "LastName": "Guha",
            "FavoriteColor": "Blue",
            "FavoriteFruit": "mango",
            "FavoriteSport": "badminton", 
            "Hobbies": ["Reading", "Piano", "Cybersecurity", "Video Games", "Debate"]
            })
    
    InfoDb.append({
            "FirstName": "Shriya",
            "LastName": "Paladugu",
            "FavoriteColor": "Pink",
            "FavoriteFruit": "Orange",
            "FavoriteSport": "Basketball",
            "Hobbies": ["Basketball", "CyberSecurity", "Hanging out with friends", "", "Speech and Debate"]
            })
    
    InfoDb.append({
            "FirstName": "Abby",
            "LastName": "Manalo",
            "FavoriteColor": "Purple",
            "FavoriteFruit": "Mango",
            "FavoriteSport": "Dance", 
            "Hobbies": ["Baking", "Watching Shows", "Reading", "Coloring",]
            })
    
    InfoDb.append({
            "FirstName": "Aranya",
            "LastName": "Bhattacharya",
            "FavoriteColor": "Orange",
            "FavoriteFruit": "Mango",
            "FavoriteSport": "Boxing", 
            "Hobbies": ["Watching Movies", "Walking Dog", "Machine Learning", "Excercise",]
            })
    
    

    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)