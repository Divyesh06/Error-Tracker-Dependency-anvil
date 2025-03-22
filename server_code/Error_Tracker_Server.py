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
        
        if not app_tables.app_data.get():
            app_tables.app_data.add_row(app_id=anvil.app.id)
        
        error_row = app_tables.error.get(error_msg=error, traceback=traceback)
        user = anvil.users.get_user()
        
        if error_row:
            if error_row['status'] == "ignored": 
                return  # Don't do anything if error is ignored
            
            if app_tables.error.get(sessions=[session], error_msg=error, traceback=traceback):
                return  # Same error in this session already
            
            users = error_row['users']
            if user:
                users.append(user['email'])
                users = list(set(users))
            
            sessions = error_row['sessions']
            sessions.append(session)
            
            update_data = {
                "users": users,
                "user_count": len(users),
                "error_count": error_row['error_count'] + 1,
                "sessions": sessions,
                "traceback": traceback,
                "last_appeared": current_time
            }
            
            if error_row['status'] == "fixed":
                update_data["status"] = "reappeared"
                app_tables.timeline.add_row(type="error_reappeared", datetime=current_time, error=error_row)
            
            error_row.update(**update_data)
        else:
            users = [user['email']] if user else []
            error_row = app_tables.error.add_row(
                error_msg=error,
                users=users,
                user_count=len(users),
                status="pending",
                traceback=traceback,
                error_count=1,
                sessions=[session],
                first_appeared=current_time,
                last_appeared=current_time
            )
        
        app_tables.timeline.add_row(
            datetime=current_time,
            type="user_error",
            user_email=user['email'] if user else None,
            additional_info=additional_data,
            error=error_row
        )
        
    except Exception as e:
        print("Exception while tracking error:", str(e))
