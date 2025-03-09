from anvil.js import window
import anvil.server
import json
def collect_error(err, **additional_data):
    window.fetch(anvil.server.get_api_origin()+"/internal/log_error", {
        "method" : "POST",
        "body" : json.dumps({"error": str(err), "additional_data": additional_data}),
        "headers": {
            "Content-Type": "application/json",
        },
    })