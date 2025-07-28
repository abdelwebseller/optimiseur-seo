import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime, timedelta
import json

class CrawlService:
    def __init__(self):
        self.session = None
        self.crawl_stats = {}
    
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Semantra Bot 1.0'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    def get_real_time_stats(self, analysis_id: str) -> Dict[str, Any]:
        """Récupérer les statistiques en temps réel d'une analyse"""
        stats = self.crawl_stats.get(analysis_id, {})
        
        if not stats:
            return {
                "estimated_completion": None,
                "current_speed": "0 urls/min",
                "blocked_requests": 0,
                "retry_queue": 0
            }
        
        # Calculer la vitesse actuelle
        current_time = datetime.utcnow()
        if stats.get("start_time"):
            elapsed_minutes = (current_time - stats["start_time"]).total_seconds() / 60
            if elapsed_minutes > 0:
                current_speed = stats.get("crawled_urls", 0) / elapsed_minutes
                current_speed_str = f"{int(current_speed)} urls/min"
            else:
                current_speed_str = "0 urls/min"
        else:
            current_speed_str = "0 urls/min"
        
        # Estimer la fin
        estimated_completion = None
        if stats.get("total_urls") and stats.get("crawled_urls"):
            remaining_urls = stats["total_urls"] - stats["crawled_urls"]
            if current_speed_str != "0 urls/min":
                speed_per_minute = int(current_speed_str.split()[0])
                if speed_per_minute > 0:
                    remaining_minutes = remaining_urls / speed_per_minute
                    estimated_completion = current_time + timedelta(minutes=remaining_minutes)
        
        return {
            "estimated_completion": estimated_completion,
            "current_speed": current_speed_str,
            "blocked_requests": stats.get("blocked_requests", 0),
            "retry_queue": stats.get("retry_queue", 0)
        }
    
    async def crawl_sitemap(
        self,
        sitemap_url: str,
        analysis_id: str,
        crawl_settings: Dict[str, Any] = None
    ) -> List[str]:
        """Crawler un sitemap et extraire toutes les URLs"""
        if not self.session:
            raise RuntimeError("CrawlService must be used as async context manager")
        
        # Initialiser les statistiques
        self.crawl_stats[analysis_id] = {
            "start_time": datetime.utcnow(),
            "total_urls": 0,
            "crawled_urls": 0,
            "failed_urls": 0,
            "blocked_requests": 0,
            "retry_queue": 0
        }
        
        try:
            # Détecter le type de sitemap
            sitemap_type = await self._detect_sitemap_type(sitemap_url)
            
            # Extraire les URLs selon le type
            if sitemap_type == "xml":
                urls = await self._parse_xml_sitemap(sitemap_url)
            elif sitemap_type == "txt":
                urls = await self._parse_txt_sitemap(sitemap_url)
            else:
                urls = await self._parse_html_sitemap(sitemap_url)
            
            # Appliquer les filtres
            filtered_urls = self._apply_url_filters(urls, crawl_settings)
            
            # Mettre à jour les statistiques
            self.crawl_stats[analysis_id]["total_urls"] = len(filtered_urls)
            
            return filtered_urls
            
        except Exception as e:
            self.crawl_stats[analysis_id]["error"] = str(e)
            raise
    
    async def _detect_sitemap_type(self, sitemap_url: str) -> str:
        """Détecter le type de sitemap"""
        try:
            async with self.session.get(sitemap_url) as response:
                content_type = response.headers.get('content-type', '')
                
                if 'xml' in content_type or sitemap_url.endswith('.xml'):
                    return "xml"
                elif 'text/plain' in content_type or sitemap_url.endswith('.txt'):
                    return "txt"
                else:
                    return "html"
        except Exception:
            # Par défaut, essayer XML
            return "xml"
    
    async def _parse_xml_sitemap(self, sitemap_url: str) -> List[str]:
        """Parser un sitemap XML"""
        try:
            async with self.session.get(sitemap_url) as response:
                content = await response.text()
                
                # Extraction simple des URLs (pour l'exemple)
                # En production, utiliser une vraie parser XML
                urls = re.findall(r'<loc>(.*?)</loc>', content)
                return urls
        except Exception as e:
            raise Exception(f"Erreur lors du parsing du sitemap XML: {str(e)}")
    
    async def _parse_txt_sitemap(self, sitemap_url: str) -> List[str]:
        """Parser un sitemap TXT"""
        try:
            async with self.session.get(sitemap_url) as response:
                content = await response.text()
                
                # Chaque ligne est une URL
                urls = [line.strip() for line in content.split('\n') if line.strip()]
                return urls
        except Exception as e:
            raise Exception(f"Erreur lors du parsing du sitemap TXT: {str(e)}")
    
    async def _parse_html_sitemap(self, sitemap_url: str) -> List[str]:
        """Parser un sitemap HTML"""
        try:
            async with self.session.get(sitemap_url) as response:
                content = await response.text()
                
                # Extraction des liens (simplifié)
                urls = re.findall(r'href=["\'](.*?)["\']', content)
                return urls
        except Exception as e:
            raise Exception(f"Erreur lors du parsing du sitemap HTML: {str(e)}")
    
    def _apply_url_filters(
        self,
        urls: List[str],
        crawl_settings: Dict[str, Any] = None
    ) -> List[str]:
        """Appliquer les filtres d'URL"""
        if not crawl_settings:
            return urls
        
        filtered_urls = urls
        
        # Filtres par pattern
        if "url_patterns" in crawl_settings:
            patterns = crawl_settings["url_patterns"]
            filtered_urls = [
                url for url in filtered_urls
                if any(re.match(pattern, url) for pattern in patterns)
            ]
        
        # Filtres d'exclusion
        if "exclude_patterns" in crawl_settings:
            exclude_patterns = crawl_settings["exclude_patterns"]
            filtered_urls = [
                url for url in filtered_urls
                if not any(re.match(pattern, url) for pattern in exclude_patterns)
            ]
        
        # Filtres regex
        if "regex_filters" in crawl_settings:
            regex_filters = crawl_settings["regex_filters"]
            filtered_urls = [
                url for url in filtered_urls
                if any(re.match(regex, url) for regex in regex_filters)
            ]
        
        # Limite de sous-domaines
        if "subdomain_limits" in crawl_settings:
            subdomains = crawl_settings["subdomain_limits"]
            filtered_urls = [
                url for url in filtered_urls
                if any(subdomain in url for subdomain in subdomains)
            ]
        
        # Limite de dossiers
        if "folder_limits" in crawl_settings:
            folders = crawl_settings["folder_limits"]
            filtered_urls = [
                url for url in filtered_urls
                if any(folder in url for folder in folders)
            ]
        
        return filtered_urls
    
    async def crawl_pages(
        self,
        urls: List[str],
        analysis_id: str,
        crawl_settings: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Crawler les pages et extraire le contenu"""
        if not self.session:
            raise RuntimeError("CrawlService must be used as async context manager")
        
        crawl_settings = crawl_settings or {}
        delay = crawl_settings.get("delay_between_requests", 1000) / 1000  # Convertir en secondes
        max_urls = crawl_settings.get("max_urls", 1000000)
        user_agent = crawl_settings.get("user_agent", "Semantra Bot 1.0")
        
        # Limiter le nombre d'URLs
        urls = urls[:max_urls]
        
        crawled_pages = []
        
        for i, url in enumerate(urls):
            try:
                # Mettre à jour les statistiques
                self.crawl_stats[analysis_id]["crawled_urls"] = i + 1
                
                # Crawler la page
                page_data = await self._crawl_single_page(url, user_agent)
                if page_data:
                    crawled_pages.append(page_data)
                
                # Délai entre les requêtes
                if delay > 0:
                    await asyncio.sleep(delay)
                
            except Exception as e:
                self.crawl_stats[analysis_id]["failed_urls"] += 1
                print(f"Erreur lors du crawl de {url}: {str(e)}")
        
        return crawled_pages
    
    async def _crawl_single_page(
        self,
        url: str,
        user_agent: str
    ) -> Optional[Dict[str, Any]]:
        """Crawler une seule page"""
        try:
            headers = {'User-Agent': user_agent}
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Extraire les métadonnées
                    title = self._extract_title(content)
                    description = self._extract_description(content)
                    headings = self._extract_headings(content)
                    
                    return {
                        "url": url,
                        "title": title,
                        "description": description,
                        "headings": headings,
                        "content": content,
                        "status_code": response.status
                    }
                else:
                    return None
                    
        except Exception as e:
            print(f"Erreur lors du crawl de {url}: {str(e)}")
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extraire le titre de la page"""
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_description(self, content: str) -> str:
        """Extraire la description de la page"""
        match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_headings(self, content: str) -> List[str]:
        """Extraire les titres de la page"""
        headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', content, re.IGNORECASE)
        return [heading.strip() for heading in headings] 