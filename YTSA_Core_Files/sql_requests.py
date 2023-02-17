import sql_models

def update_sentiment_average(target_entry, new_score):
    # Generic function to update any runnign sentiment score average
    # Can work for channel or per video (in top vids) scores
    assert new_score >= 0.0 and new_score <= 1.0
    curAvrg = target_entry.sentiment_score_average
    entry_count = target_entry.entry_count
    sum = (curAvrg * entry_count)
    sum += new_score
    entry_count += 1

    # update average and count of contributing entries
    target_entry.sentiment_score_average = sum / entry_count
    target_entry.entry_count = entry_count

