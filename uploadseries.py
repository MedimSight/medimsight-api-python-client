#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Medimsight SL. All Rights Reserved.
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

"""Simple intro to using the Medimsight API v1.
Before you begin, you must sigup for a new account in Medimsight:
https://www.medimsight.com/login
Then register and download your private key from your personal profile page.

Sample Usage:
  $ python uploadseries.py
Also you can also get help on all the command-line flags the program
understands by running:
  $ python uploadseries.py --help
"""
__author__ = 'contact@medimsight.com (Medimsight Team)'

import argparse
import sys

from medimsightapiclient import medimsight, subject, study

def main(argv):
    mds = medimsight.medimsight()
    mds.config(key='pathToYourMedimsightKey.xml', ClientID='clientEmail@')
    mds.getSubjects()
    mds.uploadZipDicom('demodata/4842440351547392.zip')
    sbj = subject.subject(mds, sorted(mds.getSubjects(), key=lambda x:x['fields']['date'], reverse=True)[0]['pk'])
    
    
    return mds.listGroups()