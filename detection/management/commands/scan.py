# coding: utf-8
__author__ = 'ciciya'

import os
import zipfile
import datetime
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
        self.extract(self.NORMAL_PATH, 0)
        self.extract(self.MALWARE_PATH, 1)

    def extract(self, path, isMalware):
        num = 0
        files = self.readDir(path)
        files = files[0:50]
        args = {'isMalware': isMalware}
        begin = datetime.datetime.now()
        print(begin)
        for f in files:
            if f[0] != '.':
                file_path = os.path.join(path, f)
                if zipfile.is_zipfile(file_path):
                    try:
                        apk = APK(file_path)
                        if apk.is_valid_APK():
                            num += 1
                            print ('num = ' + str(num))
                            package = f
                            # package = apk.get_package()
                            args['package'] = package
                            print ('package:' + package)
                            permissions = apk.get_permissions()
                            print ('extract permissions...')

                            for p in permissions:
                                p = p.split('.')[-1]
                                if self.PERMISSIONS.has_key(p):
                                    args[p] = 1

                            apkObjs = ApkPermission.objects.filter(package__exact=package)
                            if not apkObjs:
                                print ('saving:' + package)
                                apkObj = ApkPermission(**args)
                                apkObj.save()
                            else:
                                print ('exist:' + package)
                                continue
                    except:
                        continue
                else:
                    continue
        end = datetime.datetime.now()
        period = end - begin
        print (period)

    def readDir(self, path):
        return os.listdir(path)

    def get_permissions(self):
        permissions = Permission.objects.all()
        for p in permissions:
            self.PERMISSIONS[p.name] = {'protectionLevel': p.protectionLevel, 'permissionGroup': p.permissionGroup}