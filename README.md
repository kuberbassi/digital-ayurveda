# shlok
Hackathon with Smarth Sharma


"I worship that supreme soul, the one, the primordial seed of the universe, desireless, formless, knowable through Om. From whom the universe originates, by whom it is sustained, and into whom it dissolves."

"परात्मानमेकं जगद्बीजमाद्यं निरीहं निराकारमोंकारवेद्यम्।
        यतो जायते पाल्यते येन विश्वं तमीशं भजे लीयते यत्र विश्वम्।|


"Just as a flower, when it falls, spreads its fragrance all around. Similarly, good people should always do deeds that are beneficial to all."

यथा पुष्पं न पात्येत वासितं हि समन्ततः।
        तथा सत्पुरुषैर्नित्यं कार्यं यत्सर्वहिताय वै॥



"I bow to the moon, Soma, born from the milk ocean, white as conch and snow, the ornament on Shiva's crown."

 दधिशङ्खतुषाराभं क्षीरोदार्णवसम्भवम्।
        नमामि शशिनं सोमं शम्भोर्मुकुटभूषणम्॥



Based on your goal of making a "good aesthetic website," here's my recommendation:

1. Top Choice: 3. Jeevan-Amrit (Health & Wellness)

This is your strongest option by far. Wellness apps are all about aesthetics. The entire point is to "promote physical and mental balance," which is achieved through a calming, beautiful, and intuitive user interface (UI/UX).

Why it's a fit: You can focus on clean design, soothing colors, elegant data visualization (for wellness tracking), and a great user experience. This plays right into your strengths as a "creative tech mix."

Shloka Connection: It will also be much easier to find shlokas from your list that relate to "life," "balance," "mind," and "health" to integrate into this theme.




digiayur-admin
i6LPoptFvZ5jLqmT


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
