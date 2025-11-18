"""
Overlord Service - Business logic for Overlord AI platform integration
"""
from typing import Optional, List, Dict, Any
from ..overlord_client.client import get_overlord_client


class OverlordService:
    """Service class for Overlord platform operations"""

    @staticmethod
    async def get_chat_response(
        message: str,
        system_prompt: str,
        agent_name: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Get AI chat response from Overlord"""
        client = await get_overlord_client()
        return await client.chat_completion(
            message=message,
            system_prompt=system_prompt,
            agent_name=agent_name,
            context=context or []
        )

    @staticmethod
    async def generate_embeddings(text: str) -> List[float]:
        """Generate text embeddings via Overlord"""
        client = await get_overlord_client()
        result = await client.generate_embeddings(text)
        return result.get("embeddings", [])

    @staticmethod
    async def analyze_content(content: str, task: str) -> Dict[str, Any]:
        """Analyze content with specified task"""
        client = await get_overlord_client()
        return await client.analyze_content(content, task)

    @staticmethod
    async def check_health() -> bool:
        """Check Overlord platform health"""
        client = await get_overlord_client()
        return await client.health_check()
