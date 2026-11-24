from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "local-test-secret-key"

VALID_USER = "User"
VALID_PASS = "Password1"

BASE_STYLE = """
<style>
  body { font-family: system-ui, sans-serif; max-width: 620px; margin: 40px auto; padding: 0 20px; line-height: 1.5; }
  .box { border: 1px solid #ccc; padding: 20px; border-radius: 6px; margin-bottom: 20px; }
  label { display: block; margin-top: 10px; font-weight: 600; }
  input { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
  button { margin-top: 15px; padding: 8px 16px; cursor: pointer; }
  nav { margin-bottom: 20px; }
  nav a { margin-right: 15px; }
</style>
"""

PUBLIC_HTML = f"""
<!DOCTYPE html>
<html>
<head><title>Public Test Page</title>{BASE_STYLE}</head>
<body>
  <nav>
    <a href="/public">Public Page</a>
    <a href="/private">Private Page</a>
  </nav>

  <h1>Public Test Page</h1>

  <div class="box">
    <h3>Canaries</h3>
    <!-- 1. Visible canary -->
    <p>Visible canary: <code>CANARY-VIS-1234</code></p>
    <!-- 2. Hidden canary -->
    <p>Something is hidden here!!</p>
    <div style="display:none;">CANARY-HID-5678</div>
  </div>

  <div class="box">
    <h3>Form Canary (Type Fake Data, Do Not Submit)</h3>
    <!-- 3. Form canary -->
    <form onsubmit="return false;">
      <label for="pub_name">Fake Name</label>
      <input id="pub_name" type="text" name="fake_name" placeholder="Hello world">

      <label for="phone">Phone number</label>
      <input id="phone" type="text" name="phone" placeholder="514-123-1234">
    </form>
  </div>
</body>
</html>
"""

LOGIN_HTML = f"""
<!DOCTYPE html>
<html>
<head><title>Login - Private Test Page</title>{BASE_STYLE}</head>
<body>
  <nav><a href="/public">Back to Public Page</a></nav>
  <h1>Login Required</h1>
  {{% if error %}}<p style="color:red;">{{{{ error }}}}</p>{{% endif %}}
  <div class="box">
    <form method="POST">
      <label for="username">Username</label>
      <input id="username" type="text" name="username" value="User">

      <label for="password">Password</label>
      <input id="password" type="password" name="password" value="Password1">

      <button type="submit">Log In</button>
    </form>
  </div>
</body>
</html>
"""

PRIVATE_HTML = f"""
<!DOCTYPE html>
<html>
<head><title>Private Test Page</title>{BASE_STYLE}</head>
<body>
  <nav>
    <a href="/public">Public Page</a>
    <a href="/private">Private Page</a>
    <a href="/logout">Logout</a>
  </nav>

  <h1>Private Test Page (Authenticated)</h1>

  <div class="box">
    <h3>Sensitive Content</h3>
    <p>Confidential record: This is my SIN <code>123 345 567</code>.</p>
  </div>

  <div class="box">
    <h3>Canaries</h3>
    <!-- 1. Visible canary -->
    <p>Visible canary: <code>CANARY-VIS-1234</code></p>
    <!-- 2. Hidden canary -->
    <p>Something is hidden here!!</p>
    <div style="display:none;">CANARY-HID-5678</div>
  </div>

  <div class="box">
    <h3>Form Canary (Type Fake Data, Do Not Submit)</h3>
    <!-- 3. Form canary -->
    <form onsubmit="return false;">
      <label for="priv_name">Name</label>
      <input id="priv_name" type="text" name="fake_name" placeholder="Mark Carney">

      <label for="priv_card">Test Card Number</label>
      <input id="priv_card" type="text" name="test_card" placeholder="4242-4242-4242-4242">
    </form>
  </div>
</body>
</html>
"""

@app.route("/")
@app.route("/public")
def public_page():
    return render_template_string(PUBLIC_HTML)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == VALID_USER and request.form.get("password") == VALID_PASS:
            session["logged_in"] = True
            return redirect(url_for("private_page"))
        error = "Invalid credentials"
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/private")
def private_page():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(PRIVATE_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("public_page"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)