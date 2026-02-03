"""Integration tests for worktree commands.

These tests use real git repositories (not mocked) to verify worktree functionality
in realistic scenarios. Each test creates a temporary git repository and performs
actual git operations.

Sprint 144 Day 3 - Integration Testing
CTO Directive: Test real git operations, verify worktree isolation, <5s total execution
"""

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from sdlcctl.commands.worktree import app

runner = CliRunner()


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def real_git_repo() -> Generator[Path, None, None]:
    """Create a real git repository for integration testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "test-repo"
        repo_path.mkdir()

        # Initialize git repository
        subprocess.run(
            ["git", "init"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        # Configure git user (required for commits)
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        # Create initial commit
        readme = repo_path / "README.md"
        readme.write_text("# Test Repository\n")
        subprocess.run(
            ["git", "add", "README.md"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        yield repo_path

        # Cleanup: Remove all worktrees before deleting directory
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            # Parse worktree paths and remove non-main worktrees
            for line in result.stdout.split('\n'):
                if line.startswith('worktree '):
                    worktree_path = Path(line.split(' ', 1)[1])
                    if worktree_path != repo_path:
                        subprocess.run(
                            ["git", "worktree", "remove", "--force", str(worktree_path)],
                            cwd=repo_path,
                            capture_output=True
                        )
        except subprocess.CalledProcessError:
            pass  # Repository might be in inconsistent state, cleanup will handle it


# ============================================================================
# Test 1: Full Lifecycle (add → list → sync → remove)
# ============================================================================


def test_full_lifecycle(real_git_repo: Path):
    """Test complete worktree lifecycle: create, list, sync, remove.

    CTO Directive: Full lifecycle test, <5s total execution time
    """
    start_time = time.time()

    # Step 1: Create a worktree
    worktree_path = real_git_repo.parent / "test-worktree"
    result = runner.invoke(app, [
        'add',
        str(worktree_path),
        'feature/test',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "Worktree created successfully" in result.output
    assert worktree_path.exists()
    assert (worktree_path / "README.md").exists()

    # Step 2: List worktrees
    result = runner.invoke(app, [
        'list',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "2 Worktree(s)" in result.output
    assert "feature/test" in result.output

    # Step 3: Make a commit in main worktree
    new_file = real_git_repo / "new-file.txt"
    new_file.write_text("New content\n")
    subprocess.run(
        ["git", "add", "new-file.txt"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", "Add new file"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )

    # Step 4: Sync worktree (rebase on main)
    result = runner.invoke(app, [
        'sync',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    # Note: Sync may report "Already up to date" or success

    # Step 5: Remove worktree
    result = runner.invoke(app, [
        'remove',
        str(worktree_path),
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "Worktree removed successfully" in result.output
    assert not worktree_path.exists()

    # Verify total execution time
    elapsed = time.time() - start_time
    assert elapsed < 5.0, f"Full lifecycle took {elapsed:.2f}s (target: <5s)"


# ============================================================================
# Test 2: Parallel Sessions (3 worktrees, verify isolation)
# ============================================================================


def test_parallel_sessions_isolation(real_git_repo: Path):
    """Test creating 3 worktrees and verify they are isolated.

    CTO Directive: 3 worktrees, verify isolation, <10s execution
    Boris Cherny Pattern: Backend, Frontend, Tests worktrees
    """
    start_time = time.time()

    # Create 3 worktrees for parallel development
    worktree_backend = real_git_repo.parent / "backend"
    worktree_frontend = real_git_repo.parent / "frontend"
    worktree_tests = real_git_repo.parent / "tests"

    # Create backend worktree
    result = runner.invoke(app, [
        'add',
        str(worktree_backend),
        'feature/backend',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0

    # Create frontend worktree
    result = runner.invoke(app, [
        'add',
        str(worktree_frontend),
        'feature/frontend',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0

    # Create tests worktree
    result = runner.invoke(app, [
        'add',
        str(worktree_tests),
        'feature/tests',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0

    # Verify all worktrees exist
    assert worktree_backend.exists()
    assert worktree_frontend.exists()
    assert worktree_tests.exists()

    # List worktrees
    result = runner.invoke(app, [
        'list',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "4 Worktree(s)" in result.output  # Main + 3 worktrees

    # Test isolation: Create different files in each worktree
    backend_file = worktree_backend / "backend.py"
    frontend_file = worktree_frontend / "frontend.js"
    tests_file = worktree_tests / "tests.py"

    backend_file.write_text("# Backend code\n")
    frontend_file.write_text("// Frontend code\n")
    tests_file.write_text("# Test code\n")

    # Verify isolation: Files don't leak between worktrees
    assert backend_file.exists()
    assert not (worktree_frontend / "backend.py").exists()
    assert not (worktree_tests / "backend.py").exists()

    assert frontend_file.exists()
    assert not (worktree_backend / "frontend.js").exists()
    assert not (worktree_tests / "frontend.js").exists()

    assert tests_file.exists()
    assert not (worktree_backend / "tests.py").exists()
    assert not (worktree_frontend / "tests.py").exists()

    # Cleanup
    for worktree in [worktree_backend, worktree_frontend, worktree_tests]:
        result = runner.invoke(app, [
            'remove',
            str(worktree),
            '--force',  # Force because uncommitted changes
            '--project', str(real_git_repo)
        ])
        assert result.exit_code == 0

    # Verify total execution time
    elapsed = time.time() - start_time
    assert elapsed < 10.0, f"Parallel sessions test took {elapsed:.2f}s (target: <10s)"


# ============================================================================
# Test 3: Conflict Resolution (sync with uncommitted changes)
# ============================================================================


def test_conflict_resolution_uncommitted_changes(real_git_repo: Path):
    """Test sync behavior with uncommitted changes.

    CTO Directive: Error handling for uncommitted changes
    """
    # Create worktree
    worktree_path = real_git_repo.parent / "conflict-worktree"
    result = runner.invoke(app, [
        'add',
        str(worktree_path),
        'feature/conflict',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0

    # Make uncommitted changes in worktree
    conflict_file = worktree_path / "uncommitted.txt"
    conflict_file.write_text("Uncommitted changes\n")

    # Make a commit in main
    main_file = real_git_repo / "main-file.txt"
    main_file.write_text("Main changes\n")
    subprocess.run(
        ["git", "add", "main-file.txt"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", "Changes in main"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )

    # Try to sync (should handle uncommitted changes gracefully)
    result = runner.invoke(app, [
        'sync',
        '--project', str(real_git_repo)
    ])

    # Sync may warn about uncommitted changes but should not crash
    assert result.exit_code == 0

    # Cleanup
    result = runner.invoke(app, [
        'remove',
        str(worktree_path),
        '--force',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0


# ============================================================================
# Test 4: Error Recovery (invalid paths, permissions)
# ============================================================================


def test_error_recovery_invalid_paths(real_git_repo: Path):
    """Test graceful error handling for invalid paths and conditions.

    CTO Directive: Graceful failures for error conditions
    """
    # Test 1: Create worktree with existing path (without --force)
    existing_path = real_git_repo.parent / "existing"
    existing_path.mkdir()

    result = runner.invoke(app, [
        'add',
        str(existing_path),
        'feature/test',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 1
    assert "already exists" in result.output.lower()

    # Test 2: Create worktree with existing path using --force
    result = runner.invoke(app, [
        'add',
        str(existing_path),
        'feature/test',
        '--force',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "Worktree created successfully" in result.output

    # Test 3: List worktrees in non-git directory
    non_git_dir = real_git_repo.parent / "non-git"
    non_git_dir.mkdir()

    result = runner.invoke(app, [
        'list',
        '--project', str(non_git_dir)
    ])

    assert result.exit_code == 1
    assert "Not a git repository" in result.output

    # Test 4: Remove worktree with uncommitted changes (without --force)
    test_file = existing_path / "test.txt"
    test_file.write_text("Uncommitted\n")

    result = runner.invoke(app, [
        'remove',
        str(existing_path),
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 1
    assert "Hint" in result.output
    assert "--force" in result.output

    # Test 5: Remove with --force
    result = runner.invoke(app, [
        'remove',
        str(existing_path),
        '--force',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "Worktree removed successfully" in result.output


# ============================================================================
# Test 5: Performance (all commands <2s each)
# ============================================================================


def test_performance_all_commands(real_git_repo: Path):
    """Test that all commands execute within performance budget.

    CTO Directive: All commands <2s execution time each
    """
    worktree_path = real_git_repo.parent / "perf-worktree"

    # Test 1: add command performance
    start = time.time()
    result = runner.invoke(app, [
        'add',
        str(worktree_path),
        'feature/perf',
        '--project', str(real_git_repo)
    ])
    add_time = time.time() - start

    assert result.exit_code == 0
    assert add_time < 2.0, f"add command took {add_time:.2f}s (target: <2s)"

    # Test 2: list command performance
    start = time.time()
    result = runner.invoke(app, [
        'list',
        '--project', str(real_git_repo)
    ])
    list_time = time.time() - start

    assert result.exit_code == 0
    assert list_time < 2.0, f"list command took {list_time:.2f}s (target: <2s)"

    # Test 3: list --porcelain performance
    start = time.time()
    result = runner.invoke(app, [
        'list',
        '--porcelain',
        '--project', str(real_git_repo)
    ])
    porcelain_time = time.time() - start

    assert result.exit_code == 0
    assert porcelain_time < 2.0, f"list --porcelain took {porcelain_time:.2f}s (target: <2s)"

    # Test 4: sync command performance
    start = time.time()
    result = runner.invoke(app, [
        'sync',
        '--project', str(real_git_repo)
    ])
    sync_time = time.time() - start

    assert result.exit_code == 0
    assert sync_time < 2.0, f"sync command took {sync_time:.2f}s (target: <2s)"

    # Test 5: remove command performance
    start = time.time()
    result = runner.invoke(app, [
        'remove',
        str(worktree_path),
        '--project', str(real_git_repo)
    ])
    remove_time = time.time() - start

    assert result.exit_code == 0
    assert remove_time < 2.0, f"remove command took {remove_time:.2f}s (target: <2s)"

    # Summary
    total_time = add_time + list_time + porcelain_time + sync_time + remove_time
    print(f"\n=== Performance Summary ===")
    print(f"add:            {add_time:.3f}s")
    print(f"list:           {list_time:.3f}s")
    print(f"list (JSON):    {porcelain_time:.3f}s")
    print(f"sync:           {sync_time:.3f}s")
    print(f"remove:         {remove_time:.3f}s")
    print(f"Total:          {total_time:.3f}s")
    print(f"===========================")


# ============================================================================
# Bonus Test: Dry-run mode
# ============================================================================


def test_sync_dry_run(real_git_repo: Path):
    """Test sync --dry-run mode (no actual changes)."""
    # Create worktree
    worktree_path = real_git_repo.parent / "dry-run-worktree"
    result = runner.invoke(app, [
        'add',
        str(worktree_path),
        'feature/dry-run',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0

    # Make a commit in main
    test_file = real_git_repo / "dry-run-file.txt"
    test_file.write_text("Dry run test\n")
    subprocess.run(
        ["git", "add", "dry-run-file.txt"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", "Dry run commit"],
        cwd=real_git_repo,
        check=True,
        capture_output=True
    )

    # Run sync with --dry-run
    result = runner.invoke(app, [
        'sync',
        '--dry-run',
        '--project', str(real_git_repo)
    ])

    assert result.exit_code == 0
    assert "DRY RUN" in result.output
    assert "Would sync" in result.output or "Would fetch" in result.output

    # Cleanup
    result = runner.invoke(app, [
        'remove',
        str(worktree_path),
        '--force',
        '--project', str(real_git_repo)
    ])
    assert result.exit_code == 0
