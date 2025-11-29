"""
=========================================================================
Locust Load Testing - GitHub Webhook Throughput
Sprint 17 - Performance Testing

Purpose:
- Load test GitHub webhook endpoint for throughput capacity
- Simulate high-volume webhook events (push, PR, issues)
- Measure webhook processing latency (target: <500ms p95)
- Validate webhook signature verification under load

Test Configuration:
- Users: 1000 (simulating 1000 concurrent webhooks)
- Spawn rate: 100 webhooks/second
- Duration: 10 minutes sustained load
- Host: http://localhost:8000

Test Scenarios (Real GitHub Webhook Traffic):
1. Push Events (60% of traffic):
   - Commits to branches
   - Tag pushes

2. Pull Request Events (25% of traffic):
   - PR opened
   - PR merged
   - PR closed

3. Issues Events (10% of traffic):
   - Issue opened
   - Issue closed
   - Issue commented

4. Branch Events (5% of traffic):
   - Branch created
   - Branch deleted

Performance Targets (SDLC 4.9):
- p50 latency: <100ms
- p95 latency: <500ms ⭐ CRITICAL
- p99 latency: <1000ms
- Error rate: <0.1%
- Throughput: >500 webhooks/s

OWASP ASVS Compliance:
- V11.1.4: Load testing validates webhook scalability
- V13.2.1: Webhook signature validation under load
=========================================================================
"""

import hashlib
import hmac
import json
import random
import time
import uuid
from typing import Dict

from locust import HttpUser, between, task


def generate_webhook_signature(payload: str, secret: str = "test_webhook_secret") -> str:
    """
    Generate GitHub webhook HMAC-SHA256 signature.

    Args:
        payload: JSON payload string
        secret: Webhook secret key

    Returns:
        Signature in format: sha256=<hex_digest>
    """
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


class GitHubWebhookUser(HttpUser):
    """
    Simulated GitHub sending webhook events.

    Behavior:
    - Send webhook events at high frequency
    - Include proper HMAC-SHA256 signature
    - Vary event types based on real distribution
    """

    # Wait time between webhooks (0.1-0.5 seconds for high throughput)
    wait_time = between(0.1, 0.5)

    # API endpoint
    webhook_endpoint = "/api/v1/github/webhook"

    # Webhook secret (must match backend config)
    webhook_secret = "test_webhook_secret"

    # Sample repository data
    sample_repos = [
        {"id": 123456789, "full_name": "testuser/project-alpha", "name": "project-alpha"},
        {"id": 234567890, "full_name": "testuser/project-beta", "name": "project-beta"},
        {"id": 345678901, "full_name": "org/enterprise-app", "name": "enterprise-app"},
        {"id": 456789012, "full_name": "company/internal-tool", "name": "internal-tool"},
        {"id": 567890123, "full_name": "team/shared-lib", "name": "shared-lib"},
    ]

    # Sample users
    sample_users = [
        {"id": 1001, "login": "developer1", "name": "Developer One"},
        {"id": 1002, "login": "developer2", "name": "Developer Two"},
        {"id": 1003, "login": "lead-dev", "name": "Lead Developer"},
        {"id": 1004, "login": "qa-engineer", "name": "QA Engineer"},
        {"id": 1005, "login": "devops", "name": "DevOps Engineer"},
    ]

    def send_webhook(self, event_type: str, payload: dict) -> None:
        """
        Send webhook with proper signature.

        Args:
            event_type: GitHub event type (push, pull_request, etc)
            payload: Webhook payload dict
        """
        payload_json = json.dumps(payload, separators=(',', ':'))
        signature = generate_webhook_signature(payload_json, self.webhook_secret)

        headers = {
            "Content-Type": "application/json",
            "X-GitHub-Event": event_type,
            "X-GitHub-Delivery": str(uuid.uuid4()),
            "X-Hub-Signature-256": signature,
            "User-Agent": "GitHub-Hookshot/test",
        }

        self.client.post(
            self.webhook_endpoint,
            data=payload_json,
            headers=headers,
            name=f"/webhook ({event_type})",
        )

    # ========================================================================
    # PUSH EVENTS (60% of traffic)
    # ========================================================================

    @task(60)
    def push_event(self):
        """
        Simulate push event (60% of traffic).

        GitHub sends push events for:
        - Commits to branches
        - Force pushes
        - Tag pushes
        """
        repo = random.choice(self.sample_repos)
        pusher = random.choice(self.sample_users)

        # Generate random commits
        num_commits = random.randint(1, 5)
        commits = []
        for i in range(num_commits):
            commits.append({
                "id": f"abc{random.randint(100000, 999999)}def{random.randint(100000, 999999)}",
                "message": random.choice([
                    "feat: Add new feature",
                    "fix: Fix bug in module",
                    "docs: Update README",
                    "refactor: Clean up code",
                    "test: Add unit tests",
                    "chore: Update dependencies",
                ]),
                "timestamp": "2025-11-28T00:00:00Z",
                "author": {
                    "name": pusher["name"],
                    "email": f"{pusher['login']}@example.com",
                    "username": pusher["login"],
                },
                "added": ["src/new_file.py"] if i == 0 else [],
                "removed": [],
                "modified": ["src/existing_file.py"],
            })

        payload = {
            "ref": f"refs/heads/{random.choice(['main', 'develop', 'feature/test'])}",
            "before": f"0000000{random.randint(100000, 999999)}",
            "after": commits[-1]["id"] if commits else f"1111111{random.randint(100000, 999999)}",
            "created": False,
            "deleted": False,
            "forced": False,
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": random.choice([True, False]),
                "default_branch": "main",
            },
            "pusher": {
                "name": pusher["login"],
                "email": f"{pusher['login']}@example.com",
            },
            "sender": {
                "login": pusher["login"],
                "id": pusher["id"],
                "type": "User",
            },
            "commits": commits,
            "head_commit": commits[-1] if commits else None,
        }

        self.send_webhook("push", payload)

    # ========================================================================
    # PULL REQUEST EVENTS (25% of traffic)
    # ========================================================================

    @task(25)
    def pull_request_event(self):
        """
        Simulate pull request event (25% of traffic).

        GitHub sends PR events for:
        - PR opened
        - PR closed (merged or not)
        - PR review requested
        - PR approved
        """
        repo = random.choice(self.sample_repos)
        user = random.choice(self.sample_users)

        action = random.choice(["opened", "closed", "synchronize", "review_requested"])
        pr_number = random.randint(1, 1000)

        payload = {
            "action": action,
            "number": pr_number,
            "pull_request": {
                "id": random.randint(100000, 999999),
                "number": pr_number,
                "state": "open" if action != "closed" else "closed",
                "locked": False,
                "title": random.choice([
                    "feat: Add new authentication",
                    "fix: Resolve database connection issue",
                    "docs: Update API documentation",
                    "refactor: Improve performance",
                ]),
                "body": "This PR adds important changes...",
                "user": {
                    "login": user["login"],
                    "id": user["id"],
                    "type": "User",
                },
                "created_at": "2025-11-27T00:00:00Z",
                "updated_at": "2025-11-28T00:00:00Z",
                "head": {
                    "label": f"{user['login']}:feature-branch",
                    "ref": "feature-branch",
                    "sha": f"abc{random.randint(100000, 999999)}",
                },
                "base": {
                    "label": f"{repo['full_name'].split('/')[0]}:main",
                    "ref": "main",
                    "sha": f"def{random.randint(100000, 999999)}",
                },
                "merged": action == "closed" and random.choice([True, False]),
                "mergeable": True,
                "comments": random.randint(0, 10),
                "commits": random.randint(1, 5),
                "additions": random.randint(10, 500),
                "deletions": random.randint(5, 100),
                "changed_files": random.randint(1, 20),
            },
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": random.choice([True, False]),
                "default_branch": "main",
            },
            "sender": {
                "login": user["login"],
                "id": user["id"],
                "type": "User",
            },
        }

        self.send_webhook("pull_request", payload)

    # ========================================================================
    # ISSUES EVENTS (10% of traffic)
    # ========================================================================

    @task(10)
    def issues_event(self):
        """
        Simulate issues event (10% of traffic).

        GitHub sends issues events for:
        - Issue opened
        - Issue closed
        - Issue labeled
        - Issue commented
        """
        repo = random.choice(self.sample_repos)
        user = random.choice(self.sample_users)

        action = random.choice(["opened", "closed", "labeled", "reopened"])
        issue_number = random.randint(1, 500)

        payload = {
            "action": action,
            "issue": {
                "id": random.randint(100000, 999999),
                "number": issue_number,
                "title": random.choice([
                    "Bug: Application crashes on startup",
                    "Feature request: Add dark mode",
                    "Question: How to configure OAuth?",
                    "Enhancement: Improve error messages",
                ]),
                "body": "Description of the issue...",
                "state": "open" if action != "closed" else "closed",
                "locked": False,
                "user": {
                    "login": user["login"],
                    "id": user["id"],
                    "type": "User",
                },
                "labels": [
                    {"id": 1, "name": "bug", "color": "d73a4a"},
                ],
                "created_at": "2025-11-27T00:00:00Z",
                "updated_at": "2025-11-28T00:00:00Z",
                "comments": random.randint(0, 20),
            },
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": random.choice([True, False]),
                "default_branch": "main",
            },
            "sender": {
                "login": user["login"],
                "id": user["id"],
                "type": "User",
            },
        }

        self.send_webhook("issues", payload)

    # ========================================================================
    # BRANCH EVENTS (5% of traffic)
    # ========================================================================

    @task(5)
    def branch_event(self):
        """
        Simulate create/delete event (5% of traffic).

        GitHub sends create/delete events for:
        - Branch creation
        - Branch deletion
        - Tag creation
        - Tag deletion
        """
        repo = random.choice(self.sample_repos)
        user = random.choice(self.sample_users)

        event_type = random.choice(["create", "delete"])
        ref_type = random.choice(["branch", "tag"])

        payload = {
            "ref": f"feature/{random.choice(['auth', 'api', 'ui', 'tests'])}-{random.randint(1, 100)}",
            "ref_type": ref_type,
            "master_branch": "main",
            "description": repo["name"],
            "pusher_type": "user",
            "repository": {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": random.choice([True, False]),
                "default_branch": "main",
            },
            "sender": {
                "login": user["login"],
                "id": user["id"],
                "type": "User",
            },
        }

        self.send_webhook(event_type, payload)


class WebhookBurstUser(HttpUser):
    """
    Simulated burst of webhooks (simulating CI/CD pipeline).

    Sends multiple webhooks in quick succession to test
    burst handling capacity.
    """

    wait_time = between(5, 10)  # Wait longer between bursts
    webhook_endpoint = "/api/v1/github/webhook"
    webhook_secret = "test_webhook_secret"
    weight = 1  # 10% of users are burst users

    @task
    def burst_push_events(self):
        """Send burst of 10 push events rapidly."""
        repo = {
            "id": random.randint(100000, 999999),
            "name": "burst-test-repo",
            "full_name": "testuser/burst-test-repo",
        }

        for i in range(10):
            payload = {
                "ref": "refs/heads/main",
                "before": f"before{i:06d}",
                "after": f"after{i:06d}",
                "repository": {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "default_branch": "main",
                },
                "pusher": {"name": "burst-tester", "email": "burst@test.com"},
                "sender": {"login": "burst-tester", "id": 9999, "type": "User"},
                "commits": [
                    {
                        "id": f"commit{i:06d}",
                        "message": f"Burst commit {i}",
                        "timestamp": "2025-11-28T00:00:00Z",
                        "added": [],
                        "removed": [],
                        "modified": ["file.py"],
                    }
                ],
            }

            payload_json = json.dumps(payload, separators=(',', ':'))
            signature = generate_webhook_signature(payload_json, self.webhook_secret)

            self.client.post(
                self.webhook_endpoint,
                data=payload_json,
                headers={
                    "Content-Type": "application/json",
                    "X-GitHub-Event": "push",
                    "X-GitHub-Delivery": str(uuid.uuid4()),
                    "X-Hub-Signature-256": signature,
                },
                name="/webhook (burst)",
            )


# ============================================================================
# LOAD TEST CONFIGURATION
# ============================================================================

"""
How to run GitHub webhook load test:

1. Start backend server:
   docker-compose up -d
   # OR
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

2. Set webhook secret in backend config:
   GITHUB_WEBHOOK_SECRET=test_webhook_secret

3. Run load test (Web UI):
   locust -f tests/load/github_webhook_load.py --host http://localhost:8000

   Then open: http://localhost:8089
   Configure:
   - Users: 1000
   - Spawn rate: 100
   - Host: http://localhost:8000

4. Run load test (Headless):
   locust -f tests/load/github_webhook_load.py \
     --host http://localhost:8000 \
     --users 1000 \
     --spawn-rate 100 \
     --run-time 10m \
     --headless \
     --csv=reports/webhook_load \
     --html=reports/webhook_load_report.html

5. Monitor results:
   - Real-time: http://localhost:8089
   - CSV: reports/webhook_load_stats.csv
   - HTML: reports/webhook_load_report.html

Performance Targets (SDLC 4.9):
✅ p50 latency: <100ms
✅ p95 latency: <500ms ⭐ CRITICAL
✅ p99 latency: <1000ms
✅ Error rate: <0.1%
✅ Throughput: >500 webhooks/s

Expected Results:
- 1000 users * 2-10 req/s = 2000-10000 webhooks/second peak
- Actual throughput depends on:
  - Database write speed (job queue)
  - Signature verification overhead
  - Background job processing capacity
"""
