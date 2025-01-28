class ProjectAnalyzer:
    async def analyze_project(self, project_name: str) -> Dict:
        """Comprehensive project analysis"""
        return {
            'metrics': await self.get_project_metrics(project_name),
            'community': await self.analyze_community_sentiment(),
            'technical': await self.analyze_technical_aspects(),
            'opportunities': await self.identify_growth_potential()
        }

    async def generate_project_spotlight(self) -> str:
        """Generate project spotlight content"""
        project = await self.select_project_for_spotlight()
        analysis = await self.analyze_project(project)
        return self.format_spotlight_content(analysis) 