"""_summary_
Administartive functions for managing the database 
such as adding random data for testing.
"""
import random as rand
from string import ascii_letters
from time import gmtime, strftime
import YTSA_Core_Files.sql_models as sql_models
from YTSA_Core_Files.sql_models import db

def generate_random_vid_id():
    """_summary_

    Returns:
        _type_: _description_
    """
    video_id = ""
    for i in range(0,11):
        character = rand.choice(ascii_letters)
        video_id += character
    return video_id


def sql_add_demo_data_random(num_entries):
    """_summary_
    # Must pass db object to use function
    # adds num_entries amount of randomly generated videos/etc to the database
    Args:
        num_entries (_type_): _description_
    """

    test_channels = ["channel_00", "channel_01", "channel_02", "channel_04", "channel_05"]
    for v in range(0, num_entries):
        vid_id = generate_random_vid_id()
        score = rand.random()
        video_name = "Test_Video_" + str(v)
        channel_name = rand.choice(test_channels)
        date_today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        video = sql_models.Video_Info(video_id=vid_id,
                                      channel=channel_name,
                                      video_title=video_name,
                                      sentiment_score_average=score,
                                      negative_entries=rand.randint(1,1000),
                                      positive_entries=rand.randint(1,1000),
                                      neutral_entries=rand.randint(1,1000),
                                      date_updated=date_today
                                      )
        db.session.add(video)

    db.session.commit()

def sql_add_demo_data_testing():
    """_summary_
    # Incomplete
    # Adds a few non-random entries for specific testing
    """
    print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    video = sql_models.Video_Info(video_id="lfKfPfyJRdk",
                                  channel="Belogus",
                                  video_title="A video",
                                  sentiment_score_average = 0.93,
                                  negative_entries=5,
                                  positive_entries=93,
                                  neutral_entries=2,
                                  date_updated = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                                  )

    video = sql_models.Users(user_name="Admin",
                             password="Admin",
                             email="admin@ytsa_gsu.com"
                             )
    db.session.add(video)
    db.session.commit()


def hash_password(password):
    """_summary_
    # Not implemented
    Args:
        password (_type_): _description_

    Returns:
        _type_: _description_
    """

    return password

def decrypt_password(password):
    """_summary_
    # Not implemented
    Args:
        password (_type_): _description_

    Returns:
        _type_: _description_
    """

    return password

def validate_login(db_user, password_entered):
    """_summary_
    validate submitted login with user password.
    # If selection was empty return False
    Args:
        db_user (str): username from database
        password_entered (str): password entered by user

    Returns:
        bool: Pass or fail of validation
    """

    if db_user is None:
        return False
    db_password = decrypt_password(db_user.password)
    if password_entered == db_password:
        return True
    return False

if __name__ == '__main__':
    generate_random_vid_id()