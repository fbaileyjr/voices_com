import requests
import bs4 as BeautifulSoup
import re
import json
class VoicesConnector:
    def __init__(self, headers, payload):
        self.headers = headers
        self.payload = payload

    def call_and_unpack_responses(self, url):
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        if response.status_code == 200:
            jsonresponse = json.loads(response.text)
            return jsonresponse
        raise Exception(f"Probelm fetching groups. Got: {response.content}")

    @staticmethod
    def check_dict(obj):
        if isinstance(obj, dict):
            print("Returned a dictionary")
            return True
        else:
            print("Returned value is not a dictionary")
            raise Exception
            return False

    def jdump(obj):
        print(json.dumps(obj, indent=2))

    def match_security_cookie(self, response_string):
        # regex pattern for customer groups
        self.matched_string = re.search(r"(security_cookie=\w+);", response_string, re.I)
        if self.matched_string.group(1):
            return self.matched_string.group(1)
        else:
            print("No match")

    def match_metrics(self, response_string):
        # regex pattern for customer groups
        self.matched_string = re.search(r"(metrics=\w+);", response_string, re.I)
        if self.matched_string.group(1):
            return self.matched_string.group(1)
        else:
            print("No match")

    def match_security_cookie(self, response_string):
        # regex pattern for security cookie
        self.matched_string = re.search(r"(security_cookie=\w+);", response_string, re.I)
        if self.matched_string.group(1):
            return self.matched_string.group(1)
        else:
            print("No match")

    def match_vdc_session(self, response_string):
        # regex pattern for customer groups
        self.matched_string = re.search(r"(vdc_sess=\w+);", response_string, re.I)
        if self.matched_string.group(1):
            return self.matched_string.group(1)
        else:
            print("No match")


    def page_number_calc(self, count):
        # rounds down to the nearest integer
        return math.floor(count / 100) + 1

    def sfdc_iteration_and_match(self, sfdc, org_list):
        # this will take the list that contains a dictionary, then iterate to match the sfdc
        for org in range(len(org_list)):
            if org_list[org].get("organization_fields").get("sfdc_account_id") == sfdc:
                account_owner = org_list[org].get("organization_fields").get("account_owner")
                assigned_csm = org_list[org].get("organization_fields").get("assigned_csm")
                print("Account owner is {account_owner}".format(account_owner=account_owner))
                print("Account owner is {assigned_csm}".format(assigned_csm=assigned_csm))
                return {"Sales Rep": account_owner, "TAM": assigned_csm}
                break
            else:
                pass

    def yield_from_all_organization_pages(self, org_dict):
        for page in org_dict:
            if page.get("organizations"):
                yield from page["organizations"]


def connect_and_get_response(url):
    response = response = requests.request("GET", url)
    response_string = response.headers['Set-Cookie']
    return response_string

def match_metrics(response_string):
    # regex pattern for customer groups
    matched_string = re.search(r"(metrics=\w+);", response_string, re.I)
    if matched_string.group(1):
        return matched_string.group(1)
    else:
        print("No match")


def match_security_cookie(response_string):
    # regex pattern for customer groups
    matched_string = re.search(r"security_cookie=(\w+)", response_string, re.I)
    if matched_string.group(1):
        return matched_string.group(1)
    else:
        print("No match")

def match_vdc_session(response_string):
    # regex pattern for customer groups
    matched_string = re.search(r"(vdc_sess=\w+);", response_string, re.I)
    if matched_string.group(1):
        return matched_string.group(1)
    else:
        print("No match")

# return headers
def return_headers(security_cookie, vdc_sess, metrics):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': f'security_cookie={security_cookie}; {vdc_sess}; {metrics}; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks'
    }
    return headers

# need to update to pass and encode the url string
def return_payload(security_cookie):
    payload=f'security_token={security_cookie}&login=frankbaileyjr%40gmail.com&password=Kaley2Moira'
    return payload

"""
response.headers['Set-Cookie']
This is a string
need to parse out the security_cookie and vdc_session



security_token: 1c232cca39f843184787029836aba899
timezone_id: 8
vanilla_forums_jwt: 
login: frankbaileyjr@gmail.com
password: Kaley2Moira
sign_in: Log In


import requests

url = "https://www.voices.com/login"

payload={}
headers = {
  'Cookie': 'security_cookie=f04b90d3d373c66758d1ae46954f171a; vdc_sess=l196kipmta8ph52igjtbc9033q8gllpj; metrics=5ab4dee0027f8959471c5dec88b828436d7cd926'
}

response = requests.request("GET", url, headers=headers, data=payload)
response = requests.request("POST", url, headers=headers, data=payload)


---
match sequence

payload={}
headers={}

response = requests.request("GET", url, headers=headers, data=payload)

security_cookie=match_security_cookie(response.headers['Set-Cookie'])
vdc_sess=match_vdc_session(response.headers['Set-Cookie'])
metrics=match_metrics(response.headers['Set-Cookie'])
payload=return_payload(security_cookie)

post_response = requests.request("POST", url, headers=headers, data=payload)




res = requests.post('https://api.github.com/user', verify=False, auth=HTTPBasicAuth('user', 'password'))
-----

with requests.Session() as s:
    first_response = s.get(url + '/login')
    matched_string = re.search(r"security_cookie=(\w+)", test_string, re.I)
    security_cookie = matched_string.group(1)
    s.headers.update({'content-type':'application/x-www-form-urlencoded'})
    data = {
       'security_token' : security_cookie,
       'login' : 'frankbaileyjr@gmail.com',
       'password' : 'Kaley2Moira',
       'sign_in' : 'Log In',
    }
    response = requests.post(url + '/login', data=data)
    pprint(response.text)


s = requests.Session()
first_response = s.get(url + '/login')
matched_string = re.search(r"security_cookie=(\w+)", test_string, re.I)
security_cookie = irst_response.cookies['security_cookie']
s.headers.update({'content-type':'application/x-www-form-urlencoded'})

data = {
   'security_token' : security_cookie,
   'login' : 'frankbaileyjr@gmail.com',
   'password' : 'Kaley2Moira',
   'sign_in' : 'Log In',
}
response = requests.post(url + '/login', data=data)
pprint(response.text)
    
data = 








print(response.text)

test_string = response.headers['Set-Cookie']

split_stringe = test_string.split("; ")

>>> for x in first_split:
...     test_list.append(x.split(","))

for pair in split_string:
    try:
        temp_dict = dict(s.split('=', 1) for s in pair.split())
    except Exception:
        pass
    test_dict.update(temp_dict)

security_token: 1c232cca39f843184787029836aba899
timezone_id: 8
vanilla_forums_jwt: 
login: frankbaileyjr@gmail.com
password: Kaley2Moira
sign_in: Log In


url = "https://www.voices.com/login"

I can automate the whole entire process, I'll do that tomorrow


import requests

import requests

url = "https://www.voices.com/login"

payload='security_token=e4ad561c21289139729098ae7f29d007&login=frankbaileyjr%40gmail.com&password=Kaley2Moira'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'security_cookie=dd1c92411dcdacf11dfad966e2ed1471; vdc_sess=l196kipmta8ph52igjtbc9033q8gllpj; metrics=5ab4dee0027f8959471c5dec88b828436d7cd926; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks'
}

 s.headers.update({'Cookie' : f'security_cookie={security_cookie}; vdc_sess={s.cookies['vdc_sess']}; metrics={s.cookies['metrics']}; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks'})

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


dammit

you have to update s.headers
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'security_cookie=dd1c92411dcdacf11dfad966e2ed1471; vdc_sess=l196kipmta8ph52igjtbc9033q8gllpj; metrics=5ab4dee0027f8959471c5dec88b828436d7cd926; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks'
}



data = {
   'security_token' : security_cookie,
   'login' : 'frankbaileyjr@gmail.com',
   'password' : 'Kaley2Moira',
   'sign_in' : 'Log In',
}

# for current
url for current = https://www.voices.com/talent/jobs_pagination?offset=0&limit=100

request payload is the query to specify answered, archived, etc

# for answered
answered_payload = {"sort":{"order":"desc","by":"posted_date"},"search":{"query":null},"filter":{"by":["status:answered","show:all"]},"custom":{}}



# for archived?
archived_payload = {"sort":{"order":"desc","by":"posted_date"},"search":{"query":null},"filter":{"by":["status:deleted","show:all"]},"custom":{}}

url for archived = https://www.voices.com/talent/jobs_pagination/?offset=0&limit=100
url for secon page = https://www.voices.com/talent/jobs_pagination?offset=200&limit=100
retunrs a json object

# make a dict from returned json response
# dict keys are status, data
json_result = jobs.json()
totals = json_result['data']['total']

# dict keys for json_results['data'] are ['total', 'entities', 'member']
# json_results['data']['entities'] is a list, this is what we will need to iterate through in the end to convert into a csv. Probably csv export using dict keys


# update existing results dict