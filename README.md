# alexacast

Alexa skill to control local Chromecast devices. Check out the documentation on
[alexandra](https://github.com/erik/alexandra) for setup instructions. You'll
need to run it on the same network as your Chromecast.

TL;DR:

```
$ pip install -r requirements.txt
$ python server.py --device='Your Chromecast Name'
```
Then log in the [Amazon Developer Portal](https://developer.amazon.com/login.html) to setup the skill.


## usage

(assuming your trigger word is "chromecast")

- "alexa, ask chromecast to skip this"
- "alexa, ask chromecast to pause"
- "alexa, ask chromecast to play"
- "alexa, ask chromecast to reconnect"
  - if everything stops working this might fix it
- "alexa, ask chromecast to reboot"
  - sometimes the chromecast gets itself into dumb states and needs to be
    restarted.
