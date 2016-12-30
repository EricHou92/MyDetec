# coding: utf-8
__author__ = 'ciciya'

import os
from django.core.management.base import BaseCommand
from detection.models import *
from django.conf import settings
from androguard.core.bytecodes.apk import *


class Command(BaseCommand):
    MALWARE_PATH = os.path.join(settings.MEDIA_ROOT, 'malware')
    NORMAL_PATH = os.path.join(settings.MEDIA_ROOT, 'normal')
    PERMISSIONS = {}

    def handle(self, *arg, **options):
        self.get_permissions()
        if arg:
            if arg[0] == 'replace':
                ApkPermission.objects.all().delete()
                self.scan()
            elif arg[0] == 'update':
                self.scan()
            else:
                print('args:\n  --  replace\n  --  update')
        else:
            print('args:\n  --  replace\n  --  update')

    def scan(self):
        self.extract(self.MALWARE_PATH, 1)
        self.extract(self.NORMAL_PATH, 0)

    def extract(self, path, isMalware):
        files = self.readDir(path)
        # files = files[0:3]
        args = {'isMalware': isMalware}
        for f in files:
            if f[0] != '.':
                print('file:' + f)
                file_path = os.path.join(path, f)
                apk = APK(file_path)
                if apk.is_valid_APK():
                    package = apk.get_package()
                    args['package'] = package
                    print('package:' + package)
                    permissions = apk.get_permissions()
                    print('extract permissions...')

                    for p in permissions:
                        p = p.split('.')[-1]
                        if self.PERMISSIONS.has_key(p):
                            args[p] = 1

                    apkObjs = ApkPermission.objects.filter(package__exact=package)
                    if not apkObjs:
                        print('saving:' + package)
                        apkObj = ApkPermission(**args)
                        apkObj.save()
                    else:
                        print('exist:' + package)

    def readDir(self, path):
        return os.listdir(path)

    def get_permissions(self):
        permissions = Permission.objects.all()
        for p in permissions:
            self.PERMISSIONS[p.name] = {'protectionLevel': p.protectionLevel, 'permissionGroup': p.permissionGroup}
