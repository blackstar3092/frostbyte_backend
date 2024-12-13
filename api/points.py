from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (for demo)
points_data = {}

# Endpoint to submit points
@app.route('/submit-points', methods=['POST'])
def submit_points():
    data = request.jsonify
    username = data.get('username')
    points = data.get('points')

    if not username or points is None:
        return jsonify({"message": "Username and points are required."}), 400

    points_data[username] = points
    return jsonify({"message": "Points saved successfully!", "points": points_data[username]})

# Endpoint to get points
@app.route('/get-points/<username>', methods=['GET'])
def get_points(username):
    points = points_data.get(username)

    if points is None:
        return jsonify({"message": "User not found."}), 404

    return jsonify({"username": username, "points": points})

if __name__ == '__main__':
    app.run(debug=True)
