"""
Mock Services Fixtures Package - Sprint 142 (RA-004)

Provides reusable mock configurations for external services:
- MockRedis: In-memory Redis simulation
- MockSMTP: Email capture without network
- MockOPAClient: Policy evaluation simulation
- MockMinIOClient: Object storage simulation

Usage:
    from tests.unit.fixtures.mock_services import MockRedis, MockSMTP
"""

from tests.unit.fixtures.mock_services import (
    MockRedis,
    MockRedisPipeline,
    MockSMTP,
    MockOPAClient,
    MockMinIOClient,
)

__all__ = [
    "MockRedis",
    "MockRedisPipeline",
    "MockSMTP",
    "MockOPAClient",
    "MockMinIOClient",
]
