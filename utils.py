import requests
import json
from langchain_core.documents import Document
from chains import analytics_chain
from dotenv import load_dotenv
load_dotenv()
def get_tweet_pid(tweet_url):
    tweet_id = tweet_url.split('/')[-1]
    url = f'https://twitter241.p.rapidapi.com/tweet?pid={tweet_id}'
    headers = {
        'x-rapidapi-host': 'twitter241.p.rapidapi.com',
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }
    tweet_data = requests.get(url, headers=headers)
    tweet_data = json.loads(tweet_data.text)
    return {
        "post_content": tweet_data['tweet']['full_text'],
        "likes": tweet_data['tweet']['favorite_count'],
        "hashtags": tweet_data['tweet']['entities']['hashtags'],
        "retweets": tweet_data['tweet']['retweet_count'],
        "bookmarks": int(tweet_data['tweet']['bookmark_count']),
        "views": int(tweet_data['views']),
        "id": tweet_id
    }

def get_unique_hashtags(res, tweet_data):
    old_hashtags = res.metadata.get('hashtags', '').split(', ') if res.metadata.get('hashtags') else []

    new_hashtags = [hashtag['text'] for hashtag in (tweet_data.get('hashtags', []) or [])]

    old_hashtags = [tag.strip() for tag in old_hashtags]
    new_hashtags = [tag.strip() for tag in new_hashtags]

    return ', '.join(list(set(new_hashtags) - set(old_hashtags)))


def create_tweet_document(tweet_data):
    return Document(
        page_content=tweet_data['post_content'],
        metadata={
            "likes": tweet_data['likes'],
            "hashtags": ', '.join([hashtag['text'] for hashtag in tweet_data['hashtags']]),
            "retweets": tweet_data['retweets'],
            "bookmarks": tweet_data['bookmarks'],
            "views": tweet_data['views'],
            "ids": tweet_data['id']
        },
        id=tweet_data['id']
    )

def create_updated_tweet(res, tweet_data, unique_points):
    return Document(
        document_id=res.id,
        metadata={
            "views": (tweet_data['views'] + res.metadata['views']) / 2,
            "hashtags": get_unique_hashtags(res, tweet_data),
            "bookmarks": tweet_data['bookmarks'] + res.metadata['bookmarks'],
            "ids": res.metadata['ids'] + ',' + tweet_data['id'],
            "likes": (tweet_data['likes'] + res.metadata['likes']),
            "retweets": (tweet_data['retweets'] + res.metadata['retweets'])
        },
        page_content=unique_points
    )


def get_tweet_with_analytics(doc:Document):
    analytics = analytics_chain.invoke({
        "tweet_content": doc.page_content
    })

    return {
        # "id": doc.id,
        "ids": doc.metadata['ids'],
        "content": doc.page_content,
        "likes": doc.metadata['likes'],
        "hashtags": doc.metadata['hashtags'].split(', '),
        "engagement": {
            "retweets": doc.metadata['retweets'],
            "bookmarks": doc.metadata['bookmarks'],
            "views": doc.metadata['views']
        },
        "sentiment": analytics.sentiment,
        "tone": analytics.tone,
        "tags": analytics.tags,
        "summary": analytics.summary
    }
