# Script to set up database. Run from this file as main to create DB.
import flask, os, requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# still trying to figure out how to keep these methods out of main
# for now have to re-declare all of this boilerplate.
db = SQLAlchemy()


# Todo create class hierarchy instead of redundant lines if possible with sql alchemy
# ToDo I dont like the name 'entry_count' but it is sometimes videos, comments etc. think of something better.
class Users(db.Model):
    # Easy reference for top videos by sentiment
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)

class Video_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Video ID string, comes after "watch?v=". So for https://www.youtube.com/watch?v=jfKfPfyJRdk the ID is 'jfKfPfyJRdk'
    video_id = db.Column(db.String, nullable=False, unique=True)
    video_tite = db.Column(db.String, nullable=False)
    channel = db.Column(db.String)
    # Raw sentiment score as floating pt value
    sentiment_score_average = db.Column(db.Float)
    entry_count = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.String, nullable=False)

class Top_Videos(db.Model):
    # Easy reference for top videos by sentiment
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False, unique=True)
    sentiment_score_average = db.Column(db.Float)
    entry_count = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.String, nullable=False)

class Video_Categories_Log(db.Model):
    # Video Cateogries updated on video classificaton. Categories are added and keep a running average of sentiment score
    # To update: current_sum = current_avrg * current_count. current_sum += new_score. average = current_sum/updated_count
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False, unique=True)
    # Number of videos contributing to the average
    entry_count = db.Column(db.Integer, nullable=False)
    # Sentiment score average =
    sentiment_score_average = db.Column(db.Float)
    date_updated = db.Column(db.String, nullable=False)

class Channel_Log(db.Model):
    # Channel updated on video classificaton. Categories are added and keep a running average of sentiment score (same as by category)
    # To update: current_sum = current_avrg * current_count. current_sum += new_score. average = current_sum/updated_count
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String, unique=True)
    # Number of videos contributing to the average
    entry_count = db.Column(db.Integer, nullable=False)
    # Sentiment score average =
    sentiment_score_average = db.Column(db.Float)
    date_updated = db.Column(db.String, nullable=False)

# Update with new tables (will not overwrite existing)
# "Create tables that do not exist in the database by calling metadata.create_all() for all or some bind keys.
# This does not update existing tables, use a migration library for that."
