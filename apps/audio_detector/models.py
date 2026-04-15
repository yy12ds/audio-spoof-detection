from datetime import datetime
from apps.app import db

class UserAudio(db.Model):
    __tablename__="user_audio"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    audio_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class UserAudioTag(db.Model):
    __tablename__="user_audio_tags"
    id = db.Column(db.Integer, primary_key=True)
    user_audio_id = db.Column(db.String, db.ForeignKey("user_audio.id"))
    tag_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)