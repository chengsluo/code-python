# _*_ coding: utf-8 _*_

import requests

url = "http://202.120.121.204:8888/WebService/shulibLogin.asmx?WSDL"
#headers = {'content-type': 'application/soap+xml'}

body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetStudentInfo xmlns="www.lib.shu.edu.cn">
      <UserID>14121257</UserID>
    </GetStudentInfo>
  </soap:Body>
</soap:Envelope>"""

headers = {'POST': '/WebService/shulibLogin.asmx HTTP/1.1',
           'Host': '202.120.121.204',
           'Content-Type': 'text/xml; charset=utf-8',
           'Content-Length': len(body),
           'SOAPAction': 'www.lib.shu.edu.cn/GetStudentInfo'}

response=requests.post(url, data=body, headers=headers)
print (response.content.decode())
