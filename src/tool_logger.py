from datetime import datetime
from functools import wraps


tool_usage_history = []

def log_tool_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        param_names = func.__code__.co_varnames[:len(args)]
        input_data = {**dict(zip(param_names, args)), **kwargs}
        log_entry = {
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "tool_name": tool_name,
            "input": input_data,
            "output": None,
            "success": False,
            "error": None,
            "reason": ""
        }
        
        try:
            result = func(*args, **kwargs)
            log_entry.update({"output": result, "success": True})

            if tool_name == "detect_noise_words":
                log_entry["reason"] = f"Found {result.get('noise_count', 0)} noise words."
            elif tool_name == "score_topic_quality":
                log_entry["reason"] = f"Quality score is {result.get('quality_score')}."
            else:
                log_entry["reason"] = "Task completed."
                
            return result
        except Exception as e:
            log_entry["error"] = str(e)
            log_entry["reason"] = "Technical failure."
            return {"error": str(e)}
        finally:
            tool_usage_history.append(log_entry)
            
    return wrapper