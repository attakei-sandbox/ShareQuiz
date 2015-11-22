# -*- coding:utf8 -*-
"""ShareQuiz サーバーサイドAPI
"""
__version__ = '0.0.1'


def fetch_current_articles(event, context):
    '''記事リストを返す

    :param event:
    :param context:
    :return:
    '''
    # TODO: It is a stub
    return {
        'articles': [
            {
                'url': 'http://example.com/1',
                'title': 'test title 1',
                'description': 'test site is now developing 1.',
                'site': {
                    'url': 'http://example.com/',
                    'title': 'Example title'
                },
            },
            {
                'url': 'http://example.com/2',
                'title': 'test title 2',
                'description': 'test site is now developing 2.',
                'site': {
                    'url': 'http://example.com/',
                    'title': 'Example title'
                },
            },
        ]
    }