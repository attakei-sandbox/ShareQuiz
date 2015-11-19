# -*- coding:utf8 -*-
"""デプロイスクリプトのフロントエンド

プロジェクトrootでfabコマンドを実行できるようにするためのfabfileです。

最初はこのファイルへ追加していって問題無いですが、ある程度溜まってきたら分割検討してください。
"""
import os
import logging
import boto3


Session = boto3.Session(profile_name='sharequiz')

Logger = logging.getLogger('deploy')
Logger.setLevel(logging.INFO) # or whatever
Logger.addHandler(logging.StreamHandler())


def deploy_www(env=None):
    """www系のデプロイ
    
    * 事前にデプロイ先のバケットは作成してください
    """
    # env確定
    if env is not None:
        pass
    elif 'DEPLOY_ENV' in os.environ:
        env = os.environ['DEPLOY_ENV']
    else:
        env = 'dev'
    # デプロイ対象の選定
    logger = Logger.getChild('deploy_www')
    src_dir = './www/dist/'
    logger.info('source folder: {}'.format(src_dir))
    dest_bucket = 'sharequiz-{}'.format(env)
    logger.info('destination bucket: {}'.format(dest_bucket))
    dest_dir = ''
    logger.info('destination folder: {}'.format(dest_dir))

    # 全部デプロイする
    # TODO: 無変更なものをデプロイせずに済む方法を探す
    s3 = Session.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    for file_path in _glob_recursive(src_dir):
        file_s3_key = file_path.replace(src_dir, '')
        if os.path.isdir(file_path):
            continue
        bucket.upload_file(
            file_path,
            file_s3_key,
            ExtraArgs={'ACL': 'public-read', 'ContentType': _detect_mime(file_path)}
        )


# Thanks for http://qiita.com/suin/items/cdef17e447ceeff6e79d
def _glob_recursive(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


def _detect_mime(file_name):
    ext = os.path.basename(file_name).split('.')[-1]
    if ext == 'html':
        return 'text/html'
    if ext == 'css':
        return 'text/css'
    return 'application/octet-stream'