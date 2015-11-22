# -*- coding:utf8 -*-
"""ShareQuiz サーバーサイドAPI
"""
__version__ = '0.0.1'


import boto3


def fetch_current_articles(event, context):
    '''記事リストを返す

    :param event:
    :param context:
    :return:
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sharequiz-dev-articles')
    
    results = table.scan()
    # TODO: It is a stub
    return {
        'articles': results.get('Items')
    }
