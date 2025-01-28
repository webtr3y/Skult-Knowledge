from loguru import logger
import httpx
from typing import Optional, Dict, List, Any
from tenacity import retry, stop_after_attempt, wait_exponential

class BlockchainService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.base_url = "https://rest.atlantic-2.seinetwork.io"
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def verify_connection(self) -> bool:
        """Verify connection to the blockchain with retry logic."""
        try:
            logger.info("Verifying blockchain connection...")
            response = await self.client.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/node_info")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to verify blockchain connection: {str(e)}")
            return False

    async def get_latest_block(self) -> Optional[Dict]:
        """Get the latest block information."""
        try:
            response = await self.client.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/blocks/latest")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Failed to get latest block: {str(e)}")
            return None

    async def get_account_transactions(self, address: str, limit: int = 100) -> List[Dict]:
        """Get transactions for a specific account."""
        try:
            response = await self.client.get(
                f"{self.base_url}/cosmos/tx/v1beta1/txs",
                params={
                    "events": f"message.sender='{address}'",
                    "pagination.limit": str(limit)
                }
            )
            if response.status_code == 200:
                return response.json().get("tx_responses", [])
            return []
        except Exception as e:
            logger.error(f"Failed to get account transactions: {str(e)}")
            return []

    async def close(self):
        """Close the HTTP client connection."""
        await self.client.aclose()

    async def fetch_real_time_data(self) -> Dict[str, Any]:
        # Implement real-time data fetching
        return {} 

    async def fetch_detailed_block_data(self, block_height: int) -> Dict:
        """Fetch detailed data for a specific block."""
        try:
            response = await self.client.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/blocks/{block_height}")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"Failed to fetch block data: {str(e)}")
            return {} 