from dotenv import load_dotenv
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_pushover_webhook.plugin import PushoverAction

load_dotenv()

init = {
    "source": {"id": "3eecb528-e9c1-43a5-980b-314d1d21f9d7"},
    "message": "Test message from Risto"
}

payload = {}


x = run_plugin(PushoverAction, init, payload)
print(x)
