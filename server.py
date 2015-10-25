import sys

import click
import flask
import pychromecast


cast = None
app = flask.Flask(__name__)


@click.command()
@click.option('--device', help='name of chromecast device')
def server(device):
    global cast

    print '>> trying to connect to %s' % device

    cast = pychromecast.get_chromecast(friendly_name=device)
    if cast is None:
        click.echo("Couldn't find device '%s'" % device)
        sys.exit(-1)

    print repr(cast)
    print 'connected, starting up...'

    app.run('0.0.0.0', 8183, debug=True)


@app.route('/', methods=['POST'])
def dispatch_request():
    body = flask.request.get_json()
    print body

    req = body['request']

    if req['type'] != 'IntentRequest':
        return 'nope', 400

    intent_handler = {
        'SkipMedia': skip_media,
        'PlayMedia': play_media,
        'PauseMedia': pause_media,
        'Reconnect': reconnect
    }.get(req['intent']['name'])

    if intent_handler:
        return intent_handler()

    return 'NO.', 400


def _format_response(message):
    body = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message
            },

            'shouldEndSession': True
        }
    }

    return flask.jsonify(**body)


# TODO: at some point should probably not have this return 200 OK
def _error(message=''):
    return _format_response(message)


def _success(message=''):
    return _format_response(message)


def reconnect():
    global cast

    cast = pychromecast.get_chromecast(friendly_name=cast.friendly_name)
    if cast is None:
        return _error('Failed to connect, is chromecast fucked again?')

    return _success('Reconnected.')


def skip_media():
    mc = cast.media_controller

    if not mc.status.supports_skip_forward:
        return _error("Skipping not supported")

    mc.skip()
    return _success()


def play_media():
    mc = cast.media_controller

    if mc.status.player_is_playing:
        return _error("Already playing")

    mc.play()
    return _success()


def pause_media():
    cast.media_controller.pause()
    return _success()


if __name__ == '__main__':
    server()
