import anvil.server
from anvil.tables import app_tables
import anvil.users
from datetime import datetime

@anvil.server.http_endpoint("/internal/log_error")
def log_error():

        body = anvil.server.request.body_json
        error = body['error']
        print(error)
        
        additional_data = body['additional_data']
        additional_data['session'] = anvil.server.get_session_id()
        error_row = app_tables.error.get(Error=error)
        user = anvil.users.get_user()
        if error_row:
            users = error_row['Users']
            users.append(anvil.users.get_user())
            error_row['Users'] = list(set(users))
            error_row['User_Count'] = len(users)
            if error_row['status'] == "fixed":
                error_row['status'] = "reappeared"
        else:
            error_row = app_tables.error.add_row(Error=error,timeline=[],Users=[user], User_Count=1, status="pending")
    
        current_time = datetime.utcnow()
        error_row['last_appeared'] = current_time
        
        new_timeline = app_tables.timeline.add_row(datetime=current_time, type="user_error", User=user, Additional_Info=additional_data)
        
        timeline = error_row['timeline']
        timeline.append(new_timeline)
        error_row['timeline'] = timeline
