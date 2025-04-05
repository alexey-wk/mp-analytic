import time
from collections import deque

def limit_calls(max_calls=5, time_frame=60):
    timestamps = deque()
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            curr_time = time.time()
            
            while timestamps and timestamps[0] < curr_time - time_frame:
                timestamps.popleft()
            
            if len(timestamps) > max_calls:
                sleep_time = timestamps[0] + time_frame - curr_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    curr_time = time.time()

                    while timestamps and timestamps[0] < curr_time - time_frame:
                        timestamps.popleft()
            
            timestamps.append(curr_time)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
