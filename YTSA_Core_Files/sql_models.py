"""Script to set up database. Run from this file as main to create DB.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    # pylint: disable=too-few-public-methods
    """_summary_
    # Easy reference for top videos by sentiment
    Args:
        db (_type_): _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)

class VideoInfo(db.Model):
    # pylint: disable=too-few-public-methods
    """_summary_

    Args:
        db (_type_): _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    # Video ID string, comes after "watch?v=".
    # So for https://www.youtube.com/watch?v=jfKfPfyJRdk the ID is 'jfKfPfyJRdk'
    video_id = db.Column(db.String, nullable=False, unique=True)
    video_title = db.Column(db.String, nullable=False)
    channel = db.Column(db.String)
    # Raw sentiment score as floating pt value
    sentiment_score_average = db.Column(db.Float)
    negative_entries = db.Column(db.Integer, default=0)
    positive_entries = db.Column(db.Integer, default=0)
    neutral_entries = db.Column(db.Integer, default=0)
    date_updated = db.Column(db.String, nullable=False)

class TopVideos(db.Model):
    # pylint: disable=too-few-public-methods
    """_summary_
    # Easy reference for top videos by sentiment
    Args:
        db (_type_): _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False, unique=True)
    date_updated = db.Column(db.String, nullable=False)

class VideoCategories(db.Model):
    # pylint: disable=too-few-public-methods
    """_summary_
    # Video Cateogries updated on video classificaton. Categories are added and
    # keep a running average of sentiment score
    Args:
        db (_type_): _description_
    """
    # To update: current_sum = current_avrg * current_count. 
    # current_sum += new_score. average = current_sum/updated_count
    id = db.Column(db.Integer, primary_key=True)
    sentiment_score_average = db.Column(db.Float)
    date_updated = db.Column(db.String, nullable=False)

class Channels(db.Model):
    # pylint: disable=too-few-public-methods
    """_summary_
    # Channel updated on video classificaton. Categories are added and keep a running average 
    # of sentiment score (same as by category)
    Args:
        db (_type_): _description_
    """
    # To update: current_sum = current_avrg * current_count. current_sum += new_score.
    # average = current_sum/updated_count
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String, unique=True)
    sentiment_score_average = db.Column(db.Float)
    date_updated = db.Column(db.String, nullable=False)

# Update with new tables (will not overwrite existing)
# "Create tables that do not exist in the database 
# by calling metadata.create_all() for all or some bind keys.
# This does not update existing tables, use a migration library for that."
