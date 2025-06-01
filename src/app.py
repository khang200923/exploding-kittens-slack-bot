from collections import deque
from enum import Enum
import threading
from typing import Any, Dict, Tuple
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from markdown_to_mrkdwn import SlackMarkdownConverter
import src.explkttns.game
from src.explkttns.game import Game
from src.explkttns.player import Player

load_dotenv()

app = App()
converter = SlackMarkdownConverter()

class GameState(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

MsgId = Tuple[str, str] # (channel_id, ts)
MsgIdUser = Tuple[str, str, str] # (channel_id, ts, user_id)
MsgAction = Tuple[str, str, str, str] # (channel_id, ts, user_id, action)
data: Dict[MsgId, Any] = {}
queue: deque[MsgAction] = deque()
queue_condition = threading.Condition()

@app.command("/explkttns")
def handle_explkttns(ack, say, command, respond):
    ack()

    if command['text'].strip().lower() == "ui_guide":
        with open("interface.md", "r") as f:
            content = f.read()
            respond(
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": converter.convert(content)
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Close this guide"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Close",
                                "emoji": True
                            },
                            "action_id": "close-guide"
                        }
                    }
                ]
            )
        return

    if command['text'].strip().lower() != "new":
        respond(text="Invalid command. Use `/explkttns new` to start a new game.")
        return

    # New game
    x = say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "New game of Exploding Kittens!",
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Type `/explkttns ui_guide` for a guide on how to use the interface."
                    }
                ]
            }
        ],
        text="New game of Exploding Kittens!"
    )
    ts = x['ts']
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Invite someone"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Invite"
                    },
                    "action_id": "invite"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Start the game"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Start",
                        "emoji": True
                    },
                    "action_id": "start-game"
                }
            },
            # {
            #     "type": "section",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": "Cancel the game"
            #     },
            #     "accessory": {
            #         "type": "button",
            #         "text": {
            #             "type": "plain_text",
            #             "text": "Cancel",
            #             "emoji": True
            #         },
            #         "action_id": "cancel-game"
            #     }
            # }
        ],
        metadata={
            'event_type': 'pregame_actions',
            'event_payload': {
                'allowed_user': command['user_id'],
            }
        },
        thread_ts=ts
    )

    data[(command['channel_id'], ts)] = {
        'game_state': GameState.NEW,
        'host': command['user_id'],
        'players': {command['user_id']}
    }

@app.action("invite")
def handle_invite(ack, client, action, body):
    ack()

    if body["user"]["id"] != data[(body["channel"]["id"], body["message"]["thread_ts"])]['host']:
        client.chat_postEphemeral(
            channel=body["channel"]["id"],
            thread_ts=body["message"]["thread_ts"],
            user=body["user"]["id"],
            text="Only the host can invite players."
        )
        return

    if data[(body["channel"]["id"], body["message"]["thread_ts"])]['game_state'] != GameState.NEW:
        client.chat_postEphemeral(
            channel=body["channel"]["id"],
            thread_ts=body["message"]["thread_ts"],
            user=body["user"]["id"],
            text="You cannot invite players after the game has started or completed."
        )
        return

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "invite_modal",
            "title": {
                "type": "plain_text",
                "text": "Invite someone",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Invite",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "multi_users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select users",
                            "emoji": True
                        },
                        "action_id": "invite-modal",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": " ",
                        "emoji": True
                    }
                }
            ],
            "private_metadata": f"{body['channel']['id']} {body['message']['thread_ts']}"
        }
    )

@app.view("invite_modal")
def handle_invite_modal(ack, view, body, client):
    ack()
    values = view["state"]["values"]
    invite_modal = next(x["invite-modal"] for x in values.values() if "invite-modal" in x)
    users = invite_modal["selected_users"]

    if len(data[(view["private_metadata"].split()[0], view["private_metadata"].split()[1])]['players'] | users) > 5:
        client.chat_postEphemeral(
            channel=view["private_metadata"].split()[0],
            thread_ts=view["private_metadata"].split()[1],
            user=body["user"]["id"],
            text="You can only have up to 5 players in a game."
        )
        return

    data[(view["private_metadata"].split()[0], view["private_metadata"].split()[1])]['players'].update(users)
    client.chat_postMessage(
        channel=view["private_metadata"].split()[0],
        thread_ts=view["private_metadata"].split()[1],
        text=f"<@{body['user']['id']}> has invited {', '.join(f'<@{x}>' for x in users)}"
    )

@app.action("close-guide")
def handle_close_guide(ack, body, client):
    ack()
    channel = body["channel"]["id"]
    thread_ts = body["message"]["thread_ts"]

    client.chat_delete(
        channel=channel,
        ts=thread_ts
    )

@app.action("start-game")
def handle_start_game(ack, body, client):
    ack()
    channel = body["channel"]["id"]
    thread_ts = body["message"]["thread_ts"]

    if body["user"]["id"] != data[(channel, thread_ts)]['host']:
        client.chat_postEphemeral(
            channel=channel,
            thread_ts=thread_ts,
            user=body["user"]["id"],
            text="Only the host can start the game."
        )
        return

    if data[(channel, thread_ts)]['game_state'] != GameState.NEW:
        client.chat_postEphemeral(
            channel=channel,
            thread_ts=thread_ts,
            user=body["user"]["id"],
            text="You cannot start the game after it has started or completed."
        )
        return

    data[(channel, thread_ts)]['game_state'] = GameState.IN_PROGRESS
    data[(channel, thread_ts)]['game'] = Game(
        names=list(data[(channel, thread_ts)]['players'])
    )

    client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text="The game has started! Players are: " + ", ".join(f"<@{x}>" for x in data[(channel, thread_ts)]['players'])
    )
    client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=f"It's <@{data[(channel, thread_ts)]['game'].current_player}> turn to play"
    )

@app.event("message")
def handle_message(ack, body):
    ack()

    channel = body["event"]["channel"]
    thread_ts = body["event"].get("thread_ts", None)
    user = body["event"]["user"]
    if thread_ts is None or (channel, thread_ts) not in data:
        return
    if data[(channel, thread_ts)]['game_state'] != GameState.IN_PROGRESS:
        return
    if user not in data[(channel, thread_ts)]['players']:
        return
    if 'text' not in body['event']:
        return
    text = body['event']['text'].strip().lower()
    if text.startswith("#") or text.startswith("//") or text.startswith(".//"):
        return
    with queue_condition:
        queue.append((channel, thread_ts, user, text))
        queue_condition.notify()

def process_queue():
    while True:
        with queue_condition:
            while not queue:
                queue_condition.wait()
            action = queue.popleft()
        execute(*action)

def execute(channel: str, thread_ts: str, user: str, text: str):
    ...

def main():
    handler = SocketModeHandler(app)
    threading.Thread(target=process_queue, daemon=True).start()
    handler.start()

if __name__ == "__main__":
    main()
