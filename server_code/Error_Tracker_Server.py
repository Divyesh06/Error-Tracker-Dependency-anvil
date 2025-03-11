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
        
        error_row = app_tables.error.get(error_msg = error, traceback = traceback)
        user = anvil.users.get_user()
        
        if error_row:
            if app_tables.error.get(sessions = [session], error_msg = error, traceback = traceback):
                return #Same error in this session already
            if user:
                users = error_row['users']
                users.append(anvil.users.get_user())
                users = list(set(users))
                error_row['users'] = users
                error_row['user_count'] = len(users)
            error_row['error_count'] += 1
            sessions = error_row['sessions']
            sessions.append(session)
            error_row['sessions'] = sessions
            error_row['traceback'] = traceback
            if error_row['status'] == "fixed":
                error_row['status'] = "reappeared"
                app_tables.timeline.add_row(type="error_reappeared", datetime = current_time, error = error_row)
        else:
            if not user:
                users = []
            else:
                users = [user]
            error_row = app_tables.error.add_row(error_msg = error, users=users, user_count=1, status="pending", traceback = body['traceback'], error_count = 1, sessions = [session], first_appeared = current_time)

        error_row['last_appeared'] = current_time
            
        app_tables.timeline.add_row(datetime=current_time, type="user_error", user=user, additional_info = additional_data, error = error_row)
        
    except Exception as e:
        app_tables.error.add_row(error_msg = str(e))
