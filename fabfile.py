# -*- coding:utf8 -*-
"""デプロイスクリプトのフロントエンド

プロジェクトrootでfabコマンドを実行できるようにするためのfabfileです。

最初はこのファイルへ追加していって問題無いですが、ある程度溜まってきたら分割検討してください。
"""
import os
import logging
import boto3
from fabric.api import lcd, local


Session = boto3.Session(profile_name='sharequiz')

Logger = logging.getLogger('deploy')
Logger.setLevel(logging.DEBUG) # or whatever
Logger.addHandler(logging.StreamHandler())


def clean_lib():
    """lib系のクリーンアップ実行
    """
    with lcd('./lib'):
        local('rm -rf ./dist')
        local('mkdir ./dist')


def build_lib():
    """lib系のパッケージング
    """
    import zipfile
    logger = Logger.getChild('deploy_lib')
    # パッケージング対象の特定
    src_dir = './lib/build'
    with lcd('./lib'):
        # local('python setup.py sdist')
        local('pip install -t ./build -r requirements.txt')
        local('pip install -U -t ./build . ')
        local('cp ./handlers.json ./build/')
    targets = []
    for file_path in _glob_recursive(src_dir):
        file_name = os.path.basename(file_path)
        file_ext = file_name.split('.')[-1]
        packed_name = file_path.replace(src_dir + '/', '')
        if os.path.isdir(file_path):
            logger.debug('Skip: {} (directory)'.format(file_path))
            continue
        if file_name in ('.DS_Store', '.gitignore'):
            logger.debug('Skip: {} (ignored)'.format(file_path))
            continue
        if file_ext in ('pyc', ):
            logger.debug('Skip: {} (ignored)'.format(file_path))
            continue
        logger.debug('Target: {} -> {}'.format(file_path, packed_name))
        targets.append((file_path, packed_name))
    # パッケージの作成
    package_file = './lib/dist/sharequiz.zip'
    with zipfile.ZipFile(package_file, 'w') as zfp:
        for target_file, target_name in targets:
            zfp.write(target_file, target_name)


def deploy_lib(env=None):
    """www系のデプロイ
    
    * 事前にデプロイ先のバケットは作成してください
    """
    logger = Logger.getChild('deploy_lib')
    # env確定
    if env is not None:
        pass
    elif 'DEPLOY_ENV' in os.environ:
        env = os.environ['DEPLOY_ENV']
    else:
        env = 'dev'
    # デプロイ対象の選定
    dest_bucket = 'sharequiz-{}'.format(env)
    # デプロイする
    s3 = Session.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    bucket.upload_file(
        'lib/dist/sharequiz.zip',
        '_lib/sharequiz.zip',
    )


def clean_www():
    """www系のクリーンアップ実行
    """
    with lcd('./www'):
        local('npm install')
        local('npm run clean')


def build_www():
    """www系のビルド実行
    """
    with lcd('./www'):
        local('npm install')
        local('npm run build')


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
    src_dir = './www/lib/'
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
        file_name = os.path.basename(file_path)
        file_s3_key = file_path.replace(src_dir, '')
        if os.path.isdir(file_path):
            logger.debug('Skip: {} (directory)'.format(file_path))
            continue
        if file_name in ('.DS_Store'):
            logger.debug('Skip: {} (ignored)'.format(file_path))
            continue
        logger.debug('Copy: {} -> {}'.format(file_path, file_s3_key))
        bucket.upload_file(
            file_path,
            file_s3_key,
            ExtraArgs={'ACL': 'public-read', 'ContentType': _detect_mime(file_path)}
        )


def release_www():
    client = Session.client('cloudfront')
    destribution_id = 'EXEXJ7BAF1AJN'
    client.create_invalidation(
        DistributionId=destribution_id,
        InvalidationBatch={
            'Paths': {
                'Items': ['/*'],
                'Quantity': 1,
            },
            'CallerReference': 'Purge all resources',
        }
    )


def local_server():
    with lcd('www'):
        local('gulp watch & python -m SimpleHTTPServer')


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
    if ext == 'js':
        return 'application/javascript'
    if ext == 'json':
        return 'application/json'
    return 'application/octet-stream'
