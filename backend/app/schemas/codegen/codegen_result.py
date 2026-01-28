"""
Codegen Result Schema - Output from code generation

SDLC Framework Compliance:
- Framework: SDLC 5.3.0 (8-Pillar Architecture)
- Pillar 3: Build Phase - Code Generation Results
- AI Governance Principle 5: Cost Transparency & Auditing
- Methodology: Complete audit trail for AI-generated code

Purpose:
Output schema for code generation results. Includes:
- Generated files with content
- Cost breakdown (planning + execution)
- Provider metadata
- Performance metrics

Used by Evidence Vault for audit trail and governance compliance.

Sprint: 106 - App Builder Integration (MVP)
Date: January 28, 2026
Owner: Backend Team
Status: ACTIVE
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path


class GeneratedFile(BaseModel):
    """
    Single generated file from codegen.

    Attributes:
        path: Relative file path (e.g., "src/pages/index.tsx")
        content: File content as string
        language: Programming language for syntax highlighting
        is_binary: True if file is binary (images, fonts)
    """
    path: str = Field(..., description="Relative file path")
    content: str = Field(..., description="File content")
    language: str = Field(default="text", description="Programming language")
    is_binary: bool = Field(default=False, description="True if binary file")

    def __post_init__(self):
        """Auto-detect language from file extension if not provided"""
        if self.language == "text" and not self.is_binary:
            ext_map = {
                '.py': 'python',
                '.ts': 'typescript',
                '.tsx': 'typescriptreact',
                '.js': 'javascript',
                '.jsx': 'javascriptreact',
                '.json': 'json',
                '.md': 'markdown',
                '.yml': 'yaml',
                '.yaml': 'yaml',
                '.toml': 'toml',
                '.env': 'dotenv',
                '.sql': 'sql',
                '.sh': 'bash',
                '.prisma': 'prisma',
            }
            ext = Path(self.path).suffix
            self.language = ext_map.get(ext, 'text')

    @property
    def size_bytes(self) -> int:
        """Get file size in bytes"""
        return len(self.content.encode('utf-8'))


class CostBreakdown(BaseModel):
    """
    Cost breakdown for code generation.

    Separates planning (LLM analysis) from execution (deterministic/LLM).
    App Builder: $0 execution (deterministic templates).
    Ollama/Claude: Variable execution cost based on tokens.

    AI Governance Principle 5: Full cost transparency for auditing.
    """

    # Planning phase (LLM risk analysis, blueprint generation)
    planning_provider: str = Field(
        default="ollama",
        description="Provider used for planning: ollama, claude, rule-based"
    )
    planning_tokens: int = Field(
        default=0,
        description="Tokens used for planning phase"
    )
    planning_cost_usd: float = Field(
        default=0.0,
        description="Cost of planning phase in USD"
    )

    # Execution phase (template scaffolding or LLM generation)
    execution_provider: str = Field(
        default="app-builder",
        description="Provider used for execution: app-builder, ollama, claude"
    )
    execution_tokens: int = Field(
        default=0,
        description="Tokens used for execution (0 for app-builder)"
    )
    execution_cost_usd: float = Field(
        default=0.0,
        description="Cost of execution phase in USD ($0 for app-builder)"
    )

    # Totals
    @property
    def total_tokens(self) -> int:
        """Total tokens used"""
        return self.planning_tokens + self.execution_tokens

    @property
    def total_cost_usd(self) -> float:
        """Total cost in USD"""
        return self.planning_cost_usd + self.execution_cost_usd

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with computed properties"""
        return {
            "planning_provider": self.planning_provider,
            "planning_tokens": self.planning_tokens,
            "planning_cost_usd": self.planning_cost_usd,
            "execution_provider": self.execution_provider,
            "execution_tokens": self.execution_tokens,
            "execution_cost_usd": self.execution_cost_usd,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
        }


class CodegenResult(BaseModel):
    """
    Complete result from code generation.

    Used by:
    - CodegenService to return results
    - Evidence Vault for audit storage
    - Frontend for file preview

    Example:
        result = CodegenResult(
            files=[
                GeneratedFile(path="src/index.tsx", content="...", language="tsx"),
                GeneratedFile(path="package.json", content="...", language="json"),
            ],
            provider="app-builder",
            generation_time_ms=2500,
            metadata={"template": "nextjs-fullstack"},
            cost_breakdown=CostBreakdown(
                planning_cost_usd=0.02,
                execution_cost_usd=0.00,
            )
        )
    """

    # Generated files
    files: List[GeneratedFile] = Field(
        ...,
        description="List of generated files"
    )

    # Provider info
    provider: str = Field(
        ...,
        description="Provider that generated the code: app-builder, ollama, claude"
    )
    provider_version: str = Field(
        default="1.0.0",
        description="Provider version"
    )

    # Performance
    generation_time_ms: int = Field(
        ...,
        description="Total generation time in milliseconds"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific metadata (template, blueprint_id, etc.)"
    )

    # Cost tracking
    cost_breakdown: CostBreakdown = Field(
        default_factory=CostBreakdown,
        description="Cost breakdown for planning + execution"
    )

    # Status
    success: bool = Field(
        default=True,
        description="True if generation succeeded"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if generation failed"
    )

    # Audit
    result_id: str = Field(
        default_factory=lambda: __import__('uuid').uuid4().hex[:16],
        description="Unique result identifier"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Result creation timestamp"
    )

    @property
    def file_count(self) -> int:
        """Number of generated files"""
        return len(self.files)

    @property
    def total_size_bytes(self) -> int:
        """Total size of all generated files"""
        return sum(f.size_bytes for f in self.files)

    @property
    def total_lines(self) -> int:
        """Total lines of code generated"""
        return sum(len(f.content.split('\n')) for f in self.files)

    @property
    def tokens_used(self) -> int:
        """Total tokens used (alias for cost_breakdown.total_tokens)"""
        return self.cost_breakdown.total_tokens

    def get_summary(self) -> Dict[str, Any]:
        """
        Get human-readable summary for logging and display.

        Returns:
            Summary dict with key metrics
        """
        return {
            "provider": self.provider,
            "files": self.file_count,
            "total_lines": self.total_lines,
            "total_size_kb": round(self.total_size_bytes / 1024, 2),
            "generation_time_ms": self.generation_time_ms,
            "cost_usd": self.cost_breakdown.total_cost_usd,
            "success": self.success,
        }

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "files": [
                    {
                        "path": "src/app/page.tsx",
                        "content": "export default function Home() { return <div>Hello</div> }",
                        "language": "typescriptreact"
                    },
                    {
                        "path": "package.json",
                        "content": '{"name": "my-app", "version": "1.0.0"}',
                        "language": "json"
                    }
                ],
                "provider": "app-builder",
                "generation_time_ms": 2500,
                "metadata": {
                    "template": "nextjs-fullstack",
                    "template_version": "1.0.0",
                    "blueprint_id": "abc123"
                },
                "cost_breakdown": {
                    "planning_provider": "ollama",
                    "planning_tokens": 1500,
                    "planning_cost_usd": 0.02,
                    "execution_provider": "app-builder",
                    "execution_tokens": 0,
                    "execution_cost_usd": 0.00
                },
                "success": True
            }
        }
