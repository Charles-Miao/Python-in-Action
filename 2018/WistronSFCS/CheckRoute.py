import urllib.request

url="http://10.42.23.222/Tester.WebService/WebService.asmx"
#SOAP request and response
data='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CheckRoute xmlns="http://localhost/Tester.WebService/WebService">
      <UnitSerialNumber>NDBWKH300501B102</UnitSerialNumber>
      <StageCode>ZC</StageCode>
    </CheckRoute>
  </soap:Body>
</soap:Envelope>
'''

headers = {'Content-Type': 'text/xml'}
req = urllib.request.Request(url, data=data.encode('utf-8'), headers=headers)
res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))
