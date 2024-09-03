from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    # @property
    # def location(self):
    #     path = ''
    #     if hasattr(connection, 'schema_name'):
    #         path = connection.schema_name
    #     return path

    # @location.setter
    # def location(self, value):
    #     pass