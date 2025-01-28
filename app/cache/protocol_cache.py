from typing import Dict, Any
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ProtocolCache:
    """
    Cache system for protocol and NFT data to reduce API calls and server load.
    
    This cache implements a time-based invalidation strategy to ensure data freshness
    while minimizing external API calls. Different data types have different cache
    durations based on their update frequency needs.
    
    Attributes:
        nft_cache (Dict): Stores NFT collection data
        protocol_cache (Dict): Stores DeFi protocol metrics
        cache_durations (Dict): Defines how long each data type stays valid
    """
    
    def __init__(self):
        self.nft_cache: Dict[str, Dict[str, Any]] = {}
        self.protocol_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_durations = {
            'nft_stats': 300,  # 5 minutes for NFT stats
            'protocol_metrics': 60,  # 1 minute for protocol metrics
            'market_data': 120,  # 2 minutes for market data
        }
        self.logger = logging.getLogger(__name__)

    def get_cached_data(self, cache_type: str, key: str) -> Dict[str, Any]:
        """
        Retrieve cached data if it exists and is still valid.
        
        Args:
            cache_type: Type of cached data ('nft_stats', 'protocol_metrics', etc.)
            key: Identifier for the specific data entry
            
        Returns:
            Dict containing cached data or None if invalid/missing
        """
        cache = self._get_cache_for_type(cache_type)
        if not cache or key not in cache:
            return None
            
        cached_item = cache[key]
        if self._is_cache_valid(cached_item, cache_type):
            self.logger.debug(f"Cache hit for {cache_type}:{key}")
            return cached_item['data']
            
        self.logger.debug(f"Cache expired for {cache_type}:{key}")
        return None

    def set_cached_data(self, cache_type: str, key: str, data: Dict[str, Any]):
        """
        Store new data in the cache with current timestamp.
        
        Args:
            cache_type: Type of data being cached
            key: Identifier for the data entry
            data: The data to cache
        """
        cache = self._get_cache_for_type(cache_type)
        if cache is not None:
            cache[key] = {
                'timestamp': time.time(),
                'data': data
            }
            self.logger.debug(f"Updated cache for {cache_type}:{key}")

    def _get_cache_for_type(self, cache_type: str) -> Dict:
        """Map cache type to appropriate cache dictionary."""
        cache_map = {
            'nft_stats': self.nft_cache,
            'protocol_metrics': self.protocol_cache
        }
        return cache_map.get(cache_type)

    def _is_cache_valid(self, cached_item: Dict, cache_type: str) -> bool:
        """Check if cached item is still within its validity period."""
        if not cached_item:
            return False
            
        age = time.time() - cached_item['timestamp']
        return age < self.cache_durations.get(cache_type, 300)

    def clear_expired(self):
        """Remove expired entries from all caches."""
        for cache_type in self.cache_durations.keys():
            cache = self._get_cache_for_type(cache_type)
            if cache:
                expired = [
                    key for key, item in cache.items()
                    if not self._is_cache_valid(item, cache_type)
                ]
                for key in expired:
                    del cache[key]
                    self.logger.debug(f"Cleared expired cache for {cache_type}:{key}") 