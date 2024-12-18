# model/somemodel.py
class AboutModel:
    def __init__(self):
        self.InfoDb = [
            {
                "FirstName": "Abby",
                "LastName": "Manalo",
                "FavoriteColor": "Purple",
                "FavoriteFruit": "Mango",
                "FavoriteSport": "Dance",
                "Hobbies": ["Baking", "Watching Shows", "Reading", "Coloring"],
            },
            {
                "FirstName": "Aranya",
                "LastName": "Bhattacharya",
                "FavoriteColor": "Orange",
                "FavoriteFruit": "Mango",
                "FavoriteSport": "Boxing",
                "Hobbies": ["Watching Movies", "Walking Dog", "Machine Learning", "Exercise"],
            },
            {
                "FirstName": "Ava",
                "LastName": "Shalon",
                "FavoriteColor": "blue",
                "FavoriteFruit": "Avocado",
                "FavoriteSport": "none",
                "Hobbies": ["Watching TV",  "Cooking",  "Swimming",  "Going to the beach"]
            },
            {
                "FirstName": "Elliot",
                "LastName": "Yang",
                "FavoriteColor": "purple",
                "FavoriteFruit": "watermelon",
                "FavoriteSport": "none",
                "Hobbies": ["Reading",  "Exercising",  "Going to the beach",  "Hiking",  "Singing",  "Playing instruments"]
            },
            {
                "FirstName": "Risha",
                "LastName": "Guha",
                "FavoriteColor": "Blue",
                "FavoriteFruit": "mango",
                "FavoriteSport": "badminton", 
                "Hobbies": ["Reading",  "Piano",  "Cybersecurity",  "Video Games",  "Debate"]
            },
            {
                "FirstName": "Shriya",
                "LastName": "Paladugu",
                "FavoriteColor": "Pink",
                "FavoriteFruit": "Orange",
                "FavoriteSport": "Basketball",
                "Hobbies": ["Basketball",  "CyberSecurity",  "Hanging out with friends",  "Speech and Debate"]
            }
        ]

    def get_all(self):
        """Returns all records."""
        return self.InfoDb