from storages.backends.s3boto3 import S3Boto3Storage


class CustomStorage(S3Boto3Storage):
    def __init__(self):
        super(CustomStorage, self).__init__()


custom_storage = CustomStorage()
