import os
from django.utils.deconstruct import deconstructible
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage

@deconstructible
class UploadFileTo(object):
    def __init__(self, folder, sufix):
        self.folder = folder
        self.sufix = sufix

    def __call__(self, instance, filename):
        _, filename_ext = os.path.splitext(filename)
        return '{0}/{1}{2}'.format(
            self.folder,
            '{0}-{1}-{2}'.format(instance.uuid, self.sufix, timezone.now().isoformat()),
            filename_ext.lower(),
        )

@deconstructible
class UploadProfilePictureTo(object):
    def __init__(self, folder, sufix):
        self.folder = folder
        self.sufix = sufix

    def __call__(self, instance, filename):
        _, filename_ext = os.path.splitext(filename)
        name = '{0}/{1}{2}'.format(
            self.folder,
            '{0}-{1}'.format(instance.uuid, self.sufix),
            filename_ext.lower(),
        )
        print(name, filename_ext.lower())
        return name
    
class OverwriteStorage(S3Boto3Storage):
    def get_available_name(self, name, max_length = None):
        if self.exists(name):
            self.delete(name)
        return name