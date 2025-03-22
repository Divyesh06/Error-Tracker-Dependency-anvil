from anvil.js.window import UAParser, JSON, fetch
import anvil.server
import anvil.js
import json


def convert_to_py(js_object):
    return json.loads(JSON.stringify(js_object))
    
def collect_error(err, collect_device_info = False, **additional_data):
    try:
        if "debug" in anvil.app.environment.tags:
            return
        err_str = f"{type(err).__name__}: {str(err)}"
        traceback = anvil.js.call("get_error_traceback",err)
    
        if collect_device_info:
            
            ua_data = {k: ' '.join(map(str, dict(v).values())) if isinstance(v, dict) else v
                            for k, v in convert_to_py(UAParser()).items()}
            additional_data.update(ua_data)
            
        fetch(anvil.server.get_api_origin()+"/internal/log_error", {
            "method" : "POST",
            "body" : json.dumps({"error": err_str, "additional_data": additional_data, "traceback":traceback}),
            "headers": {
                "Content-Type": "application/json",
            },
        })
    except Exception as e:
        print(f"(Error Tracker) Failed to Report Error due to the following exception: {e}")