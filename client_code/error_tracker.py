from anvil.js import window
import anvil.server
import anvil.js
import json
def collect_error(err, **additional_data):
    
    traceback = anvil.js.call("get_error_traceback",err)
    
    window.fetch(anvil.server.get_api_origin()+"/internal/log_error", {
        "method" : "POST",
        "body" : json.dumps({"error": str(err), "additional_data": additional_data, "traceback":traceback}),
        "headers": {
            "Content-Type": "application/json",
        },
    })