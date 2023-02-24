import YTSA_Core_Files.sql_models as sql_models
from YTSA_Core_Files.sql_models import db
from time import gmtime, strftime


def count_comment_entries(target_entry):
    # Return sum of pos, neg and neutral counts of comments.
    return target_entry.negative_entries + target_entry.positive_entries + target_entry.neutral_entries


def update_sentiment_average_channel(channel_name):
    # add channel if it does not exist.

    if db.session.query(sql_models.Channels.id).filter_by(channel=channel_name).first() is None:
        date_today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        cur_channel = sql_models.Channels(channel=channel_name,
                                          sentiment_score_average=0.0,
                                          date_updated=date_today
                                          )
        db.session.add(cur_channel)
        db.session.add(cur_channel)
        db.session.commit()

    # Get channel from DB
    target_channel = db.session.execute(db.select(sql_models.Channels).filter_by(
        channel=channel_name)).scalar_one()

    # Get list of videos with that channel, then calculate average score based of those scores
    vids = sql_models.Video_Info.query.filter_by(channel=channel_name)
    contributors = vids.count()
    avrg_sum = 0
    for vid in vids:
        avrg_sum += vid.sentiment_score_average
    target_channel.sentiment_score_average = avrg_sum / contributors

def update_sentiment_average_video(target_entry, new_score):
    # Generic function to update any runnign sentiment score average
    # Can work for channel or per video (in top vids) scores
    assert new_score >= -1 and new_score <= 1.0
    curAvrg = target_entry.sentiment_score_average
    entry_count = count_comment_entries(target_entry)
    sum = (curAvrg * entry_count)
    sum += new_score
    entry_count += 1

    # update average and count of contributing entries
    target_entry.sentiment_score_average = sum / entry_count
    target_entry.entry_count = entry_count
    # Update overall score for that channel (if this bogs time down queue it when the DB starts or periodically.
    update_sentiment_average_channel(target_entry.channel)


def update_top_five():
    # Not implemented
    return 0
