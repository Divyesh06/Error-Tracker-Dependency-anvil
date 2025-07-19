# Error Tracker Dependency for Anvil

The dependency used for collecting errors to be displayed in [Dashboard](https://github.com/Divyesh06/Error-Tracker-anvil)

## How to use

In your main app, you can call the following function to collect errors

```python
from Error_Tracker.error_tracker import collect_error

try: 
   #Something
except Exception as e:
   collect_error(e)

```

Or you can attach it to your Error Handler 

```python
def error_handler(err):
   collect_error(err)

set_default_error_handling(error_handler)
```
You can also collect the device and browser details or any custom data you require.
```python
collect_err(err, collect_device_info = True)

#Or collect any custom data

collect_err(err, url_hash = get_url_hash(), form = get_open_form())
```
