    #-----------------------------------------
# LIBRARIES
#-----------------------------------------

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from routes import api_bp
from  termcolor import colored

#-----------------------------------------
# INIT
#-----------------------------------------

print("\n------------------------------------------")
print("| FLASK API STARTING...")
print("------------------------------------------")

host = input('|> Provide your API server host: ').strip() or "localhost"
port = input('|> Provide your API server port: ').strip() or "5000"

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "ADAMS23"
jwt = JWTManager(app)

app.register_blueprint(api_bp)


#-----------------------------------------
# ERROR HANDLING
#-----------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "error_message": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "error_message": "An unexpected error occurred.",'lang':supported_languages}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # You can also log the exception here
    return jsonify({"error": "Internal Server Error", "error_message": str(e)}), 500


app.run(host=host, port=port, debug=True)
