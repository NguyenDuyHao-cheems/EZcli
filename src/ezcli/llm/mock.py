"""Mock LLM Provider cho ezcli."""

from typing import Any
from ezcli.llm.result import LLMResult


class MockLLMProvider:
    """Cung cấp kết quả giả lập cho LLM phục vụ kiểm thử và phát triển offline."""

    def generate_command(
        self, prompt: str, context: dict[str, Any] | None = None
    ) -> LLMResult:
        """Sinh nội dung phản hồi giả lập dựa trên prompt."""
        _ = context
        prompt_lower = prompt.lower().strip()

        if "lỗi" in prompt_lower or "error" in prompt_lower:
            return LLMResult(
                success=False,
                content="",
                error=("Không thể xử lý yêu cầu này. Vui lòng thử lại!"),
            )

        if "json" in prompt_lower or "tìm" in prompt_lower:
            return LLMResult(
                success=True,
                content='find . -type f -name "*.json"',
            )

        return LLMResult(
            success=True,
            content=f"echo '{prompt}'",
        )
