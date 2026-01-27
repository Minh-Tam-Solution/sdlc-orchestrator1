#!/usr/bin/env python3
"""
Quick GateService test runner - Validates implementation without full test infrastructure.

This script tests GateService directly without pytest infrastructure.
Used for rapid TDD feedback during implementation.
"""

import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.gate_service import (
    GateService,
    InvalidGateCodeError,
    GateNotFoundError,
    GateValidationError,
    VALID_GATE_CODES,
)


class MockDB:
    """Mock database for testing without real DB."""
    
    def __init__(self):
        self.gates = {}
        self.next_id = 1
        self.committed = []
    
    def add(self, gate):
        gate.id = f"gate-{self.next_id}"
        self.next_id += 1
        self.gates[gate.id] = gate
    
    async def commit(self):
        self.committed.append(True)
    
    async def refresh(self, gate):
        pass
    
    async def execute(self, stmt):
        class Result:
            def __init__(self, gate=None):
                self._gate = gate
            
            def scalar_one_or_none(self):
                return self._gate
            
            def scalars(self):
                class Scalars:
                    def __init__(self, gates):
                        self._gates = gates
                    def all(self):
                        return self._gates
                return Scalars(list(self._gate) if isinstance(self._gate, list) else [])
        
        # Simple mock - return None for not found
        return Result(None)


class MockGate:
    """Mock Gate model."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = None
        self.deleted_at = None


async def test_create_gate_valid():
    """Test 1: Create gate with valid code."""
    print("Test 1: create_gate() with valid code...", end=" ")
    
    db = MockDB()
    service = GateService(db)
    
    # Mock Gate class
    import app.services.gate_service as gate_module
    original_gate = gate_module.Gate
    gate_module.Gate = MockGate
    
    try:
        gate = await service.create_gate(
            project_id="project-1",
            gate_code="G0.1",
            gate_name="Foundation Ready",
            created_by="user-1",
            description="Test gate"
        )
        
        assert gate.gate_type == "G0.1"
        assert gate.stage == "WHY"
        assert gate.status == "DRAFT"
        assert gate.id == "gate-1"
        print("✅ PASS")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False
    finally:
        gate_module.Gate = original_gate


async def test_create_gate_invalid_code():
    """Test 2: Create gate with invalid code raises error."""
    print("Test 2: create_gate() with invalid code raises error...", end=" ")
    
    db = MockDB()
    service = GateService(db)
    
    # Mock Gate class
    import app.services.gate_service as gate_module
    original_gate = gate_module.Gate
    gate_module.Gate = MockGate
    
    try:
        await service.create_gate(
            project_id="project-1",
            gate_code="INVALID",
            gate_name="Bad Gate",
            created_by="user-1"
        )
        print("❌ FAIL: Should have raised InvalidGateCodeError")
        return False
    except InvalidGateCodeError as e:
        assert "INVALID" in str(e)
        print("✅ PASS")
        return True
    except Exception as e:
        print(f"❌ FAIL: Wrong exception: {e}")
        return False
    finally:
        gate_module.Gate = original_gate


async def test_valid_gate_codes():
    """Test 3: All valid gate codes."""
    print("Test 3: Valid gate codes configured...", end=" ")
    
    expected_codes = ["G0.1", "G0.2", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
    
    if VALID_GATE_CODES == expected_codes:
        print("✅ PASS")
        return True
    else:
        print(f"❌ FAIL: Expected {expected_codes}, got {VALID_GATE_CODES}")
        return False


async def test_reject_gate_requires_reason():
    """Test 4: reject_gate() requires reason."""
    print("Test 4: reject_gate() requires reason...", end=" ")
    
    db = MockDB()
    service = GateService(db)
    
    # Add mock gate
    gate = MockGate(
        id="gate-1",
        gate_type="G1",
        stage="WHAT",
        status="PENDING_APPROVAL",
        deleted_at=None
    )
    db.gates["gate-1"] = gate
    
    # Mock execute to return gate
    original_execute = db.execute
    async def mock_execute(stmt):
        class Result:
            def scalar_one_or_none(self):
                return gate
        return Result()
    db.execute = mock_execute
    
    try:
        await service.reject_gate(
            gate_id="gate-1",
            approver_id="user-1",
            rejection_reason=""  # Empty reason
        )
        print("❌ FAIL: Should have raised GateValidationError")
        return False
    except GateValidationError as e:
        assert "required" in str(e).lower()
        print("✅ PASS")
        return True
    except Exception as e:
        print(f"❌ FAIL: Wrong exception: {e}")
        return False
    finally:
        db.execute = original_execute


async def main():
    """Run all tests."""
    print("=" * 60)
    print("GateService Quick Tests (TDD GREEN Phase)")
    print("=" * 60)
    print()
    
    tests = [
        test_create_gate_valid,
        test_create_gate_invalid_code,
        test_valid_gate_codes,
        test_reject_gate_requires_reason,
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Implementation is GREEN!")
    else:
        print(f"❌ {total - passed} tests failed - Need fixes")
    
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
