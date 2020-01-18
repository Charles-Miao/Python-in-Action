import urllib.request

url="http://10.42.23.222/Tester.WebService/WebService.asmx"
#SOAP request and response
data='''
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Complete xmlns="http://localhost/Tester.WebService/WebService">
      <UnitSerialNumber>NDBWKH300501B102</UnitSerialNumber>
      <Line>HA17</Line>
      <StageCode>ZC</StageCode>
      <StationName>Burn-in</StationName>
      <EmployeeID>k1203781</EmployeeID>
      <Pass>True</Pass>
      <TrnDatas>
        <TrnData>NDBWKH300501B102</TrnData>
      </TrnDatas>
    </Complete>
  </soap:Body>
</soap:Envelope>
'''

headers = {'Content-Type': 'text/xml'}
req = urllib.request.Request(url, data=data.encode('utf-8'), headers=headers)
res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))
