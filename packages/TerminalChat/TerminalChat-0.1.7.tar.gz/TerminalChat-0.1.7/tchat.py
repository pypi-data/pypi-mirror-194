import datetime
import click
import requests
import os
import pytz
import tzlocal

BASE_URL = "https://kind-moss-bb46b8b1ffc44c4ebf8b65aac6c47177.azurewebsites.net/api"
USER_ID_FILENAME = os.path.join(os.path.expanduser("~"), ".tchat_id")


@click.group()
def cli():
    pass


@cli.command()
def sign_up():
    """Command to sign up."""
    if os.path.exists(USER_ID_FILENAME):
        user_id, user_name = get_user_info()
        if user_id is not None:
            click.echo(
                f'Hi, {user_name}! You are already signed up with ID {user_id}.')
            return
        # else, continue creating new file
    user_name = click.prompt('Name', type=str)
    click.echo('Creating user %s' % user_name)
    res = requests.post(BASE_URL + '/users/', json={'name': user_name})
    if res.status_code == 201:
        user_id = res.json()['data']['id']
        with open(USER_ID_FILENAME, "w") as file:
            file.write("{},{}".format(str(user_id), user_name))
        click.echo('User created! Your ID: %s' % user_id)
    else:
        click.echo(f'Error creating user: \n {res.text}')


@cli.command()
def send():
    """Command to send a message."""
    user_id, _ = get_user_info()
    if user_id is None:
        click.echo('You must create a user first!\nUse command: `tchat sign_up`')
        return

    receiver_options = requests.get(BASE_URL + '/users/').json()['data']
    if receiver_options is []:
        click.echo('No users to send messages to!')
        return

    click.echo('Who would you like to message? Options:')
    for user in receiver_options:
        click.echo('ID: %s, Name: %s' % (user['id'], user['name']))
    if len(receiver_options) == 0:
        click.echo('No users to send messages to!')
        return

    click.echo()

    receiver_id = click.prompt('Receiver ID', type=int)

    click.echo()

    content = click.prompt('Message content', type=str)

    click.echo('Sending message...')
    res = requests.post(BASE_URL + '/messages/', json={
        'content': content,
        'sender_id': user_id,
        'receiver_id': receiver_id
    })
    if res.status_code == 201:
        click.echo('Message sent!')
    else:
        click.echo(f'Error creating message: \n {res.text}')


@cli.command()
@click.option('-a', '--all', is_flag=True, help='Get all messages.')
def read(all):
    """Command to get unread messages,  use --all to get all messages."""
    user_id, user_name = get_user_info()
    if user_id is None:
        click.echo('You must create a user first!')
        return

    res = requests.get(
        '{}/users/{}/messages/{}'.format(BASE_URL,
                                         user_id, '' if all else '?unread=true')
    )
    if res.status_code == 200:
        data = res.json().get('data')
        click.echo()
        local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
        for message in data:
            date = message.get("date")
            utc_time = datetime.datetime.strptime(
                date, '%Y-%m-%d %H:%M:%S.%f')
            local_time = utc_time.replace(
                tzinfo=pytz.utc).astimezone(local_timezone)
            content = message.get("content")
            sender_id = message.get("sender_id")
            sender_name = message.get("sender_name")
            if local_time.year == datetime.datetime.now().year:
                if local_time.day == datetime.datetime.now().day:
                    date_formatted = local_time.strftime('today at %-I:%M%p')
                elif local_time.day == datetime.datetime.now().day - 1:
                    date_formatted = local_time.strftime(
                        'yesterday at %-I:%M%p')
                else:
                    date_formatted = local_time.strftime(
                        'on %b %d at %-I:%M%p')
            else:
                date_formatted = local_time.strftime(
                    'on %b %d, %Y at %-I:%M%p')
            click.echo(
                f'{sender_name} (ID: {sender_id}) {date_formatted}: {content}')
        if not data:
            click.echo('Hi {}! No{} messages.'.format(
                user_name, '' if all else ' unread'))
        click.echo()
    else:
        click.echo(f'Error getting messages: \n {res.text}')


def get_user_info():
    """Helper to get a user id and name from the ID file."""
    user_id = None
    user_name = None
    if os.path.exists(USER_ID_FILENAME):
        with open(USER_ID_FILENAME, "r") as file:
            user_id, user_name = file.read().split(',')
    return int(user_id), user_name


if __name__ == '__main__':
    cli()
