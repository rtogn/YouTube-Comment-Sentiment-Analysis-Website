"""_summary_
SQL request functions
Returns:
    _type_: _description_
"""
from time import gmtime, strftime
from sqlalchemy import desc
import YTSA_Core_Files.sql_models as sqm
from YTSA_Core_Files.sql_models import db

def count_comment_entries(target_entry):
    """_summary_
    # Return sum of pos, neg and neutral counts of comments.
    Args:
        target_entry (_type_): _description_

    Returns:
        _type_: _description_
    """
    return target_entry.negative_entries\
            + target_entry.positive_entries\
            + target_entry.neutral_entries


def update_sentiment_average_channel(channel_name):
    """_summary_
    # add channel if it does not exist.

    Args:
        channel_name (_type_): _description_
    """

    if db.session.query(sqm.Channels.id).filter_by(channel=channel_name).first() is None:
        date_today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        cur_channel = sqm.Channels(channel=channel_name,
                                          sentiment_score_average=0.0,
                                          date_updated=date_today
                                          )
        db.session.add(cur_channel)
        db.session.commit()

    # Get channel from DB
    target_channel = db.session.execute(db.select(sqm.Channels).filter_by(
        channel=channel_name)).scalar_one()

    # Get list of videos with that channel, then calculate average score based of those scores
    vids = sqm.VideoInfo.query.filter_by(channel=channel_name)
    contributors = vids.count()
    avrg_sum = 0
    for vid in vids:
        avrg_sum += vid.sentiment_score_average
    target_channel.sentiment_score_average = avrg_sum / contributors

def set_sent_arvrg_video(video_id, new_score):
    """_summary_
    # Generic function to update any running sentiment score average of a video
    # Can work for channel or per video (in top vids) scores
    Args:
        video_id (_type_): _description_
        new_score (_type_): _description_
    """

    assert new_score >= -1
    assert new_score <= 1.0
    target_entry = db.session.execute(db.select(sqm.VideoInfo).filter_by(
        video_id=video_id)).scalar_one()

    cur_avrg = target_entry.sentiment_score_average
    entry_count = count_comment_entries(target_entry)
    sum_score = cur_avrg * entry_count
    sum_score += new_score
    entry_count += 1

    # update average and count of contributing entries
    target_entry.sentiment_score_average = sum_score / entry_count
    target_entry.entry_count = entry_count
    # Update overall score for that channel with this videos score.
    # (if this bogs time down queue it when the DB starts or periodically.
    update_sentiment_average_channel(target_entry.channel)

def add_video(vid_id, vid_dict, new_score):
    """Add a video to DB if not already
        present
    Args:
        vid_info (_type_): dict of items needed
    """
    if db.session.query(sqm.VideoInfo.id).filter_by(video_id=vid_id).first() is None:
        date_today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        vid = sqm.VideoInfo(video_id=vid_id,
                            video_title=vid_dict["video_title"],
                            #subscriber_count=vid_dict["subscriber_count"],
                            comment_count=vid_dict["comment_count"],
                            like_count=vid_dict["like_count"],
                            channel=vid_dict["channel_title"],
                            #author_displayname=vid_dict["author_display_name"],
                            #authorProfileImageUrl=vid_dict["author_profile_image_url"],
                            #text_display=vid_dict["text_display"],
                            sentiment_score_average=new_score,
                            date_updated=date_today
                            )
        db.session.add(vid)
        db.session.commit()

def get_top_five():
    """_summary_
    Returns top 5 videos from all video tables by sentiment score.
    Returns:scalars
        _type_: query object, iterable
    """
    # Get list of videos with that channel, then calculate average score based of those scores
    vi = sqm.VideoInfo
    vid_avg = sqm.VideoInfo.sentiment_score_average
    vids = db.session.execute(db.select(vi).order_by(desc(vid_avg))).scalars().all()[:5]
    return vids
