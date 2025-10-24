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

# ---------- Delete User ----------
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if user_id in users:
        users.pop(user_id)
    return redirect(url_for('home'))

# ---------- Edit User Page ----------
@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found", 404
    return render_template('edit_user.html', user_id=user_id, user=user)

# ---------- Update User ----------
@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form.get('name')
    email = request.form.get('email')
    if user_id in users:
        users[user_id]["name"] = name
        users[user_id]["email"] = email
    return redirect(url_for('home'))

# ---------- API Endpoints ----------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify({"message": "User updated", "user": user})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
