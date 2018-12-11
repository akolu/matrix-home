# Matrix HOME

Matrix HOME is a home automation project built around Raspberry Pi 3 and [Matrix Creator One](https://creator.matrix.one) board.

## Features
* Offline wakeword listening
* Speech to text using Google API
* Fuzzy matching Google STT result (closest match to predetermined list of phrases)
* Visual feedback via LED array
* Send commands to Philips HUE or IR devices (TV, speakers, etc...) based on speech

## Prerequisites
1. Raspberry Pi
2. Creator Matrix One board
3. Philips Hue Bridge & some lamps (optional, HUE actions can be disabled easily in the code)
4. IR devices (you will need to add the relevant LIRC IR commands in the app.py yourself)

## Setting up & running
1. Follow the [docs](https://matrix-io.github.io/matrix-documentation/) how to set up and configure Matrix CORE for rpi.
2. Checkout the project and update [submodule](https://github.com/akukolu/matrix-led) from remote
3. Create some .pmdl hotword models with [snowboy](https://snowboy.kitt.ai/) and place them in `snowboy/models` or use the default one (Alexa)
4. [Set up Google API credentials](https://cloud.google.com/video-intelligence/docs/common/auth)
5. `pip install -r requirements.txt`
6. Press the button in Philips Hue bridge. You only need to do this step when running the app for the first time.
7. `python app.py ip.to.your.hue.bridge`

## Changelog
* `0.3.0` use proper speech to text api
* `0.2.0` move snowboy wakeword functionality to a package, python3 is now required
* `0.1.0` first "mvp" version
  
## Roadmap
* Make the project runnable in any device (for example Google AIY kit)

## Testing
`python -m unittest`

## License
Apache
