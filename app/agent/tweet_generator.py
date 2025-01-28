from typing import Dict, List
import random

class SEITweetGenerator:
    def __init__(self):
        self.engagement_phrases = [
            "🔥 Ser, have you seen this?",
            "👀 Anon, check this out",
            "💡 Quick alpha",
            "🚀 SEI is cooking",
        ]
        
    def generate_defi_update(self, protocol_data: Dict) -> str:
        templates = [
            "🌊 DragonSwap Update 🐉\n\n"
            "📊 24h Volume: ${volume}M\n"
            "🏊‍♂️ Top Pool APR: {apr}%\n"
            "💰 TVL: ${tvl}M\n\n"
            "Wen aping? 👀\n"
            "#SEI #DeFi",

            "🏦 YEI Finance Alert 📈\n\n"
            "💎 Lending APY: {lending_apy}%\n"
            "🔒 Total Locked: ${tvl}M\n"
            "🎯 New Features Soon™\n\n"
            "#SEI #DeFi"
        ]
        
        # Implementation details here
        return random.choice(templates).format(
            volume=protocol_data.get('volume', '??'),
            apr=protocol_data.get('apr', '??'),
            tvl=protocol_data.get('tvl', '??'),
            lending_apy=protocol_data.get('lending_apy', '??')
        )

    def generate_onboarding_tweet(self, user_handle: str) -> str:
        return (
            f"Hey {user_handle}! 👋\n\n"
            "Welcome to the SEI fam! Here's your starter pack:\n"
            "🔹 @DragonSwap_DEX for trading\n"
            "🔹 @SiloStake for staking\n"
            "🔹 @YEIFinance for lending\n\n"
            "Need help? Just ask! 🤝"
        ) 