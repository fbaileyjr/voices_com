import requests
import json
import math


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

    def get_all_organizations(self):
        # perform calculations
        pagevalue = self.page_number_calc(self.get_count_of_all_organizations())

        print("pagevalue is {pagevalue}".format(pagevalue=pagevalue))

        list_of_all_orgs = []

        organization_gen = self.get_organization_next_page(pagevalue)

        all_org_gen = self.yield_from_all_organization_pages(organization_gen)

        for x in all_org_gen:
            list_of_all_orgs.append(x)

        return list_of_all_orgs

    def get_count_of_all_organizations(self):
        counturl = "https://axonius.zendesk.com/api/v2/organizations/count"

        # get the count first
        try:
            self.countresponse = self.call_and_unpack_responses(counturl)
        except Exception:
            print("Failed to get a response for organization count...")

        if self.check_dict(self.countresponse):
            return self.countresponse["count"]["value"]
        else:
            print("Returned value for count is not a dictionary. ")
            raise Exception

    def get_organization_next_page(self, number_of_pages):
        organization_url = "https://axonius.zendesk.com/api/v2/organizations?page[size]=100&page="
        for number in range(1, (number_of_pages + 1)):
            yield self.call_and_unpack_responses(
                "{organization_url}{number}".format(
                    organization_url=organization_url, number=number
                )
            )

    def get_se_and_tam(sfid):
        pass

    def get_users_by_organization(self, organization_id):
        api_url = f"https://axonius.zendesk.com/api/v2/organizations/{organization_id}/users"
        try:
            self.user_list_response = self.call_and_unpack_responses(api_url)
        except Exception:
            print("Failed to get a response for organization count...")

        if self.check_dict(self.countresponse):
            return self.user_list_response
        else:
            print("Returned value for count is not a dictionary. ")
            raise Exception

    def jdump(obj):
        print(json.dumps(obj, indent=2))

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

print(response.text)

"""
