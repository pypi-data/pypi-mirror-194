import traceback
import requests

def capture_alert(model_id, exception):
    if hasattr(exception, '__traceback__'):
        traceback_str = ''.join(traceback.format_tb(exception.__traceback__))
        req = {
            "model_name": model_id,
            "model_id": model_id,
            "exception": str(exception),
            "traceback": traceback_str,
            "status": "ERROR",
            "prompt": "None"
            }
        res = requests.post("http://0.0.0.0:8000/api/live/models/log",json=req)
        print(res.text())
        return "Alert has been captured."