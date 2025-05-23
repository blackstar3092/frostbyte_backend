# imports from flask
import json 
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.gemini import gemini_api
from api.student import student_api
from api.vote import vote_api
from api.about import about_api
from api.analytics import analytics_blueprint
from api.star import star_api
from api.camping import camping_api
from api.quiz_api import quiz_api
from api.location import location_api  
from api.checklist import checklist_api 

# database Initialization functions
#from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.vote import Vote, initVotes
from model.about import AboutModel
from model.rating import Rating, initRatings
from model.analytics import Analytics, initAnalytics
from model.frostbyte import Frostbyte, initFrostbyte, find_by_uid
from model.gemini import AIMessage, initAIMessage
from model.camping_post import camping, initCampingPosts
from model.quiz_result import QuizResult, initQuizResults
from model.locationmodel import Location, initLocations
from model.checklist import ChecklistItem, initChecklist




# register URIs for api endpoints
app.register_blueprint(user_api)
app.register_blueprint(pfp_api) 
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(vote_api)
app.register_blueprint(gemini_api)
app.register_blueprint(student_api)
app.register_blueprint(about_api)
app.register_blueprint(star_api)
app.register_blueprint(location_api)
app.register_blueprint(camping_api) 
app.register_blueprint(quiz_api)
app.register_blueprint(checklist_api)




# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

# register URIs for server pages
@login_manager.user_loader
def load_user(user_id):
    return Frostbyte.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':

        user = Frostbyte.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/user/table')
@login_required
def utable():
    users = Frostbyte.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    users = Frostbyte.query.all()
    return render_template("u2table.html", user_data=users)


@app.route('/posts')
@login_required
def posts():
    # Query all posts from the database
    post_data = Post.query.all()
    return render_template("posts.html", post_data=post_data)


@app.route('/analytics')
@login_required
def analytics():
    # Example of fetching analytics data (modify based on your model)
    analytics_data = {
        "total_users": Frostbyte.query.count(),
        "total_posts": Post.query.count(),
        "most_active_user": Frostbyte.query.order_by(Frostbyte.activity.desc()).first().name,
        "top_channel": Channel.query.order_by(Channel.popularity.desc()).first().name
    }
    return render_template("analytics.html", analytics_data=analytics_data)


@app.route('/ratings')
@login_required
def ratings():
    ratings_data = Rating.query.all()
    return render_template("ratings.html", ratings_data=ratings_data)


@app.route('/chatbot-messages')
@login_required
def chatbot_messages():
    # Query all AI messages from the database
    messages_data = AIMessage.query.all()

    # Convert messages to a format suitable for Jinja template rendering
    formatted_messages = [
        {
            "id": msg.id,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "author": msg.author,
            "category": msg.category
        }
        for msg in messages_data
    ]

    return render_template("chatbot_messages.html", messages_data=formatted_messages)


# Helper function to extract uploads for a user (ie PFP image)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
 
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = Frostbyte.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404
@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = Frostbyte.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Set the new password
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500


@app.route('/api/rating', methods=['POST'])
@login_required
def add_rating():
    try:
        # Get input data
        data = request.get_json()
        stars = data.get("stars")
        user_id = data.get("user_id")
        channel_id = data.get("channel_id")

        # Validate input
        if stars is None or not (1 <= stars <= 5):
            return jsonify({"message": "Invalid number of stars"}), 400
        if not user_id:
            return jsonify({"message": "User ID is required"}), 400

        # Create and save the rating
        rating = Rating(stars=stars, user_id=user_id, channel_id=channel_id)
        rating.create()

        return jsonify({"message": "Rating added successfully", "rating": rating.read()}), 201
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    initFrostbyte()
    initSections()
    initGroups()
    initChannels()
    initPosts()
    initVotes()
    initRatings()
    initAIMessage()
    initCampingPosts()
    initLocations()
    initAnalytics()
    initChecklist()
    
    
# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Extract data from the existing database
def extract_data():
    data = {}
    with app.app_context():
        data['users'] = [user.read() for user in Frostbyte.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
    return data

# Save extracted data to JSON files
def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

# Load data from JSON files
def load_data_from_json(directory='backup'):
    data = {}
    for table in ['users', 'sections', 'groups', 'channels', 'posts']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        users = Frostbyte.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
        _ = Post.restore(data['posts'])
    print("Data restored to the new database.")

def create():
    # optimize user time to see if uid exists
    uid = input("Enter your user id:")
    user = find_by_uid(uid)
    try:
        print("Found\n", user.read())
        return
    except:
        pass # keep going
    
    # request value that ensure creating valid object
    name = input("Enter your name:")
    password = input("Enter your password")
    
    # Initialize User object before date
    user = Frostbyte(name=name, 
                uid=uid, 
                password=password
                )
    
    # create user.dob, fail with today as dob
    dob = input("Enter your date of birth 'YYYY-MM-DD'")
    try:
        user.dob = "datetime".strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        user.dob = "datetime".today()
        print(f"Invalid date {dob} require YYYY-mm-dd, date defaulted to {user.dob}")
           
    # write object to database
    with app.app_context():
        try:
            object = user.create()
            print("Created\n", object.read())
        except:  # error raised if object not created
            print("Unknown error uid {uid}")
        
#create()

def read():
    with app.app_context():
        table = Frostbyte.query.all()
    json_ready = [user.read() for user in table] # "List Comprehensions", for each user add user.read() to list
    return json_ready

#read()

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8102")

