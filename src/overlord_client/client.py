"""
Overlord Platform Client
Connects to Overlord backend for AI services
"""
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

from src.config import settings


class OverlordClient:
    """
    Client for Overlord AI platform
    Provides AI chat, embeddings, and analysis capabilities
    """

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Overlord client

        Args:
            api_url: Overlord API base URL
            api_key: API authentication key
        """
        self.api_url = api_url or settings.overlord_api_url
        self.api_key = api_key or settings.overlord_api_key
        self.client = httpx.AsyncClient(timeout=60.0)

        if not self.api_key:
            print("Warning: Overlord API key not set. AI features will be limited.")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def chat_completion(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        agent_name: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Get AI chat completion

        Args:
            message: User message
            system_prompt: System prompt for agent personality
            agent_name: Name of the agent (for context)
            context: Previous conversation context
            temperature: Sampling temperature

        Returns:
            Chat completion response
        """
        try:
            # Build messages array
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            if context:
                messages.extend(context)

            messages.append({"role": "user", "content": message})

            # Send request to Overlord
            response = await self.client.post(
                f"{self.api_url}/ai/chat",
                headers=self._get_headers(),
                json={
                    "messages": messages,
                    "temperature": temperature,
                    "metadata": {
                        "agent_name": agent_name,
                        "source": "agent-cleo"
                    }
                }
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message": data.get("response", ""),
                    "usage": data.get("usage", {}),
                    "model": data.get("model", "unknown")
                }
            else:
                return {
                    "success": False,
                    "error": f"Overlord API error: {response.status_code}",
                    "message": "Failed to get AI response"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to connect to Overlord AI service"
            }

    async def generate_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate embeddings for text

        Args:
            texts: List of text strings to embed
            model: Embedding model name

        Returns:
            Embeddings response
        """
        try:
            response = await self.client.post(
                f"{self.api_url}/ai/embeddings",
                headers=self._get_headers(),
                json={
                    "texts": texts,
                    "model": model
                }
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "embeddings": data.get("embeddings", []),
                    "model": data.get("model", "unknown")
                }
            else:
                return {
                    "success": False,
                    "error": f"Overlord API error: {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def analyze_content(
        self,
        content: str,
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze content using AI

        Args:
            content: Content to analyze
            analysis_type: Type of analysis (general, sentiment, entities, etc.)

        Returns:
            Analysis response
        """
        try:
            response = await self.client.post(
                f"{self.api_url}/ai/analyze",
                headers=self._get_headers(),
                json={
                    "content": content,
                    "analysis_type": analysis_type
                }
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "analysis": data.get("analysis", {}),
                    "metadata": data.get("metadata", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"Overlord API error: {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def health_check(self) -> bool:
        """
        Check Overlord service health

        Returns:
            True if healthy, False otherwise
        """
        try:
            response = await self.client.get(
                f"{self.api_url}/health",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except:
            return False

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
_overlord_client: Optional[OverlordClient] = None


async def get_overlord_client() -> OverlordClient:
    """Get or create Overlord client instance"""
    global _overlord_client
    if _overlord_client is None:
        _overlord_client = OverlordClient()
    return _overlord_client
