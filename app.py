from flask import Flask, render_template, request, redirect, url_for, flash
from tracker import FoodTracker

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

tracker = FoodTracker()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        food_name = request.form['food_name']
        use_api = request.form.get('use_api') == 'no'

        if use_api:
            food = tracker.fetch_nutrition(food_name)
            if food:
                tracker.add_food(food)
                flash("Entry added using API!", "success")
        else:
            try:
                calories = int(request.form['calories'])
                protein = int(request.form['protein'])
                fat = int(request.form['fat'])
                carbs = int(request.form['carbs'])
                tracker.add_food_manual(food_name, calories, protein, fat, carbs)
                flash("Manual entry added!", "success")
            except ValueError:
                flash("Invalid input values", "danger")

        return redirect(url_for('log'))
    return render_template('log.html')

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if request.method == 'POST':
        try:
            protein = int(request.form['protein_goal'])
            fat = int(request.form['fat_goal'])
            carbs = int(request.form['carbs_goal'])
            tracker.set_goals(protein, fat, carbs)
            flash("Goals updated successfully!", "success")
        except ValueError:
            flash("Please enter valid integer values for goals.", "danger")
        return redirect(url_for('goals'))
    return render_template('goals.html')

@app.route('/review')
def review():
    percentages = tracker.calculate_goal_percentages()
    return render_template('review.html', percentages=percentages)

@app.route('/weekly')
def weekly():
    totals = tracker.calculate_weekly_totals()
    return render_template('weekly.html', totals=totals)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/entries')
def entries():
    logs = tracker.get_entries()
    return render_template('entries.html', entries=logs)

@app.route('/delete/<int:row_num>', methods=['POST'])
def delete(row_num):
    if tracker.delete_entry(row_num):
        flash("Entry deleted successfully!", "success")
    else:
        flash("Failed to delete entry.", "danger")
    return redirect(url_for('entries'))