'''Copyright (c) 2023 amirali irvany `MIT LICENSE`'''

from pyrubi import Client
from re import sub
from langdetect import detect
from random import choice
from requests import get
from requests.exceptions import JSONDecodeError


def main():
    client = Client(session='session', time_out=10)
    for update in client.on_message(filters=['Channel', 'User']):
        _me = client.get_me()['user']['user_guid']
        _message_id = client.get_messages_by_id(
            object_guid=update.object_guid,
            message_ids=[update.message_id]
        )
        try:
            _guid_message = client.get_messages_by_id(
                object_guid=update.object_guid,
                message_ids=[_message_id['messages'][0]['reply_to_message_id']]
            )
            if _me == _guid_message['messages'][0]['author_object_guid']:
                # Using this newly added feature,
                # you can get your answer just by replying to one of the bot's messages!
                client.send_text(
                    object_guid=update.object_guid,
                    text='__Please wait...__',
                    message_id=update.message_id
                )
                responce = get(f'https://pyrubi.b80.xyz/chat.php?text={update.text}').json()
                client.send_text(
                    object_guid=update.object_guid,
                    text=responce[0]['text'],
                    message_id=update.message_id
                )
        except KeyError:
            pass

        try:
            if update.text.startswith('+'):
                if update.text == '+':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Please Enter a text\nExample: __+hello__'
                    )
                else:
                    client.send_text(
                        object_guid=update.object_guid,
                        text='__Please wait...__',
                        message_id=update.message_id
                    )
                    responce = get(f'https://pyrubi.b80.xyz/chat.php?text={update.text[1:]}').json()
                    client.send_text(
                        object_guid=update.object_guid,
                        text=responce[0]['text'],
                        message_id=update.message_id
                    )


            elif update.text.startswith('voice'):
                if update.text == 'voice':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Please enter a text\nExample: __voice man hello__',
                        message_id=update.message_id
                    )
                else:
                    client.send_text(
                        object_guid=update.object_guid,
                        text='__Please wait...__',
                        message_id=update.message_id
                    )
                    mod = update.text.split()[1].strip()
                    text = update.text.split()[-1].strip()
                    try:
                        request = get(f'https://pyrubi.b80.xyz/voice.php?text={text}&mod={mod}').json()
                        responce = get(request['result'])
                        with open('.voice.mp3', 'wb') as file_:
                            file_.write(responce.content)

                        client.send_voice(
                            object_guid=update.object_guid,
                            file='.voice.mp3',
                            message_id=update.message_id,
                            text=f'your voice is realy👍\ncontent:\"{text}\"\ndeveloper: @slash_dev'
                        )
                    except JSONDecodeError:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='❌ Problem!\nThis is your problem\nPlease read the guide again',
                            message_id=update.message_id
                        )
                    except:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='❌ Problem!\nThis is our problem\nPlease try again',
                            message_id=update.message_id
                        )


            elif update.text.startswith('img'):
                if update.text == 'img':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Please Enter a text\nExample: __img wolf__',
                        message_id=update.message_id
                    )
                else:
                    client.send_text(
                        object_guid=update.object_guid,
                        text='__Please wait...__',
                        message_id=update.message_id
                    )
                    text = sub('img', '', update.text).strip()
                    request = get(f'https://haji-api.ir/prompts/?text={text}').json()
                    responce = get(choice(request['result']))
                    with open('.img.png', 'wb') as file_:
                        file_.write(responce.content)

                    client.send_image(
                        object_guid=update.object_guid,
                        file='.img.png',
                        text=f'your image is realy👍\ncontent:\"{text}\"\ndeveloper: @slash_dev',
                        message_id = update.message_id,
                    )


            elif update.text == '$' or update.text == 'usd':
                client.send_text(
                    object_guid=update.object_guid,
                    text='__Please wait...__',
                    message_id=update.message_id
                )
                responce = get('https://pyrubi.b80.xyz/usd.php').json()
                responce_ = responce['result']['Us Dollar']
                client.send_text(
                    object_guid=update.object_guid,
                    text='**Us Dollar:**\n\nAverage: __%s__\nMax: __%s__\nMin: __%s__' % (
                        responce_['Average'], responce_['Max'], responce_['Min']
                    ),
                    message_id=update.message_id
                )


            elif update.text.startswith('font'):
                if update.text == 'font':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Please Enter a text\nExample: __font amir__',
                        message_id=update.message_id
                    )
                else:
                    client.send_text(
                        object_guid=update.object_guid,
                        text='__Please wait...__',
                        message_id=update.message_id
                    )
                    _text = update.text.split('font')[-1]
                    if detect(text) in ['fa', 'ar', 'ur']:
                        request = get(f'http://api.codebazan.ir/font/?type=fa&text={_text}').json()
                    else:
                        request = get(f'http://api.codebazan.ir/font/?text={_text}').json()

                    _message_id = client.get_messages_by_id(
                        object_guid=update.object_guid,
                        message_ids=[update.message_id]
                    )
                    user_guid = _message_id['messages'][0]['author_object_guid']
                    for num in range(1, 10):
                        try:
                            client.send_text(
                                object_guid=user_guid,
                                text=request['result'][str(num)],
                                message_id=update.message_id
                            )
                        except KeyError:
                            client.send_text(
                                object_guid=user_guid,
                                text=request['Result'][str(num)],
                                message_id=update.message_id
                            )
                    client.send_text(
                        object_guid=update.object_guid,
                        text='The fonts have been sent to your PV',
                        message_id=update.message_id
                    )


            elif update.text == 'news':
                client.send_text(
                    object_guid=update.object_guid,
                    text='__Please wait...__',
                    message_id=update.message_id
                )
                _responce = get(f'https://one-api.ir/rss/?token={token}&action=irinn').json()
                responce = choice(_responce['result']['item'])
                client.send_text(
                    object_guid=update.object_guid,
                    text='**%s**\n\n%s\n\n__%s__' % (
                        responce['title'], responce['description'], responce['pubDate']
                    ),
                    message_id=update.message_id
                )


            elif update.text == 'joke':
                responce = get(f'https://one-api.ir/joke/?token={token}').json()
                client.send_text(
                    object_guid=update.object_guid,
                    text=responce['result'],
                    message_id=update.message_id
                )


            elif update.text == 'link':
                info = client.get_chat_info(object_guid=update.object_guid)
                try:
                    _results = client.get_link(object_guid=info['group']['group_guid'])
                    group_link = _results['join_link']
                    group_title = info['group']['group_title']
                    client.send_text(
                        object_guid=update.object_guid,
                        text=f'The link to the {group_title} group is:\n\n``{group_link}``'
                    )
                except:
                    client.send_text(
                        object_guid=update.object_guid,
                        text='**Please admin the robot account in the group❗**',
                        message_id=update.message_id
                    )


            elif update.text == 'test':
                client.send_text(
                    object_guid=update.object_guid,
                    text='The bot is active ✅',
                    message_id=update.message_id
                )


            elif update.text == 'time':
                responce = get('http://api.codebazan.ir/time-date/?td=all')
                client.send_text(
                    object_guid=update.object_guid,
                    text=responce.text,
                    message_id=update.message_id
                )


        except TimeoutError:
            client.send_text(
                object_guid=update.object_guid,
                text='timeout-err',
                message_id=update.message_id
            )


if __name__ == '__main__':
    main()
