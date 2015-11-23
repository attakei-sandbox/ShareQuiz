# -*- coding:utf8 -*-
"""ShareQuiz サーバーサイドAPI
"""
from datetime import datetime
import time
import boto3


def fetch_current_articles(event, context):
    """記事リストを返す

    :param event:
    :param context:
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sharequiz-dev-articles')
    
    now_string = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    results = table.scan(
        IndexName='published_date-index',
        Select='ALL_ATTRIBUTES',
        Limit=100,
        ScanFilter={
            'published_date': {
                'AttributeValueList': [
                    now_string
                ],
                'ComparisonOperator': 'LT',
            }
        },
    )
    articles = results.get('Items')
    articles.sort(key=lambda art: art['published_date'], reverse=True)

    return {
        'articles': articles
    }


def fetch_articles_from_sites(event, context):
    """登録されているサイト情報から、記事を取得させる。

    :param event:
    :param context:
    :return:
    """
    import feedparser

    def _find_published_date(entry):
        if hasattr(entry, 'published_parsed'):
            parsed_date = entry.published_parsed
        elif hasattr(entry, 'updated_parsed'):
            parsed_date = entry.updated_parsed
        else:
            return '2000-12-31T23:59:59+09:00'
        if time.strftime('%Z', parsed_date) == 'JST':
            tz = '+09:00'
        else:
            tz = '+00:00'
        return time.strftime('%Y-%m-%dT%H:%M:%S' + tz, parsed_date)

    dynamodb = boto3.resource('dynamodb')

    # サイトを取得する
    _table = dynamodb.Table('sharequiz-dev-sites')
    _results = _table.scan()
    sites = _results.get('Items')

    # サイトから記事を全部取得する
    articles = []
    for site in sites:
        try:
            dom = feedparser.parse(site['feed_url'])
        except (TypeError) as ex:
            print(ex)
            return None
        for entry in dom['entries']:
            article = {
                'id': entry.link,
                'url': entry.link,
                'title': entry.title,
                'description': entry.summary,
                'published_date': _find_published_date(entry),
                'site': site,
            }
            articles.append(article)

    # まとめてDBに登録する
    _table = dynamodb.Table('sharequiz-dev-articles')
    with _table.batch_writer() as _batch:
        for article in articles:
            _batch.put_item(Item=article)

    return 'OK'
