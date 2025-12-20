#!/bin/bash
# Test script for bulk delete fix
# CTO Debug Script - SDLC 5.1.1

echo "=== Testing Bulk Delete Fix ==="
echo ""

# Check backend status
echo "1. Checking backend container status..."
docker ps | grep sdlc-backend
echo ""

# Check if backend is healthy
echo "2. Waiting for backend to be healthy..."
sleep 5
docker compose ps backend
echo ""

# Test the endpoint with curl
echo "3. Testing bulk delete endpoint with curl..."
echo "(This will fail with 401 if no auth token, but should NOT give 422 for valid JSON)"
echo ""

# Create a test request
cat > /tmp/test-bulk-delete.json <<EOF
{
  "user_ids": ["550e8400-e29b-41d4-a716-446655440000"]
}
EOF

echo "Test payload:"
cat /tmp/test-bulk-delete.json
echo ""
echo ""

echo "Making test request..."
curl -X DELETE \
  https://sdlc.nhatquangholding.com/api/v1/admin/users/bulk \
  -H "Content-Type: application/json" \
  -d @/tmp/test-bulk-delete.json \
  -v 2>&1 | grep -E "HTTP|Content-Type|422|401|403"

echo ""
echo ""
echo "4. Checking backend logs for our debug messages..."
docker compose logs backend --tail=50 | grep -E "BULK DELETE|Bulk delete|Validation error"

echo ""
echo "=== Test Complete ==="
echo ""
echo "Expected results:"
echo "- If you see '=== BULK DELETE ENDPOINT CALLED ===' in logs: ✅ Endpoint is being reached"
echo "- If you see 'Validation error' in logs: ✅ We can see the actual validation error"
echo "- If you see HTTP 401/403: ✅ Expected (need valid auth token)"
echo "- If you see HTTP 422 but NO logs: ❌ Request not reaching our code"
echo ""
echo "Next step: Test from browser with valid session!"
