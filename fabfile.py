# -*- coding:utf8 -*-
"""デプロイスクリプトのフロントエンド

プロジェクトrootでfabコマンドを実行できるようにするためのfabfileです。

最初はこのファイルへ追加していって問題無いですが、ある程度溜まってきたら分割検討してください。
"""
import os
import logging
import glob
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
    src_dir = './www/dist'
    logger.info('source folder: {}'.format(src_dir))
    dest_bucket = 'sharequiz-{}'.format(env)
    logger.info('destination bucket: {}'.format(dest_bucket))
    dest_dir = ''
    logger.info('destination folder: {}'.format(dest_dir))

    # 全部デプロイする
    # TODO: 無変更なものをデプロイせずに済む方法を探す
    s3 = Session.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    for file_path in glob.iglob(src_dir+'/*'):
        file_name = os.path.basename(file_path)
        bucket.upload_file(
            file_path,
            # TODO: フォルダアップロードすること
            file_name,
            ExtraArgs={
                'ACL': 'public-read',
                # TODO: ContentTypeを拡張して判別しておくこと
                'ContentType': 'text/html',
            }
        )
