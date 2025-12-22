from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mongo, jwt, limiter
import os

def create_app():
    # Detect if we should serve static files (Docker production)
    # We look for the 'client' folder we created in the Dockerfile
    if os.path.exists(os.path.join(os.getcwd(), 'client')):
        app = Flask(__name__, static_folder='client/assets', template_folder='client')
        is_production = True
    else:
        app = Flask(__name__)
        is_production = False

    app.config.from_object(Config)

    # Initialize extensions
    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # Register blueprints
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # Serve Frontend in Production
    if is_production:
        from flask import send_from_directory, render_template

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            # Check if the file exists in the 'client' folder (e.g. logo.png, favicon.ico)
            client_path = os.path.join(app.template_folder, path)
            if path != "" and os.path.exists(client_path):
                return send_from_directory(app.template_folder, path)
                
            # Check if it exists in 'client/assets' (Flask static folder usually handles this, 
            # but we can be explicit if needed, or rely on /assets prefix in URL)
            if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
                 return send_from_directory(app.static_folder, path)
            
            # For everything else, serve index.html (SPA)
            return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
