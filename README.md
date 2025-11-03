# Jeevan-Amrit Backend 🌸

Flask + MongoDB backend for the Jeevan-Amrit wellness application.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   cd jeevan-amrit-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Activate (Windows)
   venv\Scripts\activate

   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env

   # Edit .env and update:
   # - SECRET_KEY (generate random string)
   # - MONGO_URI (your MongoDB connection string)
   ```

5. **Start MongoDB**
   ```bash
   # Make sure MongoDB is running locally or use MongoDB Atlas
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   Server will start at: http://localhost:5000

## 📁 Project Structure

```
jeevan-amrit-backend/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/             # HTML templates
│   └── index.html
└── static/                # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 🔌 API Endpoints

### Health Check
- **GET** `/api/health` - Check if API is running

### Users
- **POST** `/api/users` - Create or get user
- **GET** `/api/users/<user_id>` - Get user details

### Mood Tracker
- **POST** `/api/mood` - Save mood entry
- **GET** `/api/mood/<user_id>` - Get mood history
- **GET** `/api/mood/latest/<user_id>` - Get latest mood

### Daily Routines
- **POST** `/api/routines` - Save routine completion
- **GET** `/api/routines/<user_id>/today` - Get today's routines
- **GET** `/api/ai-suggestions?period=morning` - Get AI suggestions

### Sleep Tracker
- **POST** `/api/sleep` - Save sleep data
- **GET** `/api/sleep/<user_id>` - Get sleep history

### Analytics
- **GET** `/api/analytics/<user_id>?days=7` - Get wellness analytics

## 🧪 Testing API

```bash
# Health check
curl http://localhost:5000/api/health

# Save mood
curl -X POST http://localhost:5000/api/mood \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test123","mood_level":75,"emotional":8,"mental":7,"physical":9}'

# Get analytics
curl http://localhost:5000/api/analytics/test123?days=7
```

## 🗄️ MongoDB Collections

- **users** - User profiles and preferences
- **mood_tracker** - Daily mood entries
- **daily_routines** - Routine completions
- **sleep_tracker** - Sleep quality data

## 🔐 Security

- Never commit `.env` file
- Change `SECRET_KEY` in production
- Use HTTPS in production
- Enable authentication for production APIs

## 🌐 Deployment

### MongoDB Atlas Setup
1. Create account at mongodb.com/atlas
2. Create cluster and database
3. Get connection string
4. Update MONGO_URI in .env

### Heroku Deployment
```bash
heroku create jeevan-amrit-api
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGO_URI=your-mongodb-uri
git push heroku main
```

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

Built with ❤️ for holistic wellness
