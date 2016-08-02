from httpsigned import *

class subject:
        def __init__(self, mdsinst, sid):
            self.sid  = sid
            self.mdsinst = mdsinst
     
        def getData(self):
            return self.mdsinst.getCall('subject', {'wun':'data', 'sbjID' : str(self.sid)})
        
        def getImages(self):
            return self.mdsinst.getCall('subject', {'wun':'image', 'sbjID' : str(self.sid)})
            
        def downloadImage(self, vID, vformat = 'dicom', path = './'):
            filestring = 'file_' + vformat + '_' + str(vID)
            volurl = self.mdsinst.getCall(filestring, {'wun':'image', 'sbjID' : str(self.sid)})
            filename = path + str(vID) + ('.zip' if vformat == 'dicom' else '.nii.gz' if vformat == 'nii' else '.png' if vformat == 'png' else '')
            
            import urllib2, urllib
            
            file_name = filename
            u = urllib2.urlopen(volurl)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
            
                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

            f.close()
            
            #urllib.urlretrieve(volurl, path + str(vID) + ('.zip' if vformat == 'dicom' else '.nii.gz' if vformat == 'nii' else '.png' if vformat == 'png' else ''))
            
            return path + str(vID) + ('.zip' if vformat == 'dicom' else '.nii.gz' if vformat == 'nii' else '.png' if vformat == 'png' else '')
            
        def getFiles(self):
            return self.mdsinst.getCall('subject', {'wun':'files', 'sbjID' : str(self.sid)})
            
        def getStudies(self, iindex = 0, findex = 20):
            return json.loads(self.mdsinst.getCall('oldstudies', {'wun':'all', 'iindex':iindex, 'findex':findex, 'subject' : str(self.sid)}))
            
        def getStudiesData(self, sID):
            return json.loads(self.mdsinst.getCall('oldstudies', {'wun':'io', 'study' : str(sID)}))
            
        def getBiomarkers(self):
            return self.mdsinst.getCall('metatags', {'sbjID' : str(self.sid)})