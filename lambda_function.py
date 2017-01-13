"""
This is a simply skill that reads (text to speech) the daily upper room
devotional. This skill in unofficial and not authorized by the Upper Room
organization.
"""

from __future__ import print_function
import urllib
import re
import time
import BeautifulSoup

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        "card": {
            "type": "Standard",
            "title": "Unofficial Upper Room - " + title,
            "text": output,
            "image": {
                "smallImageUrl": "https://s3.amazonaws.com/dbainbri-alexa-card-images/images/ur_small.png",
                "largeImageUrl": "https://s3.amazonaws.com/dbainbri-alexa-card-images/images/ur_large.png"
            }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
def strip_html(d):
    """ Remove bracketed strings and special characters from the given input.
    """
    cleanr = re.compile('<.*?>')
    cleanr2 = re.compile('&[a-z]*;')
    cleantext = re.sub(cleanr2, '', re.sub(cleanr, '', d))

    cleanr = re.compile
    return cleantext

def strip_verse_numbers(d):
    """ Removes verse numbers from a bible passage based on patterns
    """
    cleanr = re.compile('[0-9]+:[0-9]+[^-]')
    cleantext = re.sub(cleanr, '', d)
    return cleantext

def add_pause(d):
    """ Insures a space after a period so that the text to speech engine
    will pause
    """
    cleanr = re.compile('\.')
    cleantext = re.sub(cleanr, '. ', d)
    return cleantext

def strip_copyright(d):
    """ Strip the copyright from the passage reading.
    """
    cleanr = re.compile('The scripture quotation is from.*')
    cleantext = re.sub(cleanr, '. ', d)
    return cleantext

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Unofficial Upper Room Skill. " \
                    "This skill can read the passage, message, thought for the day, " \
                    "prayer focus, prayer, and author for the day's upper " \
                    "room devotional. This skill is not sponsored, endorsed, or " \
                    "authorized by the Upper Room organization. " \
		    "For example, you can have the Unofficial Upper Room skill read " \
		    "today's Bible passage by saying, \"Read the passage\"." \
		    "What would you like the Unofficial Upper Room to read?"

    reprompt_text = "What would you like the Unofficial Upper Room to read?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Unofficial Room Skill. " \
                    "God bless you."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_passage(intent):
    """ Extracts the daily passage from the devotional.
    """

    link = "http://devotional.upperroom.org/devotionals/%s/passage" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    speech_output = add_pause(strip_verse_numbers(strip_copyright(strip_html(urllib.urlopen(link).read()))))
    should_end_session = True
    card_title = "Today's Bible Passage"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_prayer(intent):
    """ Extracts the daily Prayer from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Today's Prayer"


    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = add_pause(strip_html(str(soup.find("div", {"id": "prayer"}).findChild().findNextSibling())))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_prayer_focus(intent):
    """ Extracts the daily Prayer focus from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Today's Prayer Focus"

    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = add_pause(strip_html(str(soup.find("div", {"id": "prayer_focus"}).contents[1])))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_snippet(intent):
    """ Extracts the daily passage snipet from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Today's Bible Passage Snippet"

    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = add_pause(strip_verse_numbers(strip_html(str(soup.find("div", {"id": "scripture_snippet"})))))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_thought(intent):
    """ Extracts the daily thought for the day from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Thought for the Day"

    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = ""
    data = soup.find("div", {"id": "thought"}).findChild()
    while data:
        if data.name != u'h2':
                speech_output += str(data)
        data = data.findNextSibling()
    speech_output = add_pause(strip_html(speech_output))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_message(intent):
    """ Extracts the daily message from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Today's Devotional Message"

    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = ""
    data = soup.find("div", {"id": "scripture_snippet"}).findNextSibling()
    while data.name != u'div':
        speech_output += str(data)
        data = data.findNextSibling()
    speech_output = add_pause(strip_html(speech_output))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_author(intent):
    """ Extracts the daily author from the devotional.
    """
    link = "http://devotional.upperroom.org/devotionals/%s" % time.strftime("%Y-%m-%d")
    session_attributes = {}
    reprompt_text = ""
    card_title = "Author of Today's Devotional Message"

    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link).read())
    speech_output = strip_html(str(soup.find("h2", {"class": "author-name"})))
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ReadPassage":
        return get_passage(intent)
    elif intent_name == "ReadSnippet":
        return get_snippet(intent)
    elif intent_name == "ReadMessage":
        return get_message(intent)
    elif intent_name == "ReadPrayerFocus":
        return get_prayer_focus(intent)
    elif intent_name == "ReadThoughtForTheDay":
        return get_thought(intent)
    elif intent_name == "ReadPrayer":
        return get_prayer(intent)
    elif intent_name == "ReadAuthor":
        return get_author(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
