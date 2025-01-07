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
        "FirstName": "Abby",
        "LastName": "Manalo",
        "FavoriteColor": "Purple",
        "FavoriteFruit": "Mango",
        "FavoriteSport": "Dance", 
        "Hobbies": ["Baking",  "Watching Shows",  "Reading",  "Coloring",]
    })
            
    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Aranya",
        "LastName": "Bhattacharya",
        "FavoriteColor": "Orange",
        "FavoriteFruit": "Mango",
        "FavoriteSport": "Boxing", 
        "Hobbies": ["Watching Movies",  "Walking Dog",  "Machine Learning",  "Excercise",]
    })
    
    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Ava",
        "LastName": "Shalon",
        "FavoriteColor": "blue",
        "FavoriteFruit": "Avocado",
        "FavoriteSport": "none",
        "Hobbies": ["Watching TV",  "Cooking",  "Swimming",  "Going to the beach"]
    })
    
    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Elliot",
        "LastName": "Yang",
        "FavoriteColor": "purple",
        "FavoriteFruit": "watermelon",
        "FavoriteSport": "none",
        "Hobbies": ["Reading",  "Exercising",  "Going to the beach",  "Hiking",  "Singing",  "Playing instruments"]
    })
    
    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Risha",
        "LastName": "Guha",
        "FavoriteColor": "Blue",
        "FavoriteFruit": "mango",
        "FavoriteSport": "badminton", 
        "Hobbies": ["Reading",  "Piano",  "Cybersecurity",  "Video Games",  "Debate"]
    })
    
     # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Shriya",
        "LastName": "Paladugu",
        "FavoriteColor": "Pink",
        "FavoriteFruit": "Orange",
        "FavoriteSport": "Basketball",
        "Hobbies": ["Basketball",  "CyberSecurity",  "Hanging out with friends",  "Speech and Debate"]
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


@app.route('/student')
def print_data_student():
    html_content = """
    
<h1>Access data from our Flask server using JavaScript</h1>

<p>This code extracts data "live" from a local Web Server with JavaScript fetch.  Additionally, it formats the data into a table.</p>

<!-- Head contains information to Support the Document -->


<!-- HTML table fragment for page -->
<table id="demo" class="table">
  <thead>
      <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Favorite Color</th>
          <th>Favorite Fruit</th>
          <th>Favorite Sport</th>
          <th>Hobbies</th>  
      </tr>
  </thead>
  <tbody id="result">
    <!-- javascript generated data -->
  </tbody>
</table>

<script>
  // prepare HTML result container for new output
  let resultContainer = document.getElementById("result");
  
  // prepare URL
  url = "http://127.0.0.1:5001/api/data";

  // set options for cross origin header request
  let options = {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'default', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'include', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // fetch the API
  fetch(url, options)
    // response is a RESTful "promise" on any successful fetch
    .then(response => {
      // check for response errors and display
      if (response.status !== 200) {
          console.error(response.status);
          return;
      }
      // valid response will contain json data
      response.json().then(data => {
          console.log(data);
          for (const row of data) {
            // tr and td build out for each row
            const tr = document.createElement("tr");
            const firstname = document.createElement("td");
            const lastname = document.createElement("td");
            const FavoriteColor = document.createElement("td");
            const FavoriteFruit = document.createElement("td");
            const FavoriteSport = document.createElement("td");
            const Hobbies = document.createElement("td");
            // data is specific to the API
            firstname.innerHTML = row.FirstName; 
            lastname.innerHTML = row.LastName; 
            FavoriteColor.innerHTML = row.FavoriteColor;
            FavoriteFruit.innerHTML = row.FavoriteFruit;
            FavoriteSport.innerHTML = row.FavoriteSport;
            Hobbies.innerHTML = row.Hobbies; 
            // this builds each td into tr
            tr.appendChild(firstname);
            tr.appendChild(lastname);
            tr.appendChild(FavoriteColor);
            tr.appendChild(FavoriteFruit);
            tr.appendChild(FavoriteSport);
            tr.appendChild(Hobbies);
            // add HTML to container
            resultContainer.appendChild(tr);
          }
      })
  })
  
</script>
    
    """
    return html_content 

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)

