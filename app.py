from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/jeevan_amrit_db')

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB Connection
try:
    client = MongoClient(app.config['MONGO_URI'])
    db = client.jeevan_amrit_db

    # Collections
    users = db.users
    mood_tracker = db.mood_tracker
    daily_routines = db.daily_routines
    sleep_tracker = db.sleep_tracker
    session_scores = db.session_scores # NEW: For session-based wellness score

    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'success',
        'message': 'Jeevan-Amrit API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ==================== USER ROUTES ====================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        email = data.get('email')

        # Check if user exists
        existing_user = users.find_one({'email': email})
        if existing_user:
            existing_user['_id'] = str(existing_user['_id'])
            return jsonify({
                'status': 'success',
                'message': 'User already exists',
                'user': existing_user
            }), 200

        # Create new user
        user = {
            'name': data.get('name', 'Guest'),
            'email': email,
            'preferences': {'theme': 'light', 'notifications': True},
            'created_at': datetime.utcnow()
        }

        result = users.insert_one(user)
        user['_id'] = str(result.inserted_id)

        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'user': user
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    try:
        user = users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        user['_id'] = str(user['_id'])
        return jsonify({'status': 'success', 'user': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== MOOD TRACKER ROUTES ====================

@app.route('/api/mood', methods=['POST'])
def save_mood():
    """Save mood tracking data"""
    try:
        data = request.json
        mood_entry = {
            'user_id': data.get('user_id', 'guest'),
            'mood_level': int(data.get('mood_level', 50)),
            'emotional': int(data.get('emotional', 5)),
            'mental': int(data.get('mental', 5)),
            'physical': int(data.get('physical', 5)),
            'notes': data.get('notes', ''),
            'timestamp': datetime.utcnow(),
            'date': datetime.utcnow().date().isoformat()
        }

        result = mood_tracker.insert_one(mood_entry)
        mood_entry['_id'] = str(result.inserted_id)
        mood_entry['timestamp'] = mood_entry['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'message': 'Mood saved successfully',
            'mood': mood_entry
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/mood/<user_id>', methods=['GET'])
def get_mood_history(user_id):
    """Get mood history for a user"""
    try:
        days = int(request.args.get('days', 7))
        start_date = datetime.utcnow() - timedelta(days=days)

        moods = list(mood_tracker.find({
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }).sort('timestamp', -1).limit(100))

        for mood in moods:
            mood['_id'] = str(mood['_id'])
            mood['timestamp'] = mood['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'count': len(moods),
            'moods': moods
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/mood/latest/<user_id>', methods=['GET'])
def get_latest_mood(user_id):
    """Get latest mood entry"""
    try:
        mood = mood_tracker.find_one(
            {'user_id': user_id},
            sort=[('timestamp', -1)]
        )

        if not mood:
            return jsonify({'status': 'success', 'mood': None}), 200

        mood['_id'] = str(mood['_id'])
        mood['timestamp'] = mood['timestamp'].isoformat()

        return jsonify({'status': 'success', 'mood': mood}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== DAILY ROUTINES ROUTES ====================

@app.route('/api/routines', methods=['POST'])
def save_routine():
    """Save daily routine completion"""
    try:
        data = request.json
        routine = {
            'user_id': data.get('user_id', 'guest'),
            'time_period': data.get('time_period'),
            'activities': data.get('activities', []),
            'completed': data.get('completed', False),
            'completion_percentage': data.get('completion_percentage', 0),
            'date': datetime.utcnow().date().isoformat(),
            'timestamp': datetime.utcnow()
        }

        result = daily_routines.insert_one(routine)
        routine['_id'] = str(result.inserted_id)
        routine['timestamp'] = routine['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'message': 'Routine saved successfully',
            'routine': routine
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/routines/<user_id>/today', methods=['GET'])
def get_today_routines(user_id):
    """Get today's routines"""
    try:
        today = datetime.utcnow().date().isoformat()
        routines = list(daily_routines.find({
            'user_id': user_id,
            'date': today
        }))

        for routine in routines:
            routine['_id'] = str(routine['_id'])
            routine['timestamp'] = routine['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'count': len(routines),
            'routines': routines
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== DAILY ROUTINES ROUTES (Cont.) ====================
# ... (existing /api/routines/<user_id>/today route is above this)

@app.route('/api/ai-suggestions', methods=['GET'])
def get_ai_suggestions():
    """
    Get AI-powered wellness suggestions, dynamically adjusting 
    based on the user's latest mood and adding random activities.
    """
    try:
        import random # This needs to be imported at the top of app.py

        period = request.args.get('period', 'evening') # Default to evening for "Soma Zone" focus
        user_id = request.args.get('user_id', 'temp_user_hackathon') 

        # 1. Fetch latest mood for dynamic text (MongoDB usage)
        latest_mood = mood_tracker.find_one(
            {'user_id': user_id},
            sort=[('timestamp', -1)]
        )
        # mood_level is scaled 10-100 in the frontend, so we use that for logic
        mood_level = latest_mood.get('mood_level', 50) if latest_mood else 50
        
        if mood_level > 70:
            mood_status = "highly positive! Let's sustain this tranquility."
            mood_message = 'A mindful evening routine will help you lock in your great state.'
        elif mood_level < 40:
            mood_status = "needs attention. Focus on 'Soma' to cool the stress."
            mood_message = 'Prioritize deep relaxation and self-care tonight.'
        else:
            mood_status = "balanced. Great work maintaining harmony."
            mood_message = 'Continue your consistent practice to support your balance.'
            

        # 2. Define extra random activities for dynamic presentation
        extra_activities = [
            {'name': 'Chanting a Mantra', 'duration': '5 min', 'icon': '🕉️', 'benefit': 'Spiritual focus'},
            {'name': 'Oil Pulling', 'duration': '10 min', 'icon': '💧', 'benefit': 'Oral cleanse'},
            {'name': 'Listen to Soothing Ragas', 'duration': '20 min', 'icon': '🎶', 'benefit': 'Soothing sound'},
            {'name': 'Write Down 3 Wins', 'duration': '5 min', 'icon': '🏆', 'benefit': 'Fosters resilience'}
        ]
        
        # Pick two random activities
        random_activities = random.sample(extra_activities, 2)
        
        # 3. Compile all suggestions with the dynamic message
        suggestions_map = {
            'morning': {
                'title': 'Morning Ritual',
                'icon': '🌅',
                'message': f'Start your day with energy and positivity. Your aura is currently {mood_status}',
                'activities': [
                    {'name': 'Sun Salutation', 'duration': '10 min', 'icon': '🧘', 'benefit': 'Energizes body'},
                    {'name': 'Pranayama Breathing', 'duration': '5 min', 'icon': '💨', 'benefit': 'Clears mind'},
                    {'name': 'Gratitude Meditation', 'duration': '5 min', 'icon': '🙏', 'benefit': 'Positive mindset'},
                    {'name': 'Herbal Tea', 'duration': '5 min', 'icon': '🍵', 'benefit': 'Hydration'},
                    *random_activities # Add two random ones
                ]
            },
            'day': {
                'title': 'Daytime Balance',
                'icon': '☀️',
                'message': f'Maintain harmony throughout your productive hours. Remember, your balance {mood_status}',
                'activities': [
                    {'name': 'Mindful Breaks', 'duration': '10 min', 'icon': '🚶', 'benefit': 'Reduces stress'},
                    {'name': 'Positive Affirmations', 'duration': '3 min', 'icon': '✨', 'benefit': 'Boosts confidence'},
                    {'name': 'Healthy Meal', 'duration': '30 min', 'icon': '🥗', 'benefit': 'Sustained energy'},
                    {'name': 'Energy Check-in', 'duration': '2 min', 'icon': '⚡', 'benefit': 'Self-awareness'},
                    *random_activities
                ]
            },
            'evening': {
                'title': 'Evening Serenity: Moon Mode',
                'icon': '🌙',
                'message': f'{mood_message} Your latest mood {mood_status}',
                'activities': [
                    {'name': 'Gentle Yoga', 'duration': '15 min', 'icon': '🧘‍♀️', 'benefit': 'Releases tension'},
                    {'name': 'Digital Sunset', 'duration': '60 min', 'icon': '📱', 'benefit': 'Better sleep'},
                    {'name': 'Journaling', 'duration': '10 min', 'icon': '📔', 'benefit': 'Reflection'},
                    {'name': 'Sleep Meditation', 'duration': '10 min', 'icon': '😴', 'benefit': 'Deep rest'},
                    *random_activities
                ]
            }
        }

        return jsonify({
            'status': 'success',
            'period': period,
            'suggestions': suggestions_map.get(period, suggestions_map['evening'])
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== SLEEP TRACKER ROUTES ====================
# ... (rest of app.py continues here)

@app.route('/api/sleep', methods=['POST'])
def save_sleep():
    """Save sleep tracking data"""
    try:
        data = request.json
        sleep_entry = {
            'user_id': data.get('user_id', 'guest'),
            'hours': float(data.get('hours', 0)),
            'quality': int(data.get('quality', 3)),
            'notes': data.get('notes', ''),
            'date': datetime.utcnow().date().isoformat(),
            'timestamp': datetime.utcnow()
        }

        result = sleep_tracker.insert_one(sleep_entry)
        sleep_entry['_id'] = str(result.inserted_id)
        sleep_entry['timestamp'] = sleep_entry['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'message': 'Sleep data saved successfully',
            'sleep': sleep_entry
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/sleep/<user_id>', methods=['GET'])
def get_sleep_history(user_id):
    """Get sleep history"""
    try:
        days = int(request.args.get('days', 7))
        start_date = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

        sleep_data = list(sleep_tracker.find({
            'user_id': user_id,
            'date': {'$gte': start_date}
        }).sort('date', -1))

        for entry in sleep_data:
            entry['_id'] = str(entry['_id'])
            entry['timestamp'] = entry['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'count': len(sleep_data),
            'sleep_history': sleep_data
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== ANALYTICS ROUTES ====================

@app.route('/api/analytics/<user_id>', methods=['GET'])
def get_analytics(user_id):
    """
    Get wellness analytics, including historical data from all trackers 
    and the latest session-based wellness score.
    """
    try:
        days = int(request.args.get('days', 7))
        start_date = datetime.utcnow() - timedelta(days=days)

        # Mood analytics (Historical)
        moods = list(mood_tracker.find({
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }))
        avg_mood = sum(m['mood_level'] for m in moods) / len(moods) if moods else 0

        # Routine completion (Historical)
        routines = list(daily_routines.find({
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }))
        completed = sum(1 for r in routines if r.get('completed', False))
        completion_rate = (completed / len(routines) * 100) if routines else 0

        # Sleep analytics (Historical)
        sleep_data = list(sleep_tracker.find({
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }))
        avg_sleep = sum(s['hours'] for s in sleep_data) / len(sleep_data) if sleep_data else 0
        avg_quality = sum(s['quality'] for s in sleep_data) / len(sleep_data) if sleep_data else 0

        # NEW: Get the latest session score (for current 'Aura' display)
        # This score is calculated on the frontend and temporarily stored in MongoDB 
        # to simulate the "browser caching" effect for the current state.
        latest_session_score = session_scores.find_one(
            {'user_id': user_id},
            sort=[('timestamp', -1)]
        )
        current_wellness_score = latest_session_score['score'] if latest_session_score else 82 # Fallback
        
        return jsonify({
            'status': 'success',
            'analytics': {
                'average_mood': round(avg_mood, 1),
                'routine_completion': round(completion_rate, 1),
                'average_sleep_hours': round(avg_sleep, 1),
                'average_sleep_quality': round(avg_quality, 1),
                'total_mood_entries': len(moods),
                'total_routines': len(routines),
                'period_days': days, # Comma added here
                'current_wellness_score': round(current_wellness_score, 1)
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    

# ==================== WELLNESS SESSION LOG ROUTES ====================

@app.route('/api/wellness-session-log', methods=['POST'])
def save_wellness_score():
    """Save a temporary wellness score to a session-based collection"""
    try:
        data = request.json
        score_entry = {
            'user_id': data.get('user_id', 'guest'),
            'score': data.get('score', 0),
            'timestamp': datetime.utcnow()
        }

        # For "clear after session", we insert it into a dedicated collection.
        # In a real-world scenario, you would set a TTL (Time To Live) index on 'timestamp' 
        # for the 'session_scores' collection to automatically clear old entries.
        result = session_scores.insert_one(score_entry)
        
        # NOTE: To truly reflect "clearing the score," a separate background task 
        # or the TTL index would handle the deletion.
        # For this demonstration, we'll just insert it.

        score_entry['_id'] = str(result.inserted_id)
        score_entry['timestamp'] = score_entry['timestamp'].isoformat()

        return jsonify({
            'status': 'success',
            'message': 'Session score logged successfully',
            'score': score_entry
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/wellness-session-log/<user_id>', methods=['GET'])
def get_latest_session_score(user_id):
    """Get the latest temporary wellness score"""
    try:
        score = session_scores.find_one(
            {'user_id': user_id},
            sort=[('timestamp', -1)]
        )

        if not score:
            # Fallback to a default or a general analytics score if the session score isn't found
            return jsonify({'status': 'success', 'score': 75}), 200

        # We don't need to format the whole object, just return the score value
        return jsonify({'status': 'success', 'score': score['score']}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
