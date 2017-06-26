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

from medimsightapiclient import medimsight, subject, analysis, analysisapp

def main(argv):
    mds = medimsight.medimsight()
    mds.config(key='pathToYourMedimsightKey.xml', ClientID='clientEmail@')
    mds.getSubjects()
    mds.uploadZipDicom('demodata/4842440351547392.zip')
    sbj = subject.subject(mds, sorted(mds.getSubjects(), key=lambda x:x['fields']['date'], reverse=True)[0]['pk'])
    
    appa = analysisapp.analysisapp('5768923442053120', mds)
    
    for elem in appa.getInOut():
    	print 'Set value for ' + elem.find('id').text
    	
    appargs = {'lst_lpa_report': 'LST Lesion prediction algorithm report',
				'vol_grp_flair': 5070410546675712,
				'vol_grp_t1': 'none',
				'lst_map': 'ME Lesion map',
				'3d_brain_lesions': '3D Brain Lesions',
				'vol_t1_wl': 'None'}
				
	analysisID = appa.launch(appargs)
	
	# Check after some time
    if sorted(sbj.getStudies(), key=lambda x:x['fields']['dateStart'], reverse=True)[0]['fields']['state'] == 4:
        latestAnalysisParams = sbj.getStudiesData(sorted(sbj.getStudies(), key=lambda x:x['fields']['dateStart'], reverse=True)[0]['pk'])
		
        lesions_map = 0
		
        for elem in latestAnalysisParams:
            if elem['fields']['name'] == 'lst_map':
                lesions_map = elem['fields']['vol']
                
        if lesions_map != 0:
        	sbj.downloadImage(lesions_map, vformat = 'nii')
        
        biomarkers = sbj.getBiomarkers()
				
    return sbj.getData()
