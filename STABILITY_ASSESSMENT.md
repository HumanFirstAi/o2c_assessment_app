# Stability Assessment: O2C Assessment App
**Date:** 2026-01-15
**Assessment for:** 10 concurrent users
**Current Status:** ⚠️ **NOT PRODUCTION-READY** - Critical issues identified

---

## Executive Summary

**Current State:** The application will work for 1-3 concurrent users but has **3 CRITICAL issues** that will cause failures with 10 concurrent users.

**Risk Level:** 🔴 **HIGH RISK**

**Estimated Time to Production-Ready:** 4-8 hours of focused development

---

## Critical Issues (Must Fix Before Production)

### 🔴 CRITICAL #1: API Rate Limiting
**File:** `modules/concurrent_generator.py:94`
**Impact:** Will fail at ~10 concurrent users

**Problem:**
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # Each user generates report with 3 workers
    # 10 users × 3 workers = 30 concurrent Claude API calls
```

**What happens:**
- Anthropic API rate limit: typically 100-1000 requests/minute
- With 10 concurrent users generating reports: 30+ simultaneous API calls
- **Result:** API returns 429 errors, users get degraded/failed reports

**Fix Required:**
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def synthesize_with_claude(section_type, context, valid_agents):
    # ... existing code
```

**Priority:** IMMEDIATE - Add before deploying to 10 users

---

### 🔴 CRITICAL #2: File System Race Conditions
**File:** `modules/storage.py:27`
**Impact:** Data loss, corrupted assessments

**Problem:**
```python
def save_assessment(user: dict, scores: dict, report: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    assessment_id = f"{timestamp}_{user['session_id']}"
    # If 2 requests happen in same second → same assessment_id → one overwrites other
```

**What happens:**
- Two rapid report generations by same user
- Both get identical timestamp (same second)
- Second write overwrites first → data loss
- Also: No file locking → partial writes possible

**Fix Required:**
```python
import uuid

def save_assessment(user: dict, scores: dict, report: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    assessment_id = f"{timestamp}_{unique_id}"

    # Add atomic writes with temp file + rename
    temp_file = scores_file.with_suffix('.tmp')
    with open(temp_file, "w") as f:
        json.dump(scores_data, f, indent=2)
    temp_file.rename(scores_file)  # Atomic operation
```

**Priority:** IMMEDIATE - Data loss is unacceptable

---

### 🔴 CRITICAL #3: Session File Corruption
**File:** `modules/session_manager.py:47-50`
**Impact:** Users randomly logged out, session data corrupted

**Problem:**
```python
def load_session(token: str) -> Optional[dict]:
    if not session_file.exists():  # Check
        return None
    with open(session_file) as f:  # File could be deleted here by another thread
        session_data = json.load(f)
    # TOCTOU (Time-Of-Check-Time-Of-Use) vulnerability
```

**What happens:**
- User A loads session (checks file exists)
- User B's expired session cleanup deletes different session
- Due to race condition, could delete User A's file
- User A reads non-existent/corrupted file → crashes

**Fix Required:**
```python
import fcntl  # Unix file locking

def load_session(token: str) -> Optional[dict]:
    session_file = SESSION_DIR / f"{token}.json"
    if not session_file.exists():
        return None

    try:
        with open(session_file, "r") as f:
            fcntl.flock(f, fcntl.LOCK_SH)  # Shared read lock
            session_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    # ... rest of logic
```

**Priority:** HIGH - Will cause user frustration and data loss

---

## High Priority Issues (Should Fix Soon)

### 🟠 HIGH #1: Activity Log Corruption
**File:** `modules/auth.py:176`
**Impact:** Audit logs become unreadable

**Problem:**
- Multiple users append to same log file without locking
- Lines interleave → corrupted JSONL

**Fix:** Use Python's `logging` module with `RotatingFileHandler`

---

### 🟠 HIGH #2: No API Retry Logic
**File:** `modules/concurrent_generator.py:128`
**Impact:** Transient API failures result in degraded reports

**Problem:**
```python
except Exception as e:
    print(f"Synthesis error: {e}")  # Silent failure!
```

**Fix:** Add retry with exponential backoff using `tenacity` library

---

### 🟠 HIGH #3: Resource Cleanup Missing
**Files:** Multiple
**Impact:** Memory leaks, file handle exhaustion

**Problem:**
- Uploaded images not deleted after processing
- Session files accumulate (never cleaned beyond 7-day check)
- No cleanup of old assessment files

**Fix:** Add cleanup tasks in background

---

## Medium Priority Issues

### 🟡 MEDIUM #1: No Connection Pooling
**Impact:** Slower API calls, potential connection exhaustion

**Fix:** Reuse single Anthropic client instance globally

---

### 🟡 MEDIUM #2: Cached Knowledge Base
**File:** `app.py:212`
**Impact:** If KB updated, users see stale data until restart

**Fix:** Add TTL to `@st.cache_data(ttl=3600)` or manual cache invalidation

---

### 🟡 MEDIUM #3: TOCTOU in Multiple Functions
**Impact:** Edge case failures under high load

**Files:** `storage.py:76`, `session_manager.py:47`

---

## Load Testing Results Prediction

### Scenario: 10 Users Generate Reports Simultaneously

| Metric | Predicted Result | Acceptable? |
|--------|-----------------|-------------|
| **API Calls** | 30 concurrent (10×3 workers) | ❌ Exceeds rate limit |
| **Response Time** | 30-90 seconds (with retries) | ⚠️ Slow but acceptable |
| **Success Rate** | ~60-70% (429 errors) | ❌ Too low |
| **Data Corruption** | 1-2 assessments | ❌ Unacceptable |
| **Memory Usage** | ~500MB-1GB | ✅ OK |
| **CPU Usage** | ~40-60% | ✅ OK |

**Verdict:** Application will experience failures and data loss

---

## Production Readiness Checklist

### Must Have (Before 10 Users)
- [ ] **API rate limiting** - Add rate limiter to Claude API calls
- [ ] **Atomic file operations** - UUID + temp file writes
- [ ] **File locking** - Add fcntl/msvcrt locks to storage operations
- [ ] **Error visibility** - Show API errors to users instead of silent fallback
- [ ] **Retry logic** - Exponential backoff for transient failures

### Should Have (Within 1 Week)
- [ ] **Logging infrastructure** - Replace append-to-file with proper logging
- [ ] **Connection pooling** - Reuse Anthropic client
- [ ] **Resource cleanup** - Background task to delete old files
- [ ] **Monitoring** - Track API call counts, error rates, response times
- [ ] **Circuit breaker** - Fail fast if API consistently down

### Nice to Have (Future)
- [ ] **Database migration** - Replace file storage with SQLite/PostgreSQL
- [ ] **Redis sessions** - Distributed session management
- [ ] **Background workers** - Async report generation with Celery/RQ
- [ ] **Load balancer** - Multiple Streamlit instances (requires DB first)

---

## Recommended Action Plan

### Phase 1: Critical Fixes (4 hours)
1. **Add UUID to assessment IDs** (30 min)
   - Edit `modules/storage.py:27`
   - Test: Generate 2 reports within same second

2. **Implement API rate limiting** (2 hours)
   - Add `ratelimit` to `requirements.txt`
   - Wrap `synthesize_with_claude()` function
   - Test: Simulate 10 concurrent report generations

3. **Add file locking** (1.5 hours)
   - Add locks to `save_assessment()`, `load_session()`
   - Test: Concurrent saves for same user

### Phase 2: High Priority (4 hours)
4. **Fix logging** (1 hour)
   - Replace custom logging with Python `logging` module

5. **Add retry logic** (2 hours)
   - Install `tenacity`
   - Add retry decorators with exponential backoff

6. **Resource cleanup** (1 hour)
   - Add cleanup for temp files
   - Scheduled session cleanup task

### Phase 3: Monitoring (2 hours)
7. **Add observability** (2 hours)
   - Log API call counts
   - Track error rates
   - Monitor file system usage

**Total Estimated Time:** 10 hours to production-ready state

---

## Deployment Configuration

### Current Railway Setup (Single Instance)
✅ **OK for 10 users** with fixes applied

**Requirements:**
- 1 Streamlit process (NOT multiple replicas - file system not coordinated)
- Persistent volume at `/data` (already configured)
- Environment: `PORT=8501`, `ANTHROPIC_API_KEY=xxx`

**Resource Limits:**
- CPU: 0.5-1 vCPU (sufficient)
- Memory: 512MB-1GB (sufficient)
- Storage: 10GB (more than enough for 100+ assessments)

### If Scaling Beyond 10 Users (Future)
⚠️ **Requires architectural changes:**
1. Migrate to PostgreSQL/SQLite database
2. Use Redis for sessions
3. Enable multiple Streamlit replicas
4. Add load balancer

---

## Risk Mitigation

### During Critical Fix Implementation

**Backup Strategy:**
```bash
# Before deploying fixes, backup user data
tar -czf user_data_backup_$(date +%Y%m%d).tar.gz /data/user_data/
```

**Staged Rollout:**
1. Test fixes locally with 10 simulated users
2. Deploy to staging environment (Railway preview)
3. Run load test: `locust -f load_test.py --users 10`
4. Monitor for 1 hour before full production deploy

**Rollback Plan:**
- Keep previous git commit tagged
- Railway allows instant rollback to previous deployment

---

## Conclusion

**Current Assessment:** 🔴 **NOT READY for 10 concurrent users**

**With Critical Fixes:** 🟢 **READY for 10-15 concurrent users**

**Estimated Development Time:** 4 hours (critical only) to 10 hours (all high priority)

**Recommendation:**
1. **Implement Critical Fixes #1-3 immediately** (4 hours)
2. **Load test with 10 simulated users** (1 hour)
3. **Deploy and monitor closely** for first week
4. **Implement High Priority fixes** during first week of operation

---

## Testing Script

Create `load_test.py` to verify fixes:

```python
# Load test simulation
import concurrent.futures
import requests
import time

def simulate_user(user_id):
    """Simulate a user generating a report"""
    start = time.time()
    # ... API calls to generate report
    duration = time.time() - start
    return user_id, duration

# Test with 10 concurrent users
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(simulate_user, i) for i in range(10)]
    results = [f.result() for f in futures]

print(f"Success rate: {len([r for r in results if r])/10*100}%")
```

---

**Next Steps:** Apply critical fixes in order of priority, test thoroughly, then deploy.
