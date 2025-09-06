# Calorie Mind

A Flask web application for tracking calorie intake and nutrition goals.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Google Sheets API Setup

This application uses Google Sheets to store calorie tracking data. You need to set up Google Sheets API credentials:

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Google Sheets API:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and enable it

3. **Create Service Account:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"

4. **Generate JSON Key:**
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose JSON format
   - Download the JSON file

5. **Set up credentials:**
   - Copy `creds.template.json` to `creds.json`
   - Replace the placeholder values in `creds.json` with your downloaded JSON key
   - Make sure the file is named `creds.json` and is in the project root

6. **Share Google Sheet:**
   - Create a Google Sheet named "calorietracker"
   - Add worksheets: "Entries", "Goal", "WeekTotal"
   - Share the sheet with your service account email (found in the JSON file)

### 3. Run the Application
```bash
python manage.py
```

The application will be available at `http://localhost:5000`

## Railway Deployment

### Deploy to Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Railway project:**
   ```bash
   railway init
   ```

4. **Set environment variables:**
   ```bash
   railway variables set SECRET_KEY=aafc60326f192feacf0bf5406fdb1ba27d3a4163acd58e9cb68d078fceebe01c
   railway variables set FLASK_ENV=production
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

**Note:** Railway will automatically detect this as a Python project using the `nixpacks.toml` configuration.

### Alternative: Deploy via Railway Dashboard

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables in Railway dashboard:
   - `SECRET_KEY`: Your Flask secret key
   - `FLASK_ENV`: `production`
4. Deploy automatically on git push

## Features

- Track daily calorie intake
- Set nutrition goals (protein, fat, carbs)
- View weekly totals
- Integration with Google Sheets for data storage
- Nutrition API integration for food lookup

## File Structure

- `app.py` - Main Flask application
- `tracker.py` - Food tracking logic and Google Sheets integration
- `manage.py` - Flask CLI management script
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `creds.json` - Google Sheets API credentials (you need to set this up) 