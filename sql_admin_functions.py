import sql_models
import random as rand
from string import ascii_letters
from datetime import datetime

def generateRandomVidID():
    videoID = ""
    for i in range(0,11):
        character = rand.choice(ascii_letters)
        videoID += character
    return videoID


def sql_add_demo_data_random(db, num_entries):
    # Must pass db object to use function
    # adds num_entries amount of randomly generated videos/etc to the database
    top_Vids = []
    for v in range(0, num_entries):
        vid_id = generateRandomVidID()
        score = rand.random()
        video_name = "Test_Video_" + str(v)
        channel_name = "Test_Channel_" + str(v)
        date_today = str(datetime.now)
        video = sql_models.Video_Info(video_id=vid_id,
                                      channel= channel_name,
                                      video_tite = video_name,
                                      sentiment_score_average=score,
                                      entry_count=rand.randint(1,5500),
                                      date_updated= date_today
                                      )

        # Add the first 5 as top 5 just for consistency.
        if v < 5:
            topVids = sql_models.Top_Videos(video_id=vid_id,
                                            sentiment_score_average=score,
                                            entry_count=rand.randint(1, 550),
                                            date_updated=date_today
                                    )
            db.session.add(topVids)
        db.session.add(video)

    db.session.commit()

def sql_add_demo_data_testing(db):
    # Incomplete
    # Adds a few non-random entries for specific testing
    video = sql_models.Video_Info(video_id="lfKfPfyJRdk",
                                  channel="Belogus",
                                  sentiment_score = 0.93,
                                  comments_analyzed_count = 120,
                                  date_updated = str(datetime.now)
                                  )


    db.session.add(video)
    db.session.commit()



if __name__ == '__main__':
    generateRandomVidID()