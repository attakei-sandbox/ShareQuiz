# -*- coding:utf8 -*-
"""ShareQuiz サーバーサイドAPI
"""
from datetime import datetime
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
