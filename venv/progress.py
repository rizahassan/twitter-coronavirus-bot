import tweepy
import logging
import time
from datetime import datetime
# For coronavirus monitor
import json
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Twitter Bot Account
CONSUMER_KEY = ''  # TO CHANGE: CONSUMER KEY FROM TWITTER APP
CONSUMER_SECRET = ''  # TO CHANGE: CONSUMER SECRET FROM TWITTER APP
ACCESS_KEY = ''  # TO CHANGE: ACCESS KEY FROM TWITTER APP
ACCESS_SECRET = ''  # TO CHANGE: ACCESS SECRET TOKEN FROM TWITTER APP
CALLBACK_URL = ''  # TO CHANGE: CALLBACK URL FROM TWITTER DEV


# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


active_cases = ""  # current active cases
active_cases_yesterday = ""  # active cases yesterday
date = ""

# Function that takes current active cases of a country
# Saves statistics into stats_by_country.json
# Return -1 if country does not exist. Return 1 if country exists.


def monitor_current(country):

    global active_cases
    global date

    # ---Coronavirus monitor_current - RAPID API STARTS HERE
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"

    querystring = {"country": country}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "12a507580amshde79d1bb69f1d34p1d38c6jsn5ea704a023bd"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    response_read = response.text
    # ---Coronavirus monitor_current - RAPID API ENDS HERE

    # Coronavirus monitor- printing to json
    convert_json = json.loads(response_read.replace("\'", '"'))

    with open("stats_by_country.json", "w") as text_file:
        json.dump(convert_json, text_file, indent=4)

    number = len(convert_json['latest_stat_by_country'])

    # If country does not exists return -1
    if number == 0:
        return -1

    # Else update active_cases and return 1
    else:
        # Coronavirus monitor- stats print categories
        num = convert_json['latest_stat_by_country'][0]['active_cases']
        date = convert_json['latest_stat_by_country'][0]['record_date']
        num = num.replace(',', '')
        active_cases = num
        return 1

# Function that takes yesterday's active cases of a country
# Saves statistics into yesterday_active_cases.json
# Return -1 if country does not exist. Return 1 if country exists.


def monitor_yesterday(country):
    global active_cases_yesterday
    global date  # Current holds the current date
    year = ""
    day = ""
    month = ""

    # Get yesterday's date
    date_time_divide = date.partition(" ")
    text_partition = date_time_divide[0].split("-")
    year = text_partition[0]
    month = text_partition[1]
    day = text_partition[2]
    day = str(int(day)-1)
    output_date = ""+year+"-"+month+"-"+day

    # ---Coronavirus monitor_current - RAPID API STARTS HERE
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/history_by_country_and_date.php"

    querystring = {"country": country, "date": output_date}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "12a507580amshde79d1bb69f1d34p1d38c6jsn5ea704a023bd"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    response_read = response.text
    # ---Coronavirus monitor_current - RAPID API ENDS HERE

    # Coronavirus monitor- printing to json
    convert_json = json.loads(response_read.replace("\'", '"'))

    with open("yesterday_by_country.json", "w") as text_file:
        json.dump(convert_json, text_file, indent=4)

    number = len(convert_json['stat_by_country'])

    # If country does not exists return -1
    if number == 0:
        return -1

    # Else update active_cases and return 1
    else:

        length = len(convert_json['stat_by_country'])
        # Coronavirus monitor- stats print categories
        num = convert_json['stat_by_country'][length -
                                              1]['active_cases']

        num = num.replace(',', '')
        active_cases_yesterday = num

        return 1

# Function that calculate the difference between today's and yesterday's active cases
# Return print statement


def active_cases_differences(active_cases, active_cases_yesterday):
    difference = float(active_cases) - float(active_cases_yesterday)
    statement = ""

    if difference > 0:
        percentage = (abs(difference)/float(active_cases))*100
        statement = "🤢 Cases 🅸🅽🅲🆁🅴🅰🆂🅴: " + \
            "%.2f" % percentage + "% 🤢" + \
            "\n\nUrge everyone to #stayathome and take care each other."

    elif difference < 0:
        percentage = (abs(difference)/float(active_cases))*100
        statement = "😻Cases 🅳🅴🅲🆁🅴🅰🆂🅴: " + \
            "%.2f" % percentage + "% 😻" + "\n\n#stayathome and keep it low!"

    return statement

# Twitter responsive function
# Function that reads through tweets that mentioned keywords and beginning from since_id
# Return the latest_since_id to be used in the next iteration


def check_mentions(api, keywords, since_id):

    logger.info("Retrieving mentions")
    new_since_id = since_id
    # Get all mentions using tweepy.Cursor
    mentions = tweepy.Cursor(api.mentions_timeline, since_id=since_id).items()
    # Reads every tweet in mention collection
    for tweet in mentions:
        new_since_id = max(tweet.id, new_since_id)
        try:
            # Split tweet text into array
            text = tweet.text.lower().split()
            country = text[2].lower()

            # If tweet can be replied
            if tweet.in_reply_to_status_id is not None:
                continue
            # If the tweet contains keywords
            if any(keyword in tweet.text.lower() for keyword in keywords):
                logger.info(f"Answering to {tweet.user.name}")
                # If country does not exists, tweet the right statement
                if(monitor_current(country) < 0):
                    printVar = "2020 COVID-19 Stats 🦠"+"\n\nHmm.. It looks like that country is not in our statistics 😷" + \
                        "\n\nPlease be wary that this data might not represent the latest and accurate data of your request."
                    api.update_status(
                        status=printVar, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                # If country exists, tweet the right statement with the statistics
                else:
                    monitor_current(country)
                    monitor_yesterday(country)
                    printVar = "2020 COVID-19 PROGRESS🦠"+"\nCountry: " + country + "\n\n" + \
                        active_cases_differences(
                            active_cases, active_cases_yesterday) + "\n\nActive cases yesterday: " + active_cases_yesterday + "\n Active cases today:" + active_cases
                    api.update_status(
                        status=printVar, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        except tweepy.TweepError as e:
            print(e.reason)

    return new_since_id


def main():
    # Starting since_id. Can put any number less than the latest tweet.
    since_id = 1243027569303158785

    while True:
        since_id = check_mentions(api, ["progress"], since_id)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
