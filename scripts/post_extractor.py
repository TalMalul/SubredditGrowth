import praw
import time
import datetime
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Extract data using reddit api")
parser.add_argument('--func_type', help='post function', type=str, required=True)
parser.add_argument('--subreddit', help='subreddit name', type=str, required=True)
parser.add_argument('--output_folder', help='subreddit name', type=str, required=True)

options = parser.parse_args()

print("func_type = " + options.func_type)
print("subreddit = " + options.subreddit)
print("output_folder = " + options.output_folder)


def get_function(func_type):
    if func_type == 'new':
        return subreddit.new
    elif func_type == 'top':
        return subreddit.top
    elif func_type == 'hot':
        return subreddit.hot
    elif func_type == 'controversial':
        return subreddit.controversial

def get_data(subreddit, subreddit_name, func_type, output_folder):
    
    func = get_function(func_type)
    
    post_data = []
    post_counter = 0
    
    for submission in func(limit=None):
        post_counter += 1
        
        try:
            submission_author = submission.author
            author_name = submission_author.name
            author_karma = submission_author.comment_karma
            ups = submission.ups
            downs = submission.downs
        except AttributeError:
            continue
        post_data.append({
            "type": func_type,
            "created_utc": submission.created_utc,
            "num_comments": submission.num_comments,
            "author_name": author_name,
            "author_karma":author_karma,
            "ups": ups,
            "downs": downs
            # Add more relevant data as needed
        })
        comment_data = []
        submission.comments.replace_more(limit=None)
        time.sleep(10)
        for comment in submission.comments.list():
            try:
                comment_author = comment.author
                author_name = comment_author.name
                author_karma = comment_author.comment_karma
                ups = comment.ups
                downs = comment.downs
            except AttributeError:
                continue
            comment_data.append({
              "type": func_type,
              "created_utc": comment.created_utc,
              "author_name": author_name,
              "author_karma":author_karma,
              "ups": ups,
              "downs": downs
              # Add more relevant data as needed
            })
            time.sleep(10)
        post_data[-1]['comment_data'] = comment_data
        if post_counter % 10 == 0:
            post_df = pd.DataFrame(post_data)
            post_df.to_json(f"{output_folder}/{subreddit_name}_{post_counter - 10}_{post_counter - 1}_{func_type}.json", orient='records')
            post_data.clear()
            
    post_df = pd.DataFrame(post_data)
    post_df.to_json(f"{output_folder}/{subreddit_name}_{post_counter - len(post_data)}_{post_counter - 1}_{func_type}.json", orient='records')
            

reddit = praw.Reddit(
    client_id='2Ec7bj2Da416DUCzDhLFLg',
    client_secret='kg-6-uhrV2j_DNiTSSsqAnGEalBAxg',
    user_agent='growth_data/Accomplished_Cry6473'
)

subreddit = reddit.subreddit(options.subreddit)
new_comment_data, new_post_data = get_data(subreddit, options.subreddit, options.func_type, options.output_folder)
    

