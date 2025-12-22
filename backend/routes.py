from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import mongo, limiter
from bson.objectid import ObjectId
import datetime
import bcrypt
import io
import csv
from flask import Response, stream_with_context

api_bp = Blueprint("api", __name__)

# --- Public Routes ---

@api_bp.route("/feedback", methods=["POST"])
@limiter.limit("5 per minute")
def submit_feedback():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Feedback text is required"}), 400
    
    # Input Validation: Type-cast to string to prevent NoSQL injection
    text = str(data["text"])
    
    feedback = {
        "text": text,
        "created_at": datetime.datetime.utcnow(),
        "is_read": False
    }
    
    mongo.db.feedbacks.insert_one(feedback)
    return jsonify({"message": "Feedback submitted successfully"}), 201

# --- Auth Routes ---

@api_bp.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    # Input Validation: Type-cast to string to prevent NoSQL injection
    username = str(data["username"])
    password = str(data["password"])
    
    admin = mongo.db.admins.find_one({"username": username})
    
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin["password"]):
        access_token = create_access_token(identity=str(admin["_id"]))
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# --- Admin Routes ---

@api_bp.route("/admin/feedbacks", methods=["GET"])
@jwt_required()
def get_feedbacks():
    feedbacks = list(mongo.db.feedbacks.find().sort("created_at", -1))
    for f in feedbacks:
        f["_id"] = str(f["_id"])
        if "created_at" in f and f["created_at"]:
            f["created_at"] = f["created_at"].isoformat()
    return jsonify(feedbacks), 200

@api_bp.route("/admin/feedbacks/<id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(id):
    try:
        result = mongo.db.feedbacks.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Feedback deleted"}), 200
        return jsonify({"error": "Feedback not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@api_bp.route("/admin/export", methods=["GET"])
@jwt_required()
def export_feedbacks():
    def generate():
        data = io.StringIO()
        w = csv.writer(data)
        
        # Write header
        w.writerow(('Feedback ID', 'Text', 'Date (UTC)'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # Get all feedbacks
        feedbacks = mongo.db.feedbacks.find().sort("created_at", -1)
        
        for f in feedbacks:
            w.writerow((
                str(f["_id"]),
                f["text"],
                f["created_at"].isoformat() if f.get("created_at") else ""
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
            
        # Clear database after export
        mongo.db.feedbacks.delete_many({})

    response = Response(stream_with_context(generate()), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="feedbacks.csv")
    return response
