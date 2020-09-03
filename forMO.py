import requests,json


url='http://192.168.8.34:8080/login'
data = {
    'username': '7711',
    'password': '7711',
    'workDate': '2020-09-03',
    'ela': '101',
    'redirect':'',
}
s=requests.Session()
rep=s.post(url,data=data)
url='http://192.168.8.34:8080/api/datalist/data/1030352134818820096?precept=&filter='
headers={
    'Host': '192.168.8.34:8080',
    'Connection': 'keep-alive',
    'Content-Length': '231',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'x-feign-module': 'mwork',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'http://192.168.8.34:8080',
    'Referer': 'http://192.168.8.34:8080/mwork/datalist/1030352134818820096---list',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    }
sn="DTPR2285S20072000900"
json=json.dumps({"placeholder":None,"query":[{"clazz":"String","name":"t3Sn","condition":"=","values":[sn]}],"order":[{"id":"docNo","sorting":"desc","sequence":1}],"summary":[],"page":{"size":20,"page":1,"total":0},"args":None})
response=s.post(url,headers=headers,data=json)
r=response.json()['origin'][0]
print(r['cusName'],r['momOrderDocNo'],r['invSpec'],r['snBegin'])