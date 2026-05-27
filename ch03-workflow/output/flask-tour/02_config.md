# Chapter 2: Config

In the previous chapter, we met the `Flask` object, the central manager of our web application. We saw it orchestrating requests, routing them to the right functions, and sending back responses. Remember that last line in our first Flask app?

```python
if __name__ == "__main__":
    app.run(debug=True)
```

We set `debug=True`, which instantly unlocked helpful features like an interactive debugger and automatic code reloading. But how did the `Flask` object know what `debug=True` meant? What other settings can we adjust? How does our application learn about its database connection, the location of user-uploaded files, or its "secret password" for security features?

Just as a restaurant manager has a set of policies, menus, and operational guidelines, your Flask application needs a central place to store all its settings. This "control panel" is where you define how your entire Flask website should behave, customizing its features and behavior. This is the role of Flask's `Config` object.

The `Config` object is a special dictionary-like object attached directly to your Flask application as `app.config`. It's a key-value store where you can keep all the adjustable parameters for your application. It’s the manager's clipboard, holding all the current operational notes.

Let's see it in action by examining the `debug` setting we used earlier.

```python
from flask import Flask

app = Flask(__name__)

# Accessing the debug setting directly from app.config
print(f"Debug mode from config: {app.config['DEBUG']}")

# Running the app with debug=True explicitly sets this in the config
if __name__ == "__main__":
    app.run(debug=True)
```

When you run this, you'll see that `app.config['DEBUG']` is `True`. Flask automatically populates the `Config` with default values and allows you to override them.

### Default Configuration

Flask comes with a set of sensible default settings. These are built into the `Flask` object itself. For instance, in `src/flask/sansio/app.py`, you'll find a `default_config` attribute which is a dictionary of standard settings like:

*   `TESTING`: `False` (for production)
*   `SECRET_KEY`: `None` (must be set for secure sessions)
*   `PERMANENT_SESSION_LIFETIME`: `timedelta(days=31)` (how long a "remember me" session lasts)
*   `SESSION_COOKIE_NAME`: `'session'`
*   `MAX_CONTENT_LENGTH`: `None` (maximum size for uploaded files)

These defaults ensure your application has a baseline behavior, but you'll often need to customize them.

### Customizing Configuration

There are several ways to load and manage configuration in Flask, ranging from simple direct assignment to loading from files or environment variables.

#### 1. Direct Assignment

You can set or modify configuration values just like with a regular Python dictionary:

```python
from flask import Flask

app = Flask(__name__)

# Override the default session cookie name
app.config['SESSION_COOKIE_NAME'] = 'my_app_session'

# Set a custom upload folder path
app.config['UPLOAD_FOLDER'] = '/path/to/my/uploads'

# Directly set the secret key (for development only!)
app.config['SECRET_KEY'] = 'dev-secret-key-please-change'
```

While simple, direct assignment is often best for small, temporary tweaks or during initial setup. For more complex or environment-specific settings, other methods are preferred.

#### 2. From Python Files (`from_pyfile`)

A common and recommended way to manage configuration is by storing settings in a separate Python file. This allows for clear separation of concerns, easy commenting, and version control.

First, create a `config.py` (or any `.py` file) in your project's root directory:

```python
# config.py
DEBUG = False
SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
DATABASE_URI = 'sqlite:///your_database.db'
UPLOAD_FOLDER = 'uploads'
```

Then, load this file into your application:

```python
# app.py
from flask import Flask

app = Flask(__name__)

# Load configuration from config.py relative to the app's root path
# The 'silent=True' argument means it won't raise an error if the file is missing
app.config.from_pyfile('config.py', silent=True)

# You can now access these settings
print(f"Database URI: {app.config['DATABASE_URI']}")
print(f"Uploads go to: {app.config['UPLOAD_FOLDER']}")
```

Notice that only uppercase variables from `config.py` are loaded into `app.config`. This convention allows you to include other variables in your config file without them becoming part of the application's configuration.

#### 3. From Python Objects (`from_object`)

This method is particularly useful for managing different configurations based on the environment (development, testing, production). You can define different configuration classes and load the appropriate one.

```python
# config_environments.py
class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'dev-key'
    DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = 'VERY_SECRET_PRODUCTION_KEY' # MUST be strong and unique
    DATABASE_URI = 'postgresql://user:password@host/prod_db'
    SESSION_COOKIE_SECURE = True # Only send cookies over HTTPS

class TestingConfig:
    TESTING = True
    SECRET_KEY = 'test-key'
    DATABASE_URI = 'sqlite:///:memory:' # In-memory database for tests
```

To use this:

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

# Load a default configuration (e.g., from a development config class)
app.config.from_object('config_environments.DevelopmentConfig')

# You can override this based on an environment variable
# For example, in your terminal: export FLASK_ENV='Production'
flask_env = os.environ.get('FLASK_ENV')

if flask_env == 'Production':
    app.config.from_object('config_environments.ProductionConfig')
elif flask_env == 'Testing':
    app.config.from_object('config_environments.TestingConfig')

print(f"Current environment's DEBUG setting: {app.config['DEBUG']}")
```

When using `from_object`, Flask loads any uppercase attribute from the given object. This makes it a powerful way to switch between comprehensive configurations.

#### 4. From Environment Variables (`from_envvar` and `from_prefixed_env`)

Storing sensitive information like API keys or production database credentials directly in code or even config files can be risky. Environment variables provide a secure way to inject these settings without exposing them in your codebase.

*   **`from_envvar`**: Loads a Python config file whose path is specified by an environment variable.

    ```bash
    # In your terminal, before running the app
    export MYAPP_SETTINGS='/etc/myapp/prod_config.py'
    ```

    ```python
    # app.py
    from flask import Flask

    app = Flask(__name__)
    app.config.from_envvar('MYAPP_SETTINGS', silent=False) # silent=False will raise an error if env var not set
    ```

*   **`from_prefixed_env`**: This is a more modern and flexible way, especially for containerized applications. It automatically loads any environment variables that start with a specified prefix (e.g., `FLASK_`).

    ```bash
    # In your terminal
    export FLASK_DEBUG=true
    export FLASK_DATABASE_HOST=mydb.server.com
    export FLASK_DATABASE_USER=admin
    export FLASK_DATABASE_PASSWORD=supersecure
    ```

    ```python
    # app.py
    from flask import Flask

    app = Flask(__name__)
    app.config.from_prefixed_env()

    # Flask's built-in `DEBUG` config automatically uses `FLASK_DEBUG`
    print(f"Debug from env: {app.config['DEBUG']}")

    # You can access custom environment variables too, with the prefix removed
    print(f"DB Host from env: {app.config['DATABASE_HOST']}")
    ```

    `from_prefixed_env` can even parse JSON values from environment variables, allowing for more complex data structures. It's a robust method for configuring applications in production.

### Importance of `SECRET_KEY`

One of the most critical configuration values is `SECRET_KEY`. As you saw, its default is `None`. This key is used for cryptographic operations in Flask, most notably to securely sign session cookies. If `SECRET_KEY` is not set, or is too simple, your application's sessions will be insecure, making it vulnerable to tampering.

Always set a strong, randomly generated `SECRET_KEY` in production, and never commit it directly to version control. Environment variables or secure secrets management systems are ideal for this. The previous example of `app.config['SECRET_KEY'] = 'dev-secret-key-please-change'` is *only* suitable for a local development environment.

### The Configuration Workflow

Let's visualize how Flask processes these different configuration sources, acting like a manager gathering information from various sources to run the restaurant:

```mermaid
sequenceDiagram
    participant D as Flask Defaults
    participant E as OS Environment
    participant C as Config File
    participant A as Flask App
    participant G as app.config

    A->G: Create empty Config
    D->G: Load default settings (e.g., TESTING=False)
    E->G: Load FLASK_DEBUG, FLASK_ENV env vars
    A->C: Load config.py (from_pyfile)
    C-->G: Update settings (e.g., SECRET_KEY, UPLOAD_FOLDER)
    E->G: Load FLASK_ prefixed env vars (from_prefixed_env)
    A->G: Access app.config["SETTING"]
    G-->A: Return setting value
```

This sequence shows that settings loaded later (like from environment variables or custom files) will override earlier settings (like Flask's defaults). This allows for flexible and hierarchical configuration management.

Now you understand how your Flask application can be customized and controlled through its `Config` object. You can define various settings, load them from different sources, and ensure your application behaves exactly as you intend.

But an application isn't just about its internal settings; it's constantly interacting with the outside world, primarily through user requests. How does Flask capture all the nuances of an incoming request—the URL, the method, form data, headers, and more? That's what we'll explore in the next chapter, where we dive into the `Request` object.

Go to [Request](03_request.md)