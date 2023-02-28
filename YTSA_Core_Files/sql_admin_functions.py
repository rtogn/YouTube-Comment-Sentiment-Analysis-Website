import YTSA_Core_Files.sql_models as sql_models
from YTSA_Core_Files.sql_models import db
import random as rand
from string import ascii_letters
from time import gmtime, strftime

def generateRandomVidID():
    videoID = ""
    for i in range(0,11):
        character = rand.choice(ascii_letters)
        videoID += character
    return videoID


def sql_add_demo_data_random(num_entries):
    # Must pass db object to use function
    # adds num_entries amount of randomly generated videos/etc to the database
    test_channels = ["channel_00", "channel_01", "channel_02", "channel_04", "channel_05"]
    for v in range(0, num_entries):
        vid_id = generateRandomVidID()
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
    # Incomplete
    # Adds a few non-random entries for specific testing
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
    # Not implemented
    return password

def decrypt_password(password):
    # Not implemented
    return password

def validate_login(db_user, password_entered):
    # If selection was empty return False
    if db_user is None:
        return False
    db_password = decrypt_password(db_user.password)
    if password_entered == db_password:
        return True
    return False

if __name__ == '__main__':
    generateRandomVidID()