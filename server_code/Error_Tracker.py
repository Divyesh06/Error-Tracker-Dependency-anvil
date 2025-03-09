import anvil.server
from anvil.tables import app_tables,batch_update
import anvil.users
from datetime import datetime

@anvil.server.http_endpoint("/internal/log_error")
def log_error():
    try:
        current_time = datetime.utcnow()
        body = anvil.server.request.body_json
        error = body['error']
        traceback = body['traceback']
        session = anvil.server.get_session_id()
        additional_data = body['additional_data']
        additional_data['session'] = session
        error_row = app_tables.error.get(Error=error, Traceback = traceback)
        user = anvil.users.get_user()
        
        if error_row:
            if session in error_row['Sessions']:
                return
            if user:
                users = error_row['Users']
                users.append(anvil.users.get_user())
                users = list(set(users))
                error_row['Users'] = users
                error_row['User_Count'] = len(users)
            error_row['Error_Count'] += 1
            sessions = error_row['Sessions']
            sessions.append(session)
            error_row['Sessions'] = sessions
            error_row['Traceback'] = traceback
            if error_row['status'] == "fixed":
                error_row['status'] = "reappeared"
        else:
            error_row = app_tables.error.add_row(Error=error,timeline=[],Users=[user], User_Count=1, status="pending", Traceback = body['traceback'], Error_Count = 1, Sessions = [session], first_appeared = current_time)
    
        
        error_row['last_appeared'] = current_time
            
        new_timeline = app_tables.timeline.add_row(datetime=current_time, type="user_error", User=user, Additional_Info=additional_data)
        
        timeline = error_row['timeline']
        timeline.append(new_timeline)
        error_row['timeline'] = timeline
        
    except Exception as e:
        app_tables.error.add_row(Error = str(e))
