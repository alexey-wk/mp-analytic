import time
from collections import deque

def limit_calls(max_calls=5, time_frame=60):
    call_times = deque()

    def clear_outdated_timestamps(curr_time):
        while call_times and call_times[0] < curr_time - time_frame:
            call_times.popleft()
    
    def decorator(func):
        def wrapper(*args, **kwargs):

            curr_time = time.time()
            clear_outdated_timestamps(curr_time)
            
            if len(call_times) >= max_calls:
                sleep_time = call_times[0] + time_frame - curr_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
                    curr_time = time.time()
                    clear_outdated_timestamps(curr_time)
            
            call_times.append(curr_time)
            
            return func(*args, **kwargs)
        return wrapper

    return decorator
