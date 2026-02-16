# Sprint 174 Quick Reference — Engineering Team

**Sprint**: Feb 17-28, 2026 (10 days)  
**Focus**: Anthropic Best Practices (Prompt Caching + MCP Positioning)  
**Team**: Backend (7d), DevOps (2d), Marketing (3d), CTO (1d)

---

## 🎯 Sprint Goal (2-sentence version)

Implement Anthropic's prompt caching pattern to reduce EP-06 codegen costs by 8x ($14K/year savings). Clarify market positioning: we orchestrate ALL AI coders (MCP control plane), not compete with them.

---

## 📊 Key Metrics

| Metric | Target | How to Check |
|--------|--------|--------------|
| Cache hit rate | >85% | `curl localhost:9090/metrics \| grep cache_hit_rate` |
| Cost per codegen | <$0.002 | Grafana → "Codegen Cost" panel |
| Latency reduction | -200ms | Prometheus → `codegen_duration_seconds{cached="true"}` |

---

## 🏗️ Implementation Checklist

### Days 1-2: Design & Setup
- [ ] Review Anthropic cache_control API docs
- [ ] Design cache schema (Redis keys/TTL)
- [ ] Identify cacheable sections (960KB → chunked)
- [ ] Write design doc (share in #eng-backend)

### Days 3-4: Core Implementation
- [ ] Create `SDLCContextCache` service
- [ ] Add cache_control markers to prompts
- [ ] Integrate with `CodegenService.generate_code()`
- [ ] Unit tests (cache hit/miss scenarios)

### Day 5: Integration & Testing
- [ ] Deploy to staging
- [ ] Load test: 1000 codegen requests
- [ ] Verify >85% cache hit rate
- [ ] Validate cost reduction (check Anthropic dashboard)

### Days 6-7: Monitoring
- [ ] Create Grafana dashboard
  - Panel 1: Cost per request (before/after)
  - Panel 2: Cache hit rate over time
  - Panel 3: Monthly savings estimate
- [ ] Set up alerts (cache hit <70% → #eng-alerts)
- [ ] Document runbook (`docs/07-operate/runbooks/cache-invalidation.md`)

### Days 8-10: Documentation & Training
- [ ] Write MCP positioning doc (technical)
- [ ] Update sales deck (MCP diagram)
- [ ] Write blog post draft
- [ ] All-hands presentation (Day 10)

---

## 🔧 Code Templates

### 1. Cache Service Interface

```python
# backend/app/services/context_cache_service.py
from typing import Optional
from datetime import timedelta
import redis.asyncio as redis

class SDLCContextCache:
    """
    Prompt caching for SDLC Framework context.
    
    Usage:
        cache = SDLCContextCache()
        prompt = await cache.get_cached_prompt()
        # Uses Anthropic's cache_control API
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.ttl = timedelta(hours=24)
    
    async def get_cached_prompt(self) -> str:
        """
        Returns prompt with cache_control markers.
        
        Structure:
        [
          {"type": "text", "text": "SDLC Framework...", "cache_control": {"type": "ephemeral"}},
          {"type": "text", "text": "ADRs...", "cache_control": {"type": "ephemeral"}},
          {"type": "text", "text": "Templates...", "cache_control": {"type": "ephemeral"}},
          {"type": "text", "text": "User query: {query}"}
        ]
        """
        # Check Redis first
        cached = await self.redis.get("sdlc:framework:context:v1")
        if cached:
            return cached.decode()
        
        # Build prompt with cache markers
        prompt = self._build_cached_prompt()
        
        # Store in Redis
        await self.redis.setex(
            "sdlc:framework:context:v1",
            self.ttl,
            prompt.encode()
        )
        
        return prompt
    
    def _build_cached_prompt(self) -> str:
        """Load framework docs and mark cache boundaries."""
        sections = [
            self._load_section("SDLC-Enterprise-Framework/02-Core-Methodology/README.md"),
            self._load_section("docs/02-design/ADR-*.md"),
            self._load_section("backend/app/services/codegen/templates/*.j2"),
        ]
        
        # Add cache_control markers (Anthropic syntax)
        return format_with_cache_control(sections)
    
    async def invalidate(self):
        """Force cache refresh (e.g., after framework update)."""
        await self.redis.delete("sdlc:framework:context:v1")
```

### 2. Integration with Codegen Service

```python
# backend/app/services/codegen/codegen_service.py
class CodegenService:
    def __init__(
        self,
        cache: SDLCContextCache,
        anthropic_client: Anthropic
    ):
        self.cache = cache
        self.client = anthropic_client
    
    async def generate_code(self, blueprint: IRBlueprint) -> CodeBundle:
        # Get cached framework context
        cached_context = await self.cache.get_cached_prompt()
        
        # Call Anthropic with cached prompt
        response = await self.client.messages.create(
            model="claude-opus-4.5",
            messages=[
                {"role": "system", "content": cached_context},  # Cached
                {"role": "user", "content": f"Generate code for: {blueprint}"}  # Not cached
            ],
            max_tokens=4096
        )
        
        # Track cache hit (for metrics)
        await self._record_cache_metrics(response.usage)
        
        return parse_code_bundle(response.content)
    
    async def _record_cache_metrics(self, usage: Usage):
        """Push metrics to Prometheus."""
        cache_hit = usage.cache_read_input_tokens > 0
        
        metrics.cache_hit_rate.observe(1 if cache_hit else 0)
        metrics.cost_per_request.observe(
            calculate_cost(usage)  # $0.002 vs $0.012
        )
```

### 3. Manual Cache Invalidation (CLI)

```python
# backend/sdlcctl/commands/cache.py
import click

@click.group()
def cache():
    """Manage SDLC framework context cache."""
    pass

@cache.command()
@click.option("--force", is_flag=True, help="Skip confirmation")
def clear(force: bool):
    """Clear cached framework context (forces rebuild)."""
    if not force:
        click.confirm("This will invalidate all cached contexts. Continue?", abort=True)
    
    # Redis flush
    redis_client = get_redis_client()
    redis_client.delete("sdlc:framework:context:v1")
    
    click.echo("✅ Cache cleared. Next codegen request will rebuild.")

@cache.command()
def stats():
    """Show cache statistics."""
    # Query Prometheus
    stats = get_cache_stats()
    
    click.echo(f"Cache hit rate (24h): {stats.hit_rate:.1%}")
    click.echo(f"Requests served: {stats.total_requests}")
    click.echo(f"Cost savings: ${stats.savings:.2f}")
```

---

## 🐛 Debugging Tips

### Issue: Cache hit rate is low (<50%)
**Diagnosis**:
```bash
# Check Redis
docker exec -it sdlc-redis redis-cli
> GET sdlc:framework:context:v1
> TTL sdlc:framework:context:v1  # Should be ~86400 (24h)
```

**Possible causes**:
- TTL too short (cache expires too fast)
- Framework updates trigger frequent invalidation
- Redis memory full (LRU eviction)

**Fix**:
- Increase TTL: `self.ttl = timedelta(hours=48)`
- Check Redis memory: `INFO memory`
- Review invalidation webhooks (too aggressive?)

### Issue: Anthropic API errors
**Error**: `400 Bad Request: cache_control not supported`

**Fix**: Verify API version (needs v1.8.0+):
```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    api_version="2025-02-01"  # Must support cache_control
)
```

### Issue: Cost not reducing
**Diagnosis**:
```python
# Check Anthropic usage dashboard
response = client.messages.create(...)
print(response.usage)
# Usage(input_tokens=1200, cache_read_input_tokens=10800, ...)
#       └─ New tokens       └─ Cached tokens (should be >80%)
```

**Expected**:
- First request: `cache_creation_input_tokens = 10800` (write to cache)
- Subsequent: `cache_read_input_tokens = 10800` (read from cache)

---

## 📚 References

- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/claude/docs/prompt-caching)
- [ADR-054: Full Analysis](../../02-design/ADR-054-Anthropic-Claude-Code-Best-Practices.md)
- [Sprint 174 Plan](SPRINT-174-ANTHROPIC-PATTERNS-INTEGRATION.md)
- [Redis Cache Strategy (internal)](https://redis.io/docs/manual/client-side-caching/)

---

## 🚨 Critical Alerts

### Alert 1: Cache hit rate drops below 70%
**Trigger**: `cache_hit_rate_24h < 0.70`  
**Action**: 
1. Check Redis health: `docker logs sdlc-redis`
2. Review recent framework commits (did we push 50 updates today?)
3. Consider increasing TTL (24h → 48h)

### Alert 2: Cost per request exceeds $0.005
**Trigger**: `cost_per_codegen_request_p95 > 0.005`  
**Action**:
1. Verify cache is working: `curl localhost:9090/metrics | grep cache_hit`
2. Check Anthropic dashboard (usage spikes?)
3. Roll back if broken (disable caching temporarily)

---

## ✅ Sprint 174 DoD (Definition of Done)

Before marking sprint complete:
- [ ] Cache hit rate >85% (Grafana screenshot in Slack)
- [ ] Cost per request <$0.002 (Prometheus query result)
- [ ] Grafana dashboard live (4 panels)
- [ ] Runbook documented (`cache-invalidation.md`)
- [ ] MCP positioning doc published (docs site)
- [ ] Sales team trained (Day 10 all-hands)

---

*Quick Reference Guide — Sprint 174*  
*Engineering Team — SDLC Orchestrator*  
*February 16, 2026*
