# Upper Room Alexa Skill
The Upper Room Alexa skill provides an interface from Amazon's Alexa (echo)
home devices to the daily Upper Room devotional information hosted at
http://devotional.upperroom.org.

Through this skill, Alexa will read (text to speech) the components of the
daily devotional, including:

- Bible Passage
- Bible Passage Snippet
- Devotional Message
- Devotional Message Author
- Though for the Day
- Prayer Focus
- Prayer

## Commands
To have Alexa read the Upper Room daily the following *utterances* can be used

- Bible Passage - *Alexa ask the Upper Room to read the Bible passage*
- Bible Passage Snippet - *Alexa ask the Upper Room to read the snippet*
- Devotional Message - *Alexa ask the Upper Room to read the message*
- Devotional Message Author - *Alexa ask the Upper Room who is the author*
- Though for the Day - *Alexa ask the Upper Room what is the thought for the day*
- Prayer Focus - *Alexa ask the Upper Room what is the prayer focus*
- Prayer - *Alexa ask the Upper Room to read the prayer*

#### Enhancements
Currently an utterance does not exists to read *all* components of the daily
devotional or to specify the *day* for the devotional the user wishes to hear.
Both of these enhancement may be added in the future.

## Technical
This skill leverages the daily devotional content provided by the Upper Room
organization through their web URL devotional.upperroom.org and is dependent
on the `HTML` tags, IDs, and structure of that web site. If the web site
significantly changes it is likely that this skill will need to updated to
operate correctly.

It would make my life much easier if the Upper Room exposes the components
of the daily devotional as separate web services, such that the raw text of the
devotional could be accessed via a URL such as `http://devotional.upperroom.org/2017-01-01/passage` and `http://devotional.upperroom.org/2017-01-01/message`.

## Notices
This skill is not an official skill produced or authorized by the Upper Room
organization. This skill just *screen scrapes* the freely available information
from the Upper Room's web site and uses Alexa's text to speech capability for
play back.

The Upper Room name and contents of the daily devotional are all the property
of the Upper Room organization. A very large thank you to them for making this
information available to the public. **Please** consider subscribing or
donating to this organization.
