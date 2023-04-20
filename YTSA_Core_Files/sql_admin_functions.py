"""_summary_
Administartive functions for managing the database
such as adding random data for testing.
"""
import random as rand
from string import ascii_letters
from time import gmtime, strftime
import YTSA_Core_Files.sql_models as sqm
from YTSA_Core_Files.sql_models import db


def generate_random_vid_id():
    """_summary_

    Returns:
        _type_: _description_
    """
    video_id = ""
    for _ in range(0, 11):
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
    for entry in range(0, num_entries):
        vid_id = generate_random_vid_id()
        score = rand.random()
        video_name = "Test_Video_" + str(entry)
        channel_name = rand.choice(test_channels)
        date_today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        video = sqm.VideoInfo(video_id=vid_id,
                              channel=channel_name,
                              video_title=video_name,
                              sentiment_score_average=score,
                              negative_entries=rand.randint(1, 1000),
                              positive_entries=rand.randint(1, 1000),
                              neutral_entries=rand.randint(1, 1000),
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
    video = sqm.VideoInfo(video_id="lfKfPfyJRdk",
                          channel="Belogus",
                          video_title="A video",
                          sentiment_score_average=0.93,
                          negative_entries=5,
                          positive_entries=93,
                          neutral_entries=2,
                          date_updated=str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                          )

    video = sqm.Users(user_name="Admin",
                      password="Admin",
                      email="admin@ytsa_gsu.com"
                      )
    db.session.add(video)
    db.session.commit()


def add_live_test_vids():
    """_summary_
    # Incomplete
    # Adds a few non-random entries for specific testing
    """
    # Random videos for testing purposes. Real vid ids and titles.
    vid_info = [['HI8Zg4vC5II', 'Isaac Arthur',
                 'The Fermi Paradox: Galactic Habitable Zones'],
                ['3Qb_0Vw4_t4', 'Motivation Mentors',
                 'Andrew Tate About Women | TikTok Compilation'],
                ['xnHOjiZq-ks', 'TikTok - Funny',
                 'Best Funny Dogs And Cats Videos 😅 - Funniest Animals Videos 2023😇 #1'],
                ['rqS2vFuU6SE', 'International Cat',
                 '1 HOUR FUNNY CATS COMPILATION 2022😂| Cute And Lovely Cat Videos 2022😹'],
                ['rd5U06HxHwY', 'Abrish Funny TikTok',
                 'Best Funny Dogs And Cats Videos 😂 Funniest Animals Videos 2023 😇 | PART 29 |']]

    for vid in vid_info:
        # print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        video = sqm.VideoInfo(video_id=vid[0],
                              channel=vid[1],
                              video_title=vid[2],
                              sentiment_score_average=rand.random(),
                              negative_entries=rand.randint(1, 1000),
                              positive_entries=rand.randint(1, 1000),
                              neutral_entries=rand.randint(1, 1000),
                              date_updated=str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                              )
        channel = sqm.Channels(
            channel=vid[1],
            sentiment_score_average=rand.random(),
            date_updated=str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        )
        db.session.add(video)
        db.session.add(channel)
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
        db_user (User): username from database
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


def is_new_user(user_name):
    """
    Verifies if user name is already in DB
    Args:
        user_name: str

    Returns: Bool

    """
    if db.session.query(sqm.Users.id).filter_by(user_name=user_name).first() is None:
        return True
    return False


def is_new_email(email):
    """
    Verifies if email is already in DB
    email is a unique field so they cannot be in duplicate.
    Args:
        email: str

    Returns: Bool

    """
    if db.session.query(sqm.Users.id).filter_by(email=email).first() is None:
        return True
    return False


def register_user(user_name, password_entered, email):
    """_Summary_
    Sets up User in database if valid credentials
    and not already existing
    Args:
        user_name: string
        password_entered: string
        email: string

    Returns: True for success, False for failure (user is already in DB
    """
    password_entered = hash_password(password_entered)
    email = email.lower()

    if is_new_user(user_name) and is_new_email(email):
        usr = sqm.Users(user_name=user_name,
                        password=password_entered,
                        email=email
                        )
        db.session.add(usr)
        db.session.commit()
        return True
    return False


if __name__ == '__main__':
    generate_random_vid_id()
