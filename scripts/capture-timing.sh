#!/bin/bash
# SASE Week 6 - Timing Capture Script (3 runs for p95 calculation)
# Usage: ./capture-timing.sh

set -e

ENDPOINT="http://localhost:8300/api/v1/sop/generate"
OUTPUT_DIR="/tmp/sase-week6-timing-evidence"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo "=== SASE Week 6 - Timing Capture (3 Runs) ==="
echo "Timestamp: $(date)"
echo "Endpoint: $ENDPOINT"
echo ""

# Payload
PAYLOAD='{
  "sop_type": "deployment",
  "workflow_description": "Deploy FastAPI application to Kubernetes cluster with zero-downtime. Include health checks, database migrations, and rollback procedure if deployment fails."
}'

# Run 3 times and capture metrics
for i in {1..3}; do
  echo "--- Run $i/3 ---"
  
  START=$(date +%s%3N)
  RESPONSE=$(curl -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    --silent \
    --write-out "\n%{http_code}" \
    --max-time 35)
  END=$(date +%s%3N)
  
  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')
  
  WALL_TIME=$((END - START))
  
  # Extract from response
  SOP_ID=$(echo "$BODY" | jq -r .sop_id)
  GEN_TIME=$(echo "$BODY" | jq -r .generation_time_ms)
  SECTIONS=$(echo "$BODY" | jq -r '[.purpose, .scope, .procedure, .roles, .quality_criteria] | map(if length > 0 then 1 else 0 end) | add')
  
  echo "  HTTP Code: $HTTP_CODE"
  echo "  SOP ID: $SOP_ID"
  echo "  Generation Time (API): ${GEN_TIME}ms ($(echo "scale=2; $GEN_TIME / 1000" | bc)s)"
  echo "  Wall Clock Time: ${WALL_TIME}ms ($(echo "scale=2; $WALL_TIME / 1000" | bc)s)"
  echo "  Sections Present: $SECTIONS/5"
  echo ""
  
  # Save full response
  echo "$BODY" | jq . > "$OUTPUT_DIR/run${i}-${TIMESTAMP}.json"
  
  # Append to summary CSV
  echo "$i,$HTTP_CODE,$SOP_ID,$GEN_TIME,$WALL_TIME,$SECTIONS" >> "$OUTPUT_DIR/timing-summary-${TIMESTAMP}.csv"
  
  sleep 2
done

# Calculate p95 (for 3 runs, p95 = max)
echo "=== Summary ==="
echo ""
cat "$OUTPUT_DIR/timing-summary-${TIMESTAMP}.csv" | while IFS=, read run http_code sop_id gen_time wall_time sections; do
  echo "Run $run: ${gen_time}ms (wall: ${wall_time}ms) | Sections: $sections/5 | HTTP: $http_code"
done

echo ""
GEN_TIMES=$(cat "$OUTPUT_DIR/timing-summary-${TIMESTAMP}.csv" | cut -d',' -f4 | sort -n)
P95=$(echo "$GEN_TIMES" | tail -1)
AVG=$(echo "$GEN_TIMES" | awk '{sum+=$1} END {print sum/NR}')

echo "--- Timing Statistics ---"
echo "Average Generation Time: $(echo "scale=2; $AVG / 1000" | bc)s"
echo "p95 Generation Time: $(echo "scale=2; $P95 / 1000" | bc)s"
echo "Target: <30s"
echo "Status: $([ $(echo "$P95 < 30000" | bc) -eq 1 ] && echo "✅ PASS" || echo "❌ FAIL")"

echo ""
echo "Evidence saved to: $OUTPUT_DIR"
echo "Summary CSV: $OUTPUT_DIR/timing-summary-${TIMESTAMP}.csv"
echo "Individual runs: $OUTPUT_DIR/run{1,2,3}-${TIMESTAMP}.json"
