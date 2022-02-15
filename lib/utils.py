from datetime import datetime


def format_data(raw):
    retweeted_user = None
    retweeted_id = None
    retweeted_profile_pict = None
    is_retweet = False

    media, media_type = get_media(raw)
    retweeted_count = raw['retweet_count']
    reply_count = raw['reply_count']
    like_count = raw['favorite_count']

    if 'retweeted_status' in raw:
        is_retweet = True
        retweeted_user = raw['retweeted_status']['user']['screen_name']
        retweeted_id = raw['retweeted_status']['id_str']
        retweeted_profile_pict = raw['retweeted_status']['user']['profile_image_url_https'].replace("normal", "400x400")
        retweeted_count = raw['retweeted_status']['retweet_count']
        reply_count = raw['retweeted_status']['reply_count']
        like_count = raw['retweeted_status']['favorite_count']

    impression = retweeted_count + reply_count + like_count

    json_data = {
        'tweetId': int(raw['id_str']),
        'text': get_text(raw),
        'source': raw['source'],
        'initiator': raw['user']['screen_name'],
        'initiatorName': raw['user']['name'],
        'profilePict': raw['user']['profile_image_url_https'].replace("normal", "400x400"),
        'potentialReach': raw['user']['followers_count'],
        'hashtags': get_hashtags(raw),
        'mentions': get_mentions(raw),
        'retweetedUser': retweeted_user,
        'retweetedId': retweeted_id,
        'retweetedProfilePict': retweeted_profile_pict,
        'isRetweet': is_retweet,
        'media': media,
        'mediaType': media_type,
        'retweetCount': retweeted_count,
        'replyCount': reply_count,
        'favoriteCount': like_count,
        'impression': impression,
        'createdAt': get_created_at(raw),
        'crawledAt': datetime.utcnow(),
        'place': get_place(raw),
        'lang': 'id' if raw['lang'] == 'in' else raw['lang'],
    }
    return json_data


def get_hashtags(raw):
    try:
        hashtags = [tag['text'] for tag in raw['extended_tweet']['entities']['hashtags']]
    except:
        hashtags = [tag['text'] for tag in raw['entities']['hashtags']]

    return hashtags


def get_text(raw):
    try:
        text = raw['extended_tweet']['full_text']
    except:
        text = raw['text']

    return text


def get_mentions(raw):
    try:
        mentions = [mention['screen_name'] for mention in raw['extended_tweet']['entities']['user_mentions']]
    except:
        mentions = [mention['screen_name'] for mention in raw['entities']['user_mentions']]
    return mentions


def get_media(data):
    result = []
    media_type = None
    if 'extended_entities' in data:
        if 'media' in data['extended_entities']:
            media = data['extended_entities']['media']
            if media[0]['type'] == "video":
                media_type = "video"
                for video in media[0]['video_info']['variants']:
                    if video['content_type'] == "video/mp4":
                        result.append(video['url'])
                        break
            elif media[0]['type'] == "animated_gif":
                media_type = "gif"
                for gif in media[0]['video_info']['variants']:
                    if gif['content_type'] == "video/mp4":
                        result.append(gif['url'])
                        break
            elif media[0]['type'] == "photo":
                media_type = "photo"
                for image in media:
                    result.append(image['media_url_https'])
    return result, media_type


def get_place(data):
    if data['place']:
        place = {
            'id': data['place']['id'],
            'name': data['place']['name'],
            'point': None
        }
        return place
    else:
        return None


def get_created_at(raw):
    return datetime.strptime(raw['created_at'], "%a %b %d %H:%M:%S %z %Y")
