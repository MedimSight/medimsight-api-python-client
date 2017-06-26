import json

class analysisapp:
        def __init__(self, sid, mdsinst):
            self.sid  = sid
            self.mdsinst = mdsinst
            self.studydata = json.loads(self.mdsinst.getCall('studies', {'wun':'study', 'ttypeid' : str(self.sid)}))[0]['fields']
     
        def getDesc(self):
            return self.studydata['desc']
        
        def getInOut(self):
            from xml.etree.ElementTree import XML, fromstring, tostring
            
            myxml = fromstring(self.studydata['xml'].encode('ascii', 'xmlcharrefreplace'))
            inout = myxml.find('inout')
            
            multiin = []
            
            for elem in list(inout):
                if elem.find('multiin'):
                    multiin = multiin + list(elem.find('multiin'))
                else:
                    multiin.append(elem)
                    
            return multiin
            
        def launch(self, inouts, analysisname = 'none', notifyto = '', notifyatend = False):
            # Whole brain seg
            #vol_grp_t1:5664676029399040
            #aseg:'subcorticalsegmentation'
            #reportname:'report.hippocampi'
            #csvdata:'report.hippocampi'
            
            # LST 
            #vol_grp_flair: 5070410546675712
            #vol_grp_t1: none
            #lst_lpa_report: LST Lesion prediction algorithm report
            #lst_map: ME Lesion map
            #3d_brain_lesions: 3D Brain Lesions
            #vol_t1_wl: None
            
            analysisparams = {'name': self.studydata['ttype'], 'notifyatend': notifyatend, 'notifyto': notifyto, 'studyname': analysisname if analysisname == 'none' else self.studydata['ttype'].replace(' ','')}
            
            for elem in inouts.items():
                analysisparams[elem[0]] = elem[1]

            return self.mdsinst.postCall('studies', analysisparams)