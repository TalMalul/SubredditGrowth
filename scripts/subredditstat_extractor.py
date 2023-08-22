
import tqdm
import time
from SubredditStats import SubredditStats

def extract_subreddits(subreddits_names):
    subreddits_stats = {}

    for subreddit_name in tqdm(subreddits_names):
        try:
            subreddit_stat = SubredditStats(subreddit_name)
            subreddits_stats[subreddit_name] = subreddit_stat
        except:
            pass
        time.sleep(7)

    return subreddits_stats

