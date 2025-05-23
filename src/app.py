from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from . import explkttns

load_dotenv()

app = App()

@app.command("/explkttns")
def handle_explkttns(ack, respond, command):
    # New game
    respond(
        text="New game of Exploding Kittens!",
        # ... bla bla bla
    )

def main():
    handler = SocketModeHandler(app)
    handler.start()

if __name__ == "__main__":
    main()
