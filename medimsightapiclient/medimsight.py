import httplib, urllib, urllib2, httplib2
import time
import subprocess
import random
import json
import subject
import analysisapp

class medimsight:

    def __init__(self):
        self.privateKey  = ""
        self.ClientID = ""
        self.host = "https://prdmedimsight.appspot.com"
        self.userID = ''
        
    def config (self, key = "", ClientID = ""):
        self.privateKey  = key
        self.ClientID = ClientID
        self.userID = ''
        
    def SignString(self, XMLPrivkey, string):
        from gdata.tlslite.utils import keyfactory, compat
        from gdata.tlslite.utils.jython_compat import createByteArraySequence
        from gdata.tlslite.utils.jython_compat import stringToBytes
        from hashlib import sha256
        import base64
        import urllib
        Key = keyfactory.parseXMLKey(XMLPrivkey)
        prefixBytes = createByteArraySequence([48, 49, 48, 13, 6, 9, 96, 134, 72, 1, 101, 3, 4, 2, 1, 5, 0, 4, 32])
        code = Key.sign(prefixBytes + stringToBytes(sha256(string).digest()))
        codetourl = urllib.quote(base64.b64encode(code)).replace('+','%2B').replace('/','%2F')
        
        return codetourl
    
    def getCall(self, resource, attributes = {}):
        # resource is the last part of the url
        # attributes should be like -> {'zipfilecode': inputFile, 'AccessId': ClientID, 'Expires': str(Expiration), 'Signature': signature}
        
        import os
        import subprocess
        import time
    
        Expiration = int(time.time()+300)
        CanonicalizedResource = '/' + resource
        StringToSign = "GET" + "\n\n\n" + str(Expiration) + "\n" + CanonicalizedResource
        signature = self.SignString(open(self.privateKey,'r').read(), StringToSign)
    
        attributes.update({'AccessId': self.ClientID, 'Expires': str(Expiration), 'Signature': signature})
        signedUrl = self.host + CanonicalizedResource + '?' + urllib.urlencode(attributes)
        
        req = urllib2.Request(signedUrl)
    
        cont = 0
        while True:
            try:
                response = urllib2.urlopen(req)
                responsedata = response.read()
                break
            except (urllib2.HTTPError, urllib2.URLError) as e:
                cont += 1
                print "Retry getCall: %s" % (str(cont))
            
                if cont > 5:
                    raise Exception ("getCall Error: %s" % (str(e)))
                
                time.sleep(5)
    
        return responsedata
        
    def postCall(self, resource, attributes = {}):
        # resource is the last part of the url
        # attributes should be like -> {'zipfilecode': inputFile, 'AccessId': ClientID, 'Expires': str(Expiration), 'Signature': signature}
        
        import time
        import os.path
    
        Expiration = int(time.time()+300)
        CanonicalizedResource = '/' + resource
        StringToSign = "POST" + "\n\n\n" + str(Expiration) + "\n" + CanonicalizedResource
        signature = self.SignString(open(self.privateKey,'r').read(), StringToSign)
        attributes.update({'_method': 'post', 'AccessId': self.ClientID, 'Expires': str(Expiration), 'Signature': signature})
        signedUrl = self.host + CanonicalizedResource
    
        req = urllib2.Request(signedUrl)
    
        req.add_data(urllib.urlencode(attributes))
    
        cont = 0
        while True:
            try:
                response = urllib2.urlopen(req)
                responsedata = response.read()
                break			
            except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
                cont += 1
            
                if cont > 5:
                    raise Exception ("setFile Error: %s" % (str(e)))
                
                time.sleep(5)
    
        return responsedata
        
    def putCall(self, resource, attributes = {}):
        # resource is the last part of the url
        # attributes should be like -> {'zipfilecode': inputFile, 'AccessId': ClientID, 'Expires': str(Expiration), 'Signature': signature}
        
        import time
        import os.path
    
        Expiration = int(time.time()+300)
        CanonicalizedResource = '/' + resource
        StringToSign = "POST" + "\n\n\n" + str(Expiration) + "\n" + CanonicalizedResource
        signature = self.SignString(open(self.privateKey,'r').read(), StringToSign)
        attributes.update({'_method': 'put', 'AccessId': self.ClientID, 'Expires': str(Expiration), 'Signature': signature})
        signedUrl = self.host + CanonicalizedResource
    
        req = urllib2.Request(signedUrl)
    
        req.add_data(urllib.urlencode(attributes))
    
        cont = 0
        while True:
            try:
                response = urllib2.urlopen(req)
                responsedata = response.read()
                break			
            except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
                cont += 1
            
                if cont > 5:
                    raise Exception ("setFile Error: %s" % (str(e)))
                
                time.sleep(5)
    
        return responsedata
        
    def deleteCall(self, resource, attributes = {}):
        # resource is the last part of the url
        # attributes should be like -> {'zipfilecode': inputFile, 'AccessId': ClientID, 'Expires': str(Expiration), 'Signature': signature}
        
        import time
        import os.path
    
        Expiration = int(time.time()+300)
        CanonicalizedResource = '/' + resource
        StringToSign = "POST" + "\n\n\n" + str(Expiration) + "\n" + CanonicalizedResource
        signature = self.SignString(open(self.privateKey,'r').read(), StringToSign)
        attributes.update({'_method': 'delete', 'AccessId': self.ClientID, 'Expires': str(Expiration), 'Signature': signature})
        signedUrl = self.host + CanonicalizedResource
    
        req = urllib2.Request(signedUrl)
    
        req.add_data(urllib.urlencode(attributes))
    
        cont = 0
        while True:
            try:
                response = urllib2.urlopen(req)
                responsedata = response.read()
                break			
            except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
                cont += 1
            
                if cont > 5:
                    raise Exception ("setFile Error: %s" % (str(e)))
                
                time.sleep(5)
    
        return responsedata        
        
    def createSubject(self, sname, suid = '', sage = '', sphone = '', saddress = ''):
        return json.loads(self.postCall('subject', {'name' : sname, 'uid' : suid, 'age':sage, 'phone':sphone, 'address':saddress}))
    
    def getSubjectbyID(self, sid):
        return subject.subject(sid, self)
    
    def getSubjects(self, grpID = 0):
        return json.loads(self.getCall('group', {'grpID' : str(grpID)}))
    
    def removeSubject(self, sid):
        return json.loads(self.deleteCall('subject', {'id' : sid}))
    
    def createGroup(self, gname):
        return json.loads(self.postCall('group', {'name' : gname}))
        
    def removeGroup(self, gid):
        return json.loads(self.deleteCall('group', {'id' : gid}))
            
    def listGroups(self):
        return json.loads(self.getCall('group', {'wun' : 'all'}))
    
    def addSubjectToGroup(self, sbjID, grpID):
        return json.loads(self.postCall('agroup', {'sbjID':sbjID, 'grpID':grpID}))

    def uploadZipDicom(self, filename):
        import os
        
        signedUrl = self.postCall('file_0', {'namefile':os.path.basename(filename), 'subject':'', 'class':'ZipFile', 'size':'159951', 'ftype':'.zip'})
    
        if (signedUrl == "request_signature_not_match") or (signedUrl == "request_access_forbidden"):
            #createPrivateKeyFromMAC()#de momento no se hace
            #return setZipFile(filename)
            
            return signedUrl #False
        args = signedUrl.split('+*+')
    
        url4 = args[6]
        print "Sending ..."#
        import MultipartPostHandler
        from poster.encode import multipart_encode, MultipartParam
        from poster.streaminghttp import register_openers
        register_openers()
        
        items = []
        
        for name, value in {'key': args[1], 'bucket': args[7], 'GoogleAccessId': args[2], 'Expires': args[3], 'Policy': args[4], 'signature': args[5]}.items():
            items.append(MultipartParam(name, value))
            
        items.append(('file', open(filename)))
            
        datagen4, headers4 = multipart_encode(items)
        
        req4 = urllib2.Request(url4, datagen4, headers4)
        
        try: 
            response4 = urllib2.urlopen(req4)
        except urllib2.URLError, e:
            print "URL Error: %s" % (e)
            return "URL Error: %s" % (e)
            #return e
            
        ackCheck = self.postCall('file_' + args[0], {'ack':'zip', 'id':args[0]})
        
        return True
        
    def getAnalysis(self, modality = 'allstudies'):
        return json.loads(self.getCall('studies', {'wun' : str(modality)}))
        
    def getAnalysisbyID(self, sid):
        return analysisapp.analysisapp(sid, self)