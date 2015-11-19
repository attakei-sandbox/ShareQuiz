# -*- coding:utf8 -*-
"""デプロイスクリプトのフロントエンド

プロジェクトrootでfabコマンドを実行できるようにするためのfabfileです。

最初はこのファイルへ追加していって問題無いですが、ある程度溜まってきたら分割検討してください。
"""
import os
import logging
import glob
import boto3


Logger = logging.getLogger('deploy')
Session = boto3.Session(profile_name='attakei')


def deploy_www():
    """www系のデプロイ
    
    * 事前にデプロイ先のバケットは作成してください
    """
    # デプロイ対象の選定
    logger = Logger.getChild('deploy_www')
    src_dir = './www/dist'
    logger.info('source folder: {}'.format(src_dir))
    dest_bucket = 'sharequiz-prod'
    logger.info('destination bucket: {}'.format(dest_bucket))
    dest_dir = 'www'
    logger.info('destination folder: {}'.format(dest_dir))

    # 全部デプロイする
    # TODO: 無変更なものをデプロイせずに済む方法を探す
    s3 = Session.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    for file_path in glob.iglob(src_dir+'/*'):
        file_name = os.path.basename(file_path)
        bucket.upload_file(file_path, '{}/{}'.format(dest_dir, file_name))
