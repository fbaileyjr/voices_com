import csv
import json
import requests
import re
import sys
from bs4 import BeautifulSoup
from config import username, password


def connect_and_get_response(url):
    response = response = requests.request("GET", url)
    response_string = response.headers["Set-Cookie"]
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
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"security_cookie={security_cookie}; {vdc_sess}; {metrics}; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks",
    }
    return headers


# need to update to pass and encode the url string
def return_payload(security_cookie):
    payload = (
        f"security_token={security_cookie}&login=frankbaileyjr%40gmail.com&password=Kaley2Moira"
    )
    return payload


def return_shortlist(entity_list):
    pruned_list = list()
    for entity in entity_list:
        if entity["is_shortlisted"] == 1:
            pruned_list.append(entity)
        else:
            pass
    return pruned_list


def iterate_and_return_all_entities():
    count = 100
    first_response = s.post("https://www.voices.com/talent/jobs_pagination/?offset=0&limit=100")
    record_count = first_response.json()["data"]["total"]
    results_list = first_response.json()["data"]["entities"]

    while count < int(record_count):
        jobs = s.post(f"https://www.voices.com/talent/jobs_pagination/?offset={count}&limit=100")
        if jobs.json():
            results_list = results_list + jobs.json()["data"]["entities"]
            count += 100
        else:
            pass
    return results_list


def write_entities_to_csv(entity_list):
    with open("voices_com_job_list.csv", mode="w") as csv_file:
        fieldnames = [
            "id",
            "member_id",
            "organization_id",
            "session_id",
            "member_type",
            "title",
            "posted_at",
            "deadline_at",
            "status_button",
            "is_featured",
            "is_shortlisted",
            "is_reviewed",
            "is_sent",
            "is_invited",
            "price",
            "language",
            "accent",
            "role",
            "style_one",
            "style_two",
            "gender",
            "voice_age",
            "word_count",
            "finished_minutes",
            "organization_name",
            "organization_avatar_url",
            "organization_rating",
            "total_review_count",
            "worked_together",
            "type",
            "is_full_service",
            "is_self_service",
            "responses_count",
            "voicematch_score",
            "is_denied",
            "is_closed",
            "is_saved",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for record in entity_list:
            writer.writerow(record)


def write_shortlist_entities_to_csv(entity_list):
    with open("voices_com_shortlisted.csv", mode="w") as csv_file:
        fieldnames = [
            "id",
            "member_id",
            "organization_id",
            "session_id",
            "member_type",
            "title",
            "posted_at",
            "deadline_at",
            "status_button",
            "is_featured",
            "is_shortlisted",
            "is_reviewed",
            "is_sent",
            "is_invited",
            "price",
            "language",
            "accent",
            "role",
            "style_one",
            "style_two",
            "gender",
            "voice_age",
            "word_count",
            "finished_minutes",
            "organization_name",
            "organization_avatar_url",
            "organization_rating",
            "total_review_count",
            "worked_together",
            "type",
            "is_full_service",
            "is_self_service",
            "responses_count",
            "voicematch_score",
            "is_denied",
            "is_closed",
            "is_saved",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for record in entity_list:
            writer.writerow(record)


if __name__ == "__main__":
    # declaring shortlist, if exist
    try:
        shortlist = sys.argv[1]
        shortlist = shortlist.lower()
        print(f"{shortlist} was provided...")
    except Exception:
        shortlist = "None"
        print(f"{shortlist} was provided...")

    # starting a session object
    with requests.Session() as s:

        # first get the headers and cookies for current session
        s.get("https://www.voices.com/login")

        # declaring security_cookie, vdc_sess, and metrics variables for string
        security_cookie = s.cookies["security_cookie"]
        vdc_sess = s.cookies["vdc_sess"]
        metrics = s.cookies["metrics"]

        # update headers with required cookie
        cookie = f"security_cookie={security_cookie}; vdc_sess={vdc_sess}; metrics={metrics}; vo_shortlist_count_24hours213111=0; vo_shortlist_count_all_time213111=88; vo_shortlist_last_updated213111=2%20weeks"
        s.headers.update({"Cookie": cookie})

        # update headers to log in with the proper appliation type
        s.headers.update({"Content-Type": "application/x-www-form-urlencoded"})

        # create the data payload
        data = {
            "security_token": s.cookies["security_cookie"],
            "login": username,
            "password": password,
            "sign_in": "Log In",
        }

        # send credentials and get response
        response = s.post("https://www.voices.com/login", data=data)

        # creating soup object and matching the margBot-sm-3 class
        soup = BeautifulSoup(response.text, "html.parser")

        match = soup.find("h1", class_="margBot-sm-3")

        # if successful, then pull records back and export
        if "Welcome back," in match.text:
            entity_list = iterate_and_return_all_entities()
        else:
            print("Login was unsuccessful... Try again")
            # need to add a system break

        if shortlist == "shortlist":
            short = return_shortlist(entity_list)
            print("Writing Shortlist CSV..")
            write_shortlist_entities_to_csv(short)
            print("Done.")
        else:
            print("Writing all records to CSV...")
            write_entities_to_csv(entity_list)
            print("Done")
"""
  {
    "id": 470800,
    "member_id": 213111,
    "organization_id": 213111,
    "session_id": "t0jh84fv24dakh08pgalbevn2fk04l3s",
    "member_type": "talent",
    "title": "Nissan Super Sale Radio",
    "posted_at": "2021-06-08T12:37:21+00:00",
    "deadline_at": "2021-06-11T04:59:00+00:00",
    "status_button": "<span class=\"status status-green\" title=\"Client is accepting auditions\" data-toggle=\"tooltip\" data-placement=\"bottom\" data-container=\"body\" >Hiring</span>",
    "is_featured": false,
    "is_shortlisted": 0,
    "is_reviewed": 1,
    "is_sent": 1,
    "is_invited": false,
    "price": "$550",
    "language": "English (North American)",
    "accent": "",
    "role": "Announcer",
    "style_one": "Charismatic",
    "style_two": "Confident",
    "gender": "Both",
    "voice_age": "Young Adult (18-35)",
    "word_count": 75,
    "finished_minutes": "0h: 0m: 30s",
    "organization_name": "Chris Francheville",
    "organization_avatar_url": "/assets/images/branding/default_profile_avatar_voicegirl.png",
    "organization_rating": null,
    "total_review_count": "0",
    "worked_together": 0,
    "type": "Self Service",
    "is_full_service": false,
    "is_self_service": true,
    "responses_count": "77",
    "voicematch_score": 70,
    "is_denied": false,
    "is_closed": false,
    "is_saved": 0
  },
  """
