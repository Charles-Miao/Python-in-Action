#import urlib.request module
import urllib.request
#web service URL
url="http://172.30.26.24/tester.WebService/WebService.asmx"
#SOAP request and response
data='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CheckRoute xmlns="http://localhost/Tester.WebService/WebService">
      <UnitSerialNumber>123</UnitSerialNumber>
      <StageCode>ZA</StageCode>
    </CheckRoute>
  </soap:Body>
</soap:Envelope>
'''
#content type
headers = {'Content-Type': 'text/xml'}
#request
req = urllib.request.Request(url, data=data.encode('utf-8'), headers=headers)
#response
res = urllib.request.urlopen(req)
#print result
print(res.read().decode('utf-8'))
