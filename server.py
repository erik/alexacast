import sys

import alexandra
import click
import pychromecast


device_name = None
cast = None
app = alexandra.Application()


@click.command()
@click.option('--device', help='name of chromecast device', required=True)
def server(device):
    global cast
    global device_name

    print('>> trying to connect to {}'.format(device))

    device_name = device
    cast = pychromecast.get_chromecast(friendly_name=device)
    if cast is None:
        click.echo("Couldn't find device '{}'".format(device))
        sys.exit(-1)

    print(repr(cast))
    print('connected, starting up...')

    app.run('0.0.0.0', 8183)


@app.intent('Reconnect')
def reconnect(slots, session):
    global cast

    cast = pychromecast.get_chromecast(friendly_name=device_name)

    if cast is None:
        return alexandra.respond(
            'Failed to connect to Chromecast named %s.' % device_name)

    return alexandra.respond('Reconnected.')


@app.intent('SkipMedia')
def skip_media(slots, session):
    mc = cast.media_controller

    if not mc.status.supports_skip_forward:
        return alexandra.respond("Skipping not supported")

    mc.skip()
    return alexandra.respond()


@app.intent('PlayMedia')
def play_media(slots, session):
    mc = cast.media_controller

    if mc.status.player_is_playing:
        return alexandra.respond("Already playing")

    mc.play()
    return alexandra.respond()


@app.intent('PauseMedia')
def pause_media(slots, session):
    mc = cast.media_controller

    if not mc.status.player_is_playing:
        return alexandra.respond("Already paused")

    mc.pause()
    return alexandra.respond()


@app.intent('Reboot')
def reboot(slots, session):
    cast.reboot()
    return alexandra.respond()


if __name__ == '__main__':
    server()
