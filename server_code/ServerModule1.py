import anvil.server
from anvil.tables import app_tables
import anvil.users
from datetime import datetime

@anvil.server.http_endpoint("/internal/log_error")
def log_error():
    body = anvil.server.request.body_json
    error = body['error']
    additional_data = body['additional_data']
    additional_data['session'] = anvil.server.get_session_id()
    error_row = app_tables.error.get(Error=error)
    user = anvil.users.get_user()
    if error_row:
        users = error_row['Users']
        users.append(anvil.users.get_user())
        error_row['Users'] = users
        error_row['User_Count'] = len(users)
        if error['status'] == "fixed":
            error['status'] == "reappeared"
    else:
        error_row = app_tables.error.add_row(Error=error,timeline=[],Users=[user], User_Count=1, status="pending")

    error_row['last_appeared'] = datetime.utcnow()

    new_timeline = app_tables.ti