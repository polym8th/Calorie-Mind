import gspread
import requests
from google.oauth2.service_account import Credentials
from dataclasses import dataclass
from datetime import datetime

# Google Sheets API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Initialize Google Sheets connection with error handling
GSPREAD_CLIENT = None
SHEET = None
WORKSHEET = None
GOALS_WORKSHEET = None
WEEKTOTAL_WORKSHEET = None

try:
    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open("calorietracker")
    WORKSHEET = SHEET.worksheet("Entries")
    GOALS_WORKSHEET = SHEET.worksheet("Goal")
    WEEKTOTAL_WORKSHEET = SHEET.worksheet("WeekTotal")
    GOOGLE_SHEETS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Google Sheets not available: {e}")
    print("The application will run without Google Sheets integration.")
    print("To enable Google Sheets, please set up proper credentials in creds.json")
    GOOGLE_SHEETS_AVAILABLE = False

API_KEY = "0brAMYcW8oY8uL4wFW6pEA==5CQZgsWVqQWDKyCr"
API_URL = "https://api.calorieninjas.com/v1/nutrition"

@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int

class FoodTracker:
    def __init__(self):
        self.today = []
        self.protein_goal = 100
        self.fat_goal = 70
        self.carbs_goal = 200

    def add_food(self, food: Food):
        self.today.append(food)
        self._add_to_google_sheets(food)

    def add_food_manual(self, name, calories, protein, fat, carbs):
        food = Food(name, calories, protein, fat, carbs)
        self.add_food(food)

    def _add_to_google_sheets(self, food: Food):
        if not GOOGLE_SHEETS_AVAILABLE:
            print("Google Sheets not available - data not saved")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, food.name, food.calories, food.protein, food.fat, food.carbs]
        WORKSHEET.append_row(row)

    def set_goals(self, protein, fat, carbs):
        self.protein_goal = protein
        self.fat_goal = fat
        self.carbs_goal = carbs
        self._log_goals()

    def _log_goals(self):
        if not GOOGLE_SHEETS_AVAILABLE:
            print("Google Sheets not available - goals not saved")
            return
        protein_sum = sum(f.protein for f in self.today)
        fat_sum = sum(f.fat for f in self.today)
        carbs_sum = sum(f.carbs for f in self.today)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        row = [timestamp, protein_sum, fat_sum, carbs_sum,
               self.protein_goal, self.fat_goal, self.carbs_goal]
        GOALS_WORKSHEET.append_row(row)

    def calculate_goal_percentages(self):
        if not self.today:
            return {"protein": 0, "fat": 0, "carbs": 0}

        protein_sum = sum(f.protein for f in self.today)
        fat_sum = sum(f.fat for f in self.today)
        carbs_sum = sum(f.carbs for f in self.today)

        def calc(consumed, goal):
            return min((consumed / goal) * 100 if goal else 0, 100)

        return {
            "protein": round(calc(protein_sum, self.protein_goal), 2),
            "fat": round(calc(fat_sum, self.fat_goal), 2),
            "carbs": round(calc(carbs_sum, self.carbs_goal), 2),
        }

    def calculate_weekly_totals(self):
        if not GOOGLE_SHEETS_AVAILABLE:
            print("Google Sheets not available - using local data only")
            return {
                "calories": sum(f.calories for f in self.today),
                "protein": sum(f.protein for f in self.today),
                "fat": sum(f.fat for f in self.today),
                "carbs": sum(f.carbs for f in self.today)
            }
        
        entries = WORKSHEET.get_all_values()
        data = entries[-7:] if len(entries) >= 7 else entries

        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for row in data:
            try:
                total_calories += int(row[2]) if row[2].isdigit() else 0
                total_protein += int(row[3]) if row[3].isdigit() else 0
                total_fat += int(row[4]) if row[4].isdigit() else 0
                total_carbs += int(row[5]) if row[5].isdigit() else 0
            except IndexError:
                continue

        timestamp = datetime.now().strftime("%Y-%m-%d")
        WEEKTOTAL_WORKSHEET.append_row([
            timestamp, total_calories, total_protein, total_fat, total_carbs
        ])

        return {
            "calories": total_calories,
            "protein": total_protein,
            "fat": total_fat,
            "carbs": total_carbs,
        }

    def fetch_nutrition(self, food_name):
        headers = {"X-Api-Key": API_KEY}
        params = {"query": food_name}

        try:
            res = requests.get(API_URL, headers=headers, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            if data["items"]:
                item = data["items"][0]
                return Food(
                    name=food_name,
                    calories=int(item.get("calories", 0)),
                    protein=int(item.get("protein_g", 0)),
                    fat=int(item.get("fat_total_g", 0)),
                    carbs=int(item.get("carbohydrates_total_g", 0)),
                )
        except requests.RequestException:
            return None

    def get_entries(self, limit=50):
        """Fetch the most recent food entries."""
        if not GOOGLE_SHEETS_AVAILABLE:
            return []
        entries = WORKSHEET.get_all_values()
        headers = entries[0] if entries else []
        rows = entries[-limit:] if len(entries) > 1 else []
        return [{"row_num": i + 2, **dict(zip(headers, row))} for i, row in enumerate(rows)]

    def delete_entry(self, row_num):
        """Delete a row from the worksheet by its row number."""
        if not GOOGLE_SHEETS_AVAILABLE:
            print("Google Sheets not available - cannot delete entry")
            return False
        try:
            WORKSHEET.delete_rows(row_num)
            return True
        except Exception as e:
            print(f"Error deleting row: {e}")
            return False