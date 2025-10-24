from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# In-memory database
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# ---------- Home Page ----------
@app.route('/')
def home():
    return render_template('index.html', users=users)

# ---------- Add User ----------
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email:
        return "Name and Email are required", 400
    new_id = max(users.keys()) + 1 if users else 1
    users[new_id] = {"name": name, "email": email}
    return redirect(url_for('home'))

# ---------- Update Page ----------
@app.route('/update/<int:user_id>')
def update_page(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found", 404
    return render_template('update.html', user_id=user_id, user=user)

# ---------- Update User ----------
@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found", 404
    user["name"] = request.form.get('name', user["name"])
    user["email"] = request.form.get('email', user["email"])
    return redirect(url_for('home'))

# ---------- Delete User ----------
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    if user_id in users:
        users.pop(user_id)
        return redirect(url_for('home'))
    return "User not found", 404

# ---------- API Endpoints ----------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
