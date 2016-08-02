class study:
        def __init__(self, sid, mdsinst):
            self.sid  = sid
            self.mdsinst = mdsinst
            import json
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
            
        def launch(self, inouts):
            
            #sub_grp_multivol_grp_t1:5679196776955904
            #vol_grp_t1:5664676029399040
            #aseg:'subcorticalsegmentation'
            #reportname:'report.hippocampi'
            #csvdata:'report.hippocampi'

            #return self.postCall('studies', {'name':'', 'notifyatend':'', 'notifyto':'', 'studyname':'' })
            return -1