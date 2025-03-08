import anvil.server


@anvil.server.http_endpoint("/internal/log_error")
def log_error():
    body = anvil.server.request.body_json
    error = body['error']
    additional_data = body['additional_data']