# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2019 The Mokee Open Source Project
# Copyright (C) 2019 The LineageOS Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info, False)
  Firmware_Images(info, False)

def IncrementalOTA_InstallEnd(info):
  OTA_InstallEnd(info, True)
  Firmware_Images(info, True)

def AddImage(info, basename, dest, incremental):
  name = basename
  if incremental:
    input_zip = info.source_zip
  else:
    input_zip = info.input_zip
  data = input_zip.read("IMAGES/" + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def OTA_InstallEnd(info, incremental):
  info.script.Print("Patching vbmeta and dtbo images...")
  AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta", incremental)
  AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo", incremental)

def Firmware_Images(info, incremental):
    partition_list = ["lk", "lk2", "audio_dsp", "cam_vpu1", "cam_vpu2", "cam_vpu3", "gz1", "gz2", "md1img", "oem_misc1", "scp1", "scp2", "spmfw", "sspm_1", "sspm_2", "tee1", "tee2"]
    block_list = ["sda", "sdb"]
    info.script.AppendExtra('ifelse(getprop("ro.boot.hwc") == "India"),'
                               'package_extract_file("logo_in.bin", "/dev/block/platform/bootdevice/by-name/logo"),'
                               'package_extract_file("logo.bin", "/dev/block/platform/bootdevice/by-name/logo");')
    for partition in partition_list:
        info.script.AppendExtra('ifelse(getprop("ro.boot.hwc") == "India"),'
                               'package_extract_file("{}_in.img", "/dev/block/platform/bootdevice/by-name/{}");'.format(partition, partition),
                               'package_extract_file("{}.img", "/dev/block/platform/bootdevice/by-name/{}");'.format(partition, partition))
    for partition in block_list:
        info.script.AppendExtra('ifelse(getprop("ro.boot.hwc") == "India"),'
                               'package_extract_file("{}_in.img", "/dev/block/{}");'.format(partition, partition),
                               'package_extract_file("{}.img", "/dev/block/{}");'.format(partition, partition))
