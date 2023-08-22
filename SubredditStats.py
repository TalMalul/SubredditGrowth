import json
import requests
from bs4 import BeautifulSoup

class SubredditStats:
    def __init__(self, name, data = None):
        self._name = name
        self._url = 'https://subredditstats.com/r/{}'.format(self._name)
        if data is None:
          self._data = self._query(self._url)
        else:
          self._data = data

    def _query(self, url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        return json.loads(soup.find('script', {'id': 'embeddedSubredditData'}).text)


    def _time_series(self, series_type, value_name):
        day_to_sec = lambda day: day * 24 * 60 * 60
        sorted_values = list(sorted(self._data[series_type], key=lambda d: int(d['utcDay'])))
        sorted_seconds = [{'utcDay': day_to_sec(d['utcDay']), 'count': d[value_name]} for d in sorted_values]
        return sorted_seconds

    def avg_subsribers_per_day(self):
        spd = self.subscriber_count_time_series()
        return (spd[-1]['count'] - spd[0]['count']) / (spd[-1]['utcDay'] / 24 / 60 / 60 - spd[0]['utcDay'] / 24 / 60 / 60)

    def avg_posts_per_day(self):
        ppd = self.posts_per_day_time_series()
        return (ppd[-1]['count'] - ppd[0]['count']) / (ppd[-1]['utcDay'] / 24 / 60 / 60 - ppd[0]['utcDay'] / 24 / 60 / 60)


    @property
    def name(self):
        return self._name

    def subscriber_count_time_series(self):
        return self._time_series('subscriberCountTimeSeries', 'count')

    def posts_per_day_time_series(self):
        return self._time_series('postsPerHourTimeSeries', 'postsPerHour')

    def comments_per_day_rank_time_series(self):
        return self._time_series('commentsPerHourRankTimeSeries', 'rank')

    def comments_per_day_time_series(self):
        return self._time_series('commentsPerHourTimeSeries', 'commentsPerHour')

    def n_subscribers(self):
        return self._data['subscriberCount']

    def subscribers_rank(self):
        return self._data['subscriberCountRank']

    def posts_per_subscriber(self):
        return self._data['postsPerSubscriber']

    def posts_per_hour(self):
        return self._data['postsPerHour']

    def posts_per_hour_rank(self):
        return self._data['postsPerHourRank']

    def mentions_per_day(self):
        return self._data['mentionsPerDay']

    def mentions_per_day_rank(self):
        return self._data['mentionsPerDayRank']

    def creation_time(self):
        return self._data['creationTime']

    def description(self):
        return self._data['description']

    def comments_per_subscriber(self):
        return self._data['commentsPerSubscriber']

    def comments_per_subscriber_rank(self):
        return self._data['commentsPerSubscriberRanked']

    def comments_per_hour(self):
        return self._data['commentsPerHour']

    def comments_per_hour_rank(self):
        return self._data['commentsPerHourRank']

    def top_commenters_by_frequency(self):
        return self._data['topCommentersByFrequency']

    def top_commenters_by_score_sum(self):
        return self._data['topCommentersByScoreSum']

    def top_keywords(self):
        return self._data['topKeywords']

    def top_linked_domains(self):
        return self._data['topLinkedDomains']

    def top_posters_by_frequency(self):
        return self._data['topPostersByFrequency']

    def top_posters_by_score_sum(self):
        return self._data['topPostersByScoreSum']

    def top_posts_comments_sum(self):
        return self._data['topPostsCommentsSum']

    def top_posts_comments_sum_rank(self):
        return self._data['topPostsCommentsSumRank']

    def top_posts_gilded_sum(self):
        return self._data['topPostsGildedSum']

    def top_posts_gilded_sum_rank(self):
        return self._data['topPostsGildedSumRank']

    def top_posts_score_sum(self):
        return self._data['topPostsScoreSum']

    def top_posts_score_sum_rank(self):
        return self._data['topPostsScoreSumRank']

    def comments_per_subscriber_rank(self):
        return self._data['commentsPerSubscriberRank']

    def posts_per_subscriber_rank(self):
        return self._data['postsPerSubscriberRank']

    def gilds_per_subscriber(self):
        return self._data['gildsPerSubscriber']

    def gilds_per_subscriber_rank(self):
        return self._data['gildsPerSubscriberRank']

    def subreddit_id(self):
        return self._data['subredditId']

    def quarantined(self):
        return self._data['quarantined']

    def is_active_subreddit(self):
        return self._data['isActiveSubreddit']

