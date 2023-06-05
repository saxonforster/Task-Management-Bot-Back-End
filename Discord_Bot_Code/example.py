from test_commands import TestBotCommands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ['TEST_TOKEN']
c = TestBotCommands(TOKEN)

# sends message to testingbot channel
c.send_message("testing")

# gets last message sent in testing bot channel
message = c.read_last_message()



