from typing import Dict, List, Optional
from datetime import datetime, timedelta
import aiohttp
from loguru import logger
from ...config.settings import Settings

class NetworkAnalytics:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.SEI_RPC_URL
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            
    async def get_transactions_per_second(self) -> float:
        """Calculate current TPS"""
        try:
            async with self.session.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/blocks/latest") as response:
                if response.status == 200:
                    data = await response.json()
                    return await self._calculate_tps(data)
                raise Exception(f"Failed to get block data: {response.status}")
        except Exception as e:
            logger.error(f"Error calculating TPS: {str(e)}")
            return 0.0

    async def count_active_validators(self) -> int:
        """Get count of active validators"""
        try:
            async with self.session.get(f"{self.base_url}/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED") as response:
                if response.status == 200:
                    data = await response.json()
                    return len(data.get('validators', []))
                raise Exception(f"Failed to get validators: {response.status}")
        except Exception as e:
            logger.error(f"Error counting validators: {str(e)}")
            return 0

    async def get_total_stake(self) -> float:
        """Get total staked SEI"""
        try:
            async with self.session.get(f"{self.base_url}/cosmos/staking/v1beta1/pool") as response:
                if response.status == 200:
                    data = await response.json()
                    bonded_tokens = float(data.get('pool', {}).get('bonded_tokens', 0))
                    return bonded_tokens / 1e6  # Convert to SEI
                raise Exception(f"Failed to get stake data: {response.status}")
        except Exception as e:
            logger.error(f"Error getting total stake: {str(e)}")
            return 0.0

    async def get_average_block_time(self) -> float:
        """Calculate average block time in seconds"""
        try:
            blocks = await self._get_recent_blocks(100)
            if not blocks:
                return 0.0
            
            times = [datetime.fromisoformat(block['header']['time'].replace('Z', '+00:00')) 
                    for block in blocks]
            differences = [(times[i] - times[i+1]).total_seconds() 
                         for i in range(len(times)-1)]
            
            return sum(differences) / len(differences)
        except Exception as e:
            logger.error(f"Error calculating block time: {str(e)}")
            return 0.0

    async def calculate_uptime(self) -> float:
        """Calculate network uptime percentage"""
        try:
            async with self.session.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/syncing") as response:
                if response.status == 200:
                    data = await response.json()
                    return 100.0 if not data.get('syncing', True) else 0.0
                raise Exception(f"Failed to get sync status: {response.status}")
        except Exception as e:
            logger.error(f"Error calculating uptime: {str(e)}")
            return 0.0

    async def get_consensus_status(self) -> Dict:
        """Get consensus status"""
        try:
            async with self.session.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/blocks/latest") as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'height': int(data['block']['header']['height']),
                        'time': data['block']['header']['time'],
                        'proposer': data['block']['header']['proposer_address']
                    }
                raise Exception(f"Failed to get consensus status: {response.status}")
        except Exception as e:
            logger.error(f"Error getting consensus status: {str(e)}")
            return {}

    def calculate_health_score(self, metrics: Dict) -> Dict:
        """Calculate overall network health score"""
        try:
            scores = {
                'uptime': metrics['uptime'] / 100 * 0.4,  # 40% weight
                'consensus': 1.0 if metrics['consensus'] else 0.0,  # 30% weight
                'peer_count': min(metrics['peer_count'] / 10, 1.0) * 0.3  # 30% weight
            }
            total_score = sum(scores.values()) * 100
            return {
                'score': round(total_score, 2),
                'status': 'healthy' if total_score > 80 else 'warning' if total_score > 50 else 'unhealthy',
                'metrics': scores
            }
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            return {'score': 0, 'status': 'unknown', 'metrics': {}}

    async def _get_recent_blocks(self, limit: int = 100) -> List[Dict]:
        """Get recent blocks"""
        try:
            latest = await self._get_latest_block_height()
            blocks = []
            for height in range(latest, latest - limit, -1):
                async with self.session.get(f"{self.base_url}/cosmos/base/tendermint/v1beta1/blocks/{height}") as response:
                    if response.status == 200:
                        data = await response.json()
                        blocks.append(data['block'])
            return blocks
        except Exception as e:
            logger.error(f"Error getting recent blocks: {str(e)}")
            return []

    async def get_status(self) -> Dict:
        """Get comprehensive network status"""
        return {
            'tps': await self.get_transactions_per_second(),
            'validators': await self.get_validator_metrics(),
            'blocks': await self.get_block_metrics(),
            'network_health': await self.get_network_health()
        }
        
    async def get_validator_metrics(self) -> Dict:
        """Get validator-related metrics"""
        return {
            'active_validators': await self.count_active_validators(),
            'total_stake': await self.get_total_stake(),
            'avg_block_time': await self.get_average_block_time()
        }

    async def get_network_health(self) -> Dict:
        """Calculate overall network health score"""
        metrics = {
            'uptime': await self.calculate_uptime(),
            'consensus': await self.get_consensus_status(),
            'peer_count': await self.get_peer_count()
        }
        return self.calculate_health_score(metrics) 