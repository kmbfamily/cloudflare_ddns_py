import requests,json
"""
클라우드플레어 DDNS 파이썬 스크립트 사용법

1. 제발 'update_dns_record' 함수만 사용해주세요, 'get_dns_record'는 사용하지 않아요.
2. 'update_dns_record' 함수 매개변수(입력값)은 다음과 같습니다.
    - zone_id : 클라우드 플레어 데시보드➝Domain Overview➝Zone ID
    - api_token : https://dash.cloudflare.com/profile/api-tokens 옆 링크로 들어가서, API Tokens을 발급받으면 됩니다.
    - domain : String(예시. ddns1.example.com, ddns2.example.com , fun.examples.com)
    - ip : String
    - ttl : Integer(분 단위)
    - proxied : Bool
3. 반환값은 Bool값입니다, DDNS 업데이트를 성공했다면 True 반환, 오류 또는 어떤 사유로 실패하면 False
"""
"""
cloudflare DDNS python script menual

1. Please use the 'update_dns_record' def(function) only,'get_dns_record' def is not use
2. The parameters of the 'update_dns_record' function are as follows
    - zone_id : cloudflare dashboard➝Domain Overview➝Zone ID
    - api_token : https://dash.cloudflare.com/profile/api-tokens , API Tokens is yes But API Keys is not
    - domain : String(ex. ddns1.example.com, ddns2.example.com , fun.examples.com)
    - ip : String
    - ttl : Integer(Minute)
    - proxied : Bool
3. Return value is Bool, If the DDNS update is successful, it returns True, otherwise, it returns False
"""

def get_my_ip():
    try:
        result = requests.get("http://kmbddns.dothome.co.kr/").json()["ip"]
    except:
        return False
    return result

def get_dns_record(zone_id, api_token, domain):         #서브 도메인별 ID 구하기
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records?type=A&name="+domain
        headers = {
            "Authorization": "Bearer "+api_token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        dns_record_info = response.json()
        if dns_record_info["success"] and dns_record_info["result_info"]["total_count"] == 1:
            return dns_record_info["result"][0]["id"]
        else:
            return False
    except:
        return False
    return

def update_dns_record(zone_id, api_token, domain, ip, ttl, proxied):
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records/"+get_dns_record(zone_id, api_token, domain)
        headers = {
            "Authorization": "Bearer "+api_token,
            "Content-Type": "application/json"
        }
        data = {
            "type": "A",
            "name": domain,
            "content": ip,
            "ttl": ttl,
            "proxied": proxied
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        update_dns_record = response.json()
    except:
        return False
    return update_dns_record["success"]

update_dns_record("","","ddns1.kmbfamily.com",get_my_ip(),60,False)
