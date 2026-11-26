import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request

def rate_limit(max_calls, seconds):
    hits= defaultdict(deque)
    def check(request: Request):
        visitor = request. client.host if request.client else "unknown"
        now= time.monotonic()
        recent = hits[visitor]
        while recent and now -recent[0]>seconds:
            recent.popleft()
        if len(recent)>=max_calls:
            wait= int(seconds- (now-recent[0])) +1
            raise HTTPException(429, "too many attempts. please wait and try again", headers={"Retry-After": str(wait)})
        recent.append(now)
    return check