import twitter
from datetime import datetime
from twitter_text import TwitterText

from django.db import models
from django.utils.timezone import utc


class TwitterAccount(models.Model):
    user_name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=511, null=True, blank=True)

    @property
    def latest_tweet(self):
        try:
            return self.tweets.all()[0]
        except IndexError:
            return False

    @property
    def latest_3_tweets(self):
        try:
            return self.tweets.all()[:3]
        except IndexError:
            return False

    def update(self):
        api = twitter.Api()
        tweets = api.GetUserTimeline(self.user_name)
        user = api.GetUser(self.user_name)

        if user.profile_image_url != self.image_url:
            self.image_url = user.profile_image_url
            self.save()

        for tweet in tweets:
            tw, new = Tweet.objects.get_or_create(tweet_id=tweet.id,
                defaults={
                    'account': self,
                    'created_at': datetime.fromtimestamp(
                        tweet.created_at_in_seconds).replace(tzinfo=utc),
                    'text': tweet.text
                })
            if new:
                tw.save()

    def __unicode__(self):
        return self.user_name


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    account = models.ForeignKey(TwitterAccount, related_name='tweets')
    created_at = models.DateTimeField()
    text = models.TextField()

    @property
    def html(self):
        tt = TwitterText(self.text)
        tt.autolink.auto_link()
        return mark_safe(tt)

    def __unicode__(self):
        return '{}'.format(self.tweet_id)

    class Meta:
        ordering = ('-created_at',)