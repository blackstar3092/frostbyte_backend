from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (for demo)
points_data = {}

# Endpoint to submit points
@app.route('/api/submit-points', methods=['POST'])
def submit_points():
    data = request.json
    username = data.get('username')
    points = data.get('points')

    if not username or points is None:
        return jsonify({"message": "Username and points are required."}), 400

    # Save points to in-memory storage
    points_data[username] = points
    return jsonify({"message": "Points saved successfully!", "username": username, "points": points_data[username]})

# Endpoint to get points
@app.route('/api/get-points/<username>', methods=['GET'])
def get_points(username):
    points = points_data.get(username)

    if points is None:
        return jsonify({"message": "User not found."}), 404

    return jsonify({"username": username, "points": points})

if __name__ == '__main__':
    app.run(debug=True)
