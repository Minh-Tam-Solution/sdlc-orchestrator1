#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing Script
Tests all 636+ API endpoints from API-ENDPOINTS-COMPACT.md
Generates detailed report with full requests/responses and root cause analysis
"""

import re
import json
import time
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict

# Configuration
BASE_URL = "http://localhost:8300"
API_ENDPOINTS_FILE = "/Users/anhnlq/Documents/GitHub/SDLC-Orchestrator/docs/backend/API-ENDPOINTS-COMPACT.md"
OUTPUT_REPORT = "/Users/anhnlq/Documents/GitHub/SDLC-Orchestrator/docs/backend/API-ENDPOINTS.md"

# Test credentials
TEST_USER = {
    "username": "api_tester",
    "email": "api.tester@sdlc.local",
    "password": "SecureTestPassword123!@#"
}

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.results = []
        self.stats = {
            "total": 0,
            "success": 0,
            "auth_required": 0,
            "client_error": 0,
            "server_error": 0,
            "not_found": 0
        }

    def parse_endpoints_file(self, file_path: str) -> List[Dict]:
        """Parse API-ENDPOINTS-COMPACT.md to extract unique endpoints"""
        endpoints = []
        seen = set()

        with open(file_path, 'r') as f:
            content = f.read()

        # Extract endpoints from markdown table
        # Format: | 🔵 GET | `/api/v1/path` | Summary |
        pattern = r'\|\s*[🔵🟢🟡🟠🔴]\s*(\w+)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|'

        for match in re.finditer(pattern, content):
            method, path, summary = match.groups()
            method = method.strip()
            path = path.strip()
            summary = summary.strip()

            # Create unique key
            key = f"{method}:{path}"
            if key not in seen:
                seen.add(key)
                endpoints.append({
                    "method": method,
                    "path": path,
                    "summary": summary
                })

        print(f"✅ Parsed {len(endpoints)} unique endpoints")
        return endpoints

    def register_test_user(self) -> bool:
        """Register a test user for authentication"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/register",
                json=TEST_USER,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 201]:
                print("✅ Test user registered successfully")
                return True
            elif response.status_code == 400 and "already exists" in response.text.lower():
                print("✅ Test user already exists")
                return True
            else:
                print(f"⚠️ Registration failed: {response.status_code} - {response.text[:100]}")
                return True  # Continue anyway, user might exist

        except Exception as e:
            print(f"⚠️ Registration error: {str(e)}")
            return True  # Continue anyway

    def login_test_user(self) -> bool:
        """Login and get JWT token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                json={
                    "username": TEST_USER["username"],
                    "password": TEST_USER["password"]
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token") or data.get("token")
                print(f"✅ Login successful, token obtained")
                return True
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text[:100]}")
                return False

        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False

    def prepare_request_data(self, method: str, path: str) -> Dict:
        """Prepare sample request data based on endpoint"""
        data = {}

        # POST/PUT/PATCH endpoints need body
        if method in ["POST", "PUT", "PATCH"]:
            # Authentication endpoints
            if "/auth/login" in path:
                data = {"username": "test", "password": "test"}
            elif "/auth/register" in path:
                data = {"username": "test2", "email": "test2@test.com", "password": "Test123!"}
            elif "/auth/refresh" in path:
                data = {"refresh_token": "dummy_token"}

            # Gate endpoints
            elif "/gates" in path and method == "POST":
                data = {
                    "project_id": 1,
                    "gate_type": "G1_CONSULTATION",
                    "name": "Test Gate",
                    "description": "Test gate for API testing"
                }
            elif "/gates" in path and "evaluate" in path:
                data = {"force": False}

            # Project endpoints
            elif "/projects" in path and method == "POST":
                data = {
                    "name": "Test Project",
                    "description": "Test project for API testing",
                    "repository_url": "https://github.com/test/test"
                }

            # Evidence endpoints
            elif "/evidence" in path:
                data = {
                    "gate_id": 1,
                    "type": "TEST_RESULTS",
                    "description": "Test evidence"
                }

            # Agent team endpoints
            elif "/agent-team/definitions" in path:
                data = {
                    "name": "Test Agent",
                    "role": "DEVELOPER",
                    "system_prompt": "Test agent",
                    "provider": "ollama"
                }
            elif "/agent-team/conversations" in path:
                data = {
                    "agent_id": 1,
                    "project_id": 1,
                    "initial_message": "Test message"
                }

            # Generic fallback
            else:
                data = {"test": "data"}

        return data

    def replace_path_params(self, path: str) -> str:
        """Replace path parameters with test values"""
        replacements = {
            "{id}": "1",
            "{gate_id}": "1",
            "{project_id}": "1",
            "{user_id}": "1",
            "{definition_id}": "1",
            "{conversation_id}": "1",
            "{session_id}": "1",
            "{provider}": "ollama",
            "{breaker_name}": "test",
            "{key}": "test_key",
            "{scan_id}": "1",
            "{roadmap_id}": "1",
            "{phase_id}": "1",
            "{sprint_id}": "1",
            "{item_id}": "1",
            "{message_id}": "1"
        }

        for param, value in replacements.items():
            path = path.replace(param, value)

        return path

    def test_endpoint(self, endpoint: Dict) -> Dict:
        """Test a single endpoint and return result"""
        method = endpoint["method"]
        path = endpoint["path"]
        summary = endpoint["summary"]

        # Replace path parameters
        test_path = self.replace_path_params(path)
        url = f"{self.base_url}{test_path}"

        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Prepare request data
        data = self.prepare_request_data(method, path)

        # Make request
        try:
            start_time = time.time()

            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                response = None

            elapsed_time = time.time() - start_time

            if response is None:
                return self.create_result(endpoint, "SKIP", "Unsupported HTTP method", "", "", 0)

            # Analyze response
            status_code = response.status_code
            status_category = self.categorize_status(status_code)

            # Try to parse JSON response
            try:
                response_body = json.dumps(response.json(), indent=2)
            except:
                response_body = response.text[:500]  # Limit text response

            # Build request details
            request_details = {
                "method": method,
                "url": url,
                "headers": {k: v for k, v in headers.items() if k != "Authorization"},
                "body": data if data else None
            }
            request_str = json.dumps(request_details, indent=2)

            # Root cause analysis
            root_cause = self.analyze_root_cause(status_code, response, path, method)

            return self.create_result(
                endpoint,
                status_category,
                root_cause,
                request_str,
                response_body,
                elapsed_time
            )

        except requests.exceptions.Timeout:
            return self.create_result(endpoint, "TIMEOUT", "Request timeout after 10s", "", "", 10.0)
        except requests.exceptions.ConnectionError:
            return self.create_result(endpoint, "ERROR", "Connection refused - service may be down", "", "", 0)
        except Exception as e:
            return self.create_result(endpoint, "ERROR", f"Exception: {str(e)}", "", "", 0)

    def categorize_status(self, status_code: int) -> str:
        """Categorize HTTP status code"""
        if 200 <= status_code < 300:
            return "SUCCESS"
        elif status_code == 401:
            return "AUTH_REQUIRED"
        elif status_code == 403:
            return "FORBIDDEN"
        elif status_code == 404:
            return "NOT_FOUND"
        elif 400 <= status_code < 500:
            return "CLIENT_ERROR"
        elif 500 <= status_code < 600:
            return "SERVER_ERROR"
        else:
            return "UNKNOWN"

    def analyze_root_cause(self, status_code: int, response, path: str, method: str) -> str:
        """Analyze root cause of response status"""
        try:
            body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        except:
            body = {}

        detail = body.get("detail", "")

        # Success cases
        if 200 <= status_code < 300:
            return f"✅ Success - {status_code}"

        # Authentication
        if status_code == 401:
            if "credentials" in str(detail).lower():
                return "🔒 Invalid or missing authentication token (JWT required)"
            return "🔒 Authentication required - endpoint needs valid JWT token"

        # Forbidden
        if status_code == 403:
            if "permission" in str(detail).lower() or "forbidden" in str(detail).lower():
                return "🚫 Insufficient permissions - user role lacks required access"
            return "🚫 Access forbidden - check user permissions and roles"

        # Not Found
        if status_code == 404:
            if method in ["GET", "PUT", "PATCH", "DELETE"] and any(p in path for p in ["{id}", "{gate_id}", "{project_id}"]):
                return "❌ Resource not found - ID may not exist in database (test data needed)"
            return f"❌ Endpoint not found - {path} may not be implemented"

        # Validation errors
        if status_code == 422:
            return f"⚠️ Validation error - {detail}"

        # Bad request
        if status_code == 400:
            return f"⚠️ Bad request - {detail}"

        # Server errors
        if 500 <= status_code < 600:
            return f"🔥 Server error - {status_code}: {detail}"

        return f"Status {status_code}: {detail}"

    def create_result(self, endpoint: Dict, status: str, root_cause: str,
                     request: str, response: str, elapsed_time: float) -> Dict:
        """Create result dictionary"""
        return {
            "method": endpoint["method"],
            "path": endpoint["path"],
            "summary": endpoint["summary"],
            "status": status,
            "root_cause": root_cause,
            "request": request,
            "response": response,
            "elapsed_ms": int(elapsed_time * 1000)
        }

    def update_stats(self, status: str):
        """Update statistics"""
        self.stats["total"] += 1

        if status == "SUCCESS":
            self.stats["success"] += 1
        elif status == "AUTH_REQUIRED":
            self.stats["auth_required"] += 1
        elif status == "NOT_FOUND":
            self.stats["not_found"] += 1
        elif status in ["CLIENT_ERROR", "FORBIDDEN"]:
            self.stats["client_error"] += 1
        elif status == "SERVER_ERROR":
            self.stats["server_error"] += 1

    def generate_report(self, results: List[Dict]):
        """Generate comprehensive markdown report"""
        with open(OUTPUT_REPORT, 'w') as f:
            # Header
            f.write("# API Endpoints Testing Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Base URL**: {self.base_url}\n")
            f.write(f"**Total Endpoints Tested**: {self.stats['total']}\n\n")

            f.write("---\n\n")

            # Statistics
            f.write("## 📊 Test Statistics\n\n")
            f.write("| Metric | Count | Percentage |\n")
            f.write("|--------|-------|------------|\n")
            f.write(f"| **Total Tested** | {self.stats['total']} | 100% |\n")
            f.write(f"| ✅ Success (2xx) | {self.stats['success']} | {self.stats['success']/self.stats['total']*100:.1f}% |\n")
            f.write(f"| 🔒 Auth Required (401) | {self.stats['auth_required']} | {self.stats['auth_required']/self.stats['total']*100:.1f}% |\n")
            f.write(f"| ❌ Not Found (404) | {self.stats['not_found']} | {self.stats['not_found']/self.stats['total']*100:.1f}% |\n")
            f.write(f"| ⚠️ Client Error (4xx) | {self.stats['client_error']} | {self.stats['client_error']/self.stats['total']*100:.1f}% |\n")
            f.write(f"| 🔥 Server Error (5xx) | {self.stats['server_error']} | {self.stats['server_error']/self.stats['total']*100:.1f}% |\n")
            f.write("\n---\n\n")

            # Detailed Results Table
            f.write("## 📋 Detailed Test Results\n\n")
            f.write("| # | Service | Method | Endpoint | Status | Root Cause |\n")
            f.write("|---|---------|--------|----------|--------|------------|\n")

            for idx, result in enumerate(results, 1):
                # Extract service from endpoint path
                service = self.extract_service(result["path"])

                f.write(f"| {idx} | {service} | {result['method']} | `{result['path']}` | {result['status']} | {result['root_cause']} |\n")

            f.write("\n---\n\n")

            # Full Request/Response Details (grouped by status)
            f.write("## 🔍 Full Request/Response Details\n\n")

            # Group by status
            by_status = defaultdict(list)
            for result in results:
                by_status[result["status"]].append(result)

            for status in ["SUCCESS", "AUTH_REQUIRED", "NOT_FOUND", "CLIENT_ERROR", "SERVER_ERROR", "ERROR"]:
                if status not in by_status:
                    continue

                status_results = by_status[status]
                f.write(f"### {status} ({len(status_results)} endpoints)\n\n")

                for result in status_results[:50]:  # Limit to first 50 per status to avoid huge file
                    f.write(f"#### {result['method']} {result['path']}\n\n")
                    f.write(f"**Summary**: {result['summary']}\n\n")
                    f.write(f"**Status**: {result['status']}\n\n")
                    f.write(f"**Root Cause**: {result['root_cause']}\n\n")
                    f.write(f"**Latency**: {result['elapsed_ms']}ms\n\n")

                    if result['request']:
                        f.write("**Request**:\n```json\n")
                        f.write(result['request'])
                        f.write("\n```\n\n")

                    if result['response']:
                        f.write("**Response**:\n```json\n")
                        f.write(result['response'][:1000])  # Limit response size
                        if len(result['response']) > 1000:
                            f.write("\n... (truncated)")
                        f.write("\n```\n\n")

                    f.write("---\n\n")

                if len(status_results) > 50:
                    f.write(f"*... and {len(status_results) - 50} more endpoints with {status} status*\n\n")

            # Recommendations
            f.write("## 💡 Recommendations\n\n")

            if self.stats["auth_required"] > 0:
                f.write(f"1. **Authentication**: {self.stats['auth_required']} endpoints require authentication. Create test users and obtain JWT tokens.\n")

            if self.stats["not_found"] > 0:
                f.write(f"2. **Missing Resources**: {self.stats['not_found']} endpoints returned 404. Seed test data (projects, gates, evidence) to test fully.\n")

            if self.stats["server_error"] > 0:
                f.write(f"3. **Server Errors**: {self.stats['server_error']} endpoints have server errors. Check backend logs for details.\n")

            f.write("\n---\n\n")
            f.write(f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Testing Tool**: SDLC Orchestrator API Tester\n")

    def extract_service(self, path: str) -> str:
        """Extract service name from path"""
        parts = path.strip('/').split('/')
        if len(parts) >= 3:
            return parts[2]  # /api/v1/SERVICE
        return "unknown"

    def run(self):
        """Main execution"""
        print("🚀 SDLC Orchestrator API Testing Tool\n")

        # Step 1: Parse endpoints
        print("📖 Step 1: Parsing endpoints from API-ENDPOINTS-COMPACT.md...")
        endpoints = self.parse_endpoints_file(API_ENDPOINTS_FILE)
        print(f"   Found {len(endpoints)} unique endpoints\n")

        # Step 2: Setup authentication
        print("🔐 Step 2: Setting up test user and authentication...")
        self.register_test_user()
        auth_success = self.login_test_user()
        print()

        if not auth_success:
            print("⚠️ Authentication failed, continuing with unauthenticated requests...\n")

        # Step 3: Test all endpoints
        print(f"🧪 Step 3: Testing {len(endpoints)} endpoints...")
        print("   This may take several minutes...\n")

        for idx, endpoint in enumerate(endpoints, 1):
            if idx % 50 == 0:
                print(f"   Progress: {idx}/{len(endpoints)} ({idx/len(endpoints)*100:.1f}%)")

            result = self.test_endpoint(endpoint)
            self.results.append(result)
            self.update_stats(result["status"])

            # Small delay to avoid overwhelming the server
            time.sleep(0.05)

        print(f"\n✅ Testing complete: {len(self.results)} endpoints tested\n")

        # Step 4: Generate report
        print("📝 Step 4: Generating detailed report...")
        self.generate_report(self.results)
        print(f"   Report saved to: {OUTPUT_REPORT}\n")

        # Step 5: Print summary
        print("=" * 60)
        print("📊 TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Endpoints:    {self.stats['total']}")
        print(f"✅ Success:         {self.stats['success']} ({self.stats['success']/self.stats['total']*100:.1f}%)")
        print(f"🔒 Auth Required:   {self.stats['auth_required']} ({self.stats['auth_required']/self.stats['total']*100:.1f}%)")
        print(f"❌ Not Found:       {self.stats['not_found']} ({self.stats['not_found']/self.stats['total']*100:.1f}%)")
        print(f"⚠️  Client Errors:   {self.stats['client_error']} ({self.stats['client_error']/self.stats['total']*100:.1f}%)")
        print(f"🔥 Server Errors:   {self.stats['server_error']} ({self.stats['server_error']/self.stats['total']*100:.1f}%)")
        print("=" * 60)
        print(f"\n📄 Full report: {OUTPUT_REPORT}")
        print("\n🎉 Testing complete!")

if __name__ == "__main__":
    tester = APITester()
    tester.run()
