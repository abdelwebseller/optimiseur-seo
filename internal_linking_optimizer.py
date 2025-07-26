#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimiseur de maillage interne SEO - Version optimisée avec parallélisation
"""

import os
import json
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, unquote
import openai
from datetime import datetime
import logging
import time
from pathlib import Path
import xml.etree.ElementTree as ET
import re
from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional, Callable
import argparse
import warnings
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
from tqdm import tqdm
warnings.filterwarnings('ignore')

class InternalLinkingOptimizer:
    def __init__(self, api_key: str, model: str = "text-embedding-3-small", 
                 max_concurrent_requests: int = 10, max_concurrent_embeddings: int = 5,
                 batch_size: int = 50, memory_limit_mb: int = 2048):
        self.api_key = api_key
        self.model = model
        self.dimensions = None  # Sera défini dans process_urls si nécessaire
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SEO Optimizer/1.0)'
        }
        self.timeout = 30
        self.max_retries = 3  # Nombre de tentatives pour les requêtes
        self.retry_delay = 2  # Délai entre les tentatives en secondes
        
        # Paramètres de parallélisation
        self.max_concurrent_requests = max_concurrent_requests
        self.max_concurrent_embeddings = max_concurrent_embeddings
        self.batch_size = batch_size
        self.memory_limit_mb = memory_limit_mb
        
        # Données de traitement
        self.pages_data = {}
        self.embeddings = {}
        self.failed_urls = []
        self.setup_logging()
        self.client = openai.OpenAI(api_key=api_key)
        
    def setup_logging(self):
        """Configure le logging."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f'seo_optimizer_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def extract_page_content(self, url):
        """Extrait UNIQUEMENT le contenu de l'article, pas le template."""
        # Vérifier que ce n'est pas une image
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico', '.tiff'}
        if any(url.lower().endswith(ext) for ext in image_extensions):
            self.logger.warning(f"URL ignorée (média): {url}")
            return None
            
        # Tentatives multiples avec retry
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraire le titre depuis l'URL si nécessaire
                url_slug = url.split('/')[-1]
                url_title = url_slug.replace('-', ' ').title()
                
                # STRATEGIE 1: Chercher le contenu de l'article spécifiquement
                article_content = None
                
                # Sélecteurs WordPress courants pour le contenu principal
                selectors = [
                    'article .entry-content',
                    'article .post-content',
                    'div.entry-content',
                    'div.post-content',
                    'main article .entry-content',
                    'main article .post-content',
                    'div.content-area article .entry-content',
                    '#content article .entry-content',
                    'article[itemtype*="Article"] .entry-content',
                    'article[itemtype*="BlogPosting"] .entry-content',
                    '.post-content',
                    '.article-content',
                    '.content-wrapper article',
                    'main .content',
                    '.post .entry-content',
                    '.hentry .entry-content'
                ]
                
                for selector in selectors:
                    article_content = soup.select_one(selector)
                    if article_content:
                        break
                
                # STRATEGIE 2: Si pas trouvé, chercher dans le body
                if not article_content:
                    # Chercher le contenu principal
                    main_selectors = [
                        'main',
                        '#main',
                        '.main',
                        '#content',
                        '.content',
                        'article',
                        '.post',
                        '.entry'
                    ]
                    
                    for selector in main_selectors:
                        article_content = soup.select_one(selector)
                        if article_content:
                            break
                
                # STRATEGIE 3: Fallback sur le body
                if not article_content:
                    article_content = soup.find('body')
                
                # Extraire le titre
                title = ""
                title_elem = soup.find('title')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                elif soup.find('h1'):
                    title = soup.find('h1').get_text(strip=True)
                else:
                    title = url_title
                
                # Extraire le contenu
                if article_content:
                    # Supprimer les éléments de navigation et footer
                    for elem in article_content.find_all(['nav', 'footer', 'aside', 'script', 'style']):
                        elem.decompose()
                    
                    content_text = article_content.get_text(separator=' ', strip=True)
                else:
                    content_text = soup.get_text(separator=' ', strip=True)
                
                # Nettoyer le contenu
                content_text = re.sub(r'\s+', ' ', content_text)
                content_text = content_text.strip()
                
                # Supprimer les phrases répétitives du template
                template_phrases = [
                    r'Aller au contenu principal',
                    r'Skip to content',
                    r'Rechercher:',
                    r'Search for:',
                    r'Menu principal',
                    r'Main menu',
                    r'Suivez-nous sur',
                    r'Follow us on',
                    r'Partager sur',
                    r'Share on',
                    r'Articles récents',
                    r'Recent posts',
                    r'Catégories',
                    r'Categories',
                    r'Archives',
                    r'Laisser un commentaire',
                    r'Leave a comment',
                    r'Votre adresse e-mail',
                    r'Your email',
                    r'Copyright \d{4}',
                    r'Tous droits réservés',
                    r'All rights reserved',
                    r'Propulsé par',
                    r'Powered by'
                ]
                
                for phrase in template_phrases:
                    content_text = re.sub(phrase, '', content_text, flags=re.IGNORECASE)
                
                # Limiter la longueur
                content_text = content_text[:2000]  # Réduire pour se concentrer sur l'essentiel
                
                # Vérification de longueur minimale
                word_count = len(content_text.split())
                if word_count < 20:
                    self.logger.warning(f"Contenu trop court pour {url}: {word_count} mots")
                    return None
                
                # IMPORTANT: Utiliser uniquement le contenu réel pour l'embedding
                # Ne pas répéter artificiellement des éléments
                combined = f"{title} {content_text}"
                
                return {
                    'url': url,
                    'title': title,
                    'content': content_text,
                    'word_count': word_count,
                    'combined': combined,
                    'url_slug': url_slug
                }
                
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout pour {url} (tentative {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"Timeout final pour {url}")
                    return None
                    
            except requests.exceptions.ConnectionError:
                self.logger.warning(f"Erreur de connexion pour {url} (tentative {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"Erreur de connexion finale pour {url}")
                    return None
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    self.logger.warning(f"Page 404: {url}")
                    return None
                elif e.response.status_code >= 500:
                    self.logger.warning(f"Erreur serveur {e.response.status_code} pour {url} (tentative {attempt + 1}/{self.max_retries})")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        self.logger.error(f"Erreur serveur finale pour {url}")
                        return None
                else:
                    self.logger.error(f"Erreur HTTP {e.response.status_code} pour {url}")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Erreur extraction {url}: {str(e)}")
                return None
        
        return None

    async def extract_page_content_async(self, session: aiohttp.ClientSession, url: str) -> Tuple[str, Optional[dict]]:
        """Extrait le contenu d'une page de manière asynchrone."""
        # Vérifier que ce n'est pas une image
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico', '.tiff'}
        if any(url.lower().endswith(ext) for ext in image_extensions):
            return url, None
            
        for attempt in range(self.max_retries):
            try:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extraire le titre depuis l'URL si nécessaire
                        url_slug = url.split('/')[-1]
                        url_title = url_slug.replace('-', ' ').title()
                        
                        # STRATEGIE 1: Chercher le contenu de l'article spécifiquement
                        article_content = None
                        
                        # Sélecteurs WordPress courants pour le contenu principal
                        selectors = [
                            'article .entry-content',
                            'article .post-content',
                            'div.entry-content',
                            'div.post-content',
                            'main article .entry-content',
                            'main article .post-content',
                            'div.content-area article .entry-content',
                            '#content article .entry-content',
                            'article[itemtype*="Article"] .entry-content',
                            'article[itemtype*="BlogPosting"] .entry-content',
                            '.post-content',
                            '.article-content',
                            '.content-wrapper article',
                            'main .content',
                            '.post .entry-content',
                        ]
                        
                        # Essayer les sélecteurs spécifiques
                        for selector in selectors:
                            content_elem = soup.select_one(selector)
                            if content_elem:
                                article_content = content_elem.get_text(strip=True)
                                break
                        
                        # STRATEGIE 2: Si pas trouvé, chercher le contenu principal
                        if not article_content:
                            main_selectors = [
                                'main',
                                'article',
                                '.content',
                                '.main-content',
                                '#content',
                                '.post',
                                '.entry'
                            ]
                            
                            for selector in main_selectors:
                                main_elem = soup.select_one(selector)
                                if main_elem:
                                    # Exclure les éléments de navigation et sidebar
                                    for elem in main_elem.find_all(['nav', 'aside', '.sidebar', '.navigation', 'header', 'footer']):
                                        elem.decompose()
                                    article_content = main_elem.get_text(strip=True)
                                    break
                        
                        # STRATEGIE 3: Dernier recours - tout le body
                        if not article_content:
                            body = soup.find('body')
                            if body:
                                # Nettoyer le body
                                for elem in body.find_all(['nav', 'aside', '.sidebar', '.navigation', 'header', 'footer', 'script', 'style']):
                                    elem.decompose()
                                article_content = body.get_text(strip=True)
                        
                        # Extraire le titre
                        title = ""
                        title_elem = soup.find('title')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                        elif soup.find('h1'):
                            title = soup.find('h1').get_text(strip=True)
                        else:
                            title = url_title
                        
                        # Nettoyer et limiter le contenu
                        if article_content:
                            # Supprimer les espaces multiples
                            article_content = re.sub(r'\s+', ' ', article_content)
                            # Limiter à 8000 caractères pour les embeddings
                            article_content = article_content[:8000]
                            
                            # Compter les mots
                            word_count = len(article_content.split())
                            
                            # Combiner titre et contenu pour l'embedding
                            combined = f"{title}\n\n{article_content}"
                            
                            return url, {
                                'title': title,
                                'content': article_content,
                                'combined': combined,
                                'word_count': word_count
                            }
                        
                        return url, None
                        
                    else:
                        self.logger.warning(f"HTTP {response.status} pour {url}")
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(self.retry_delay)
                            continue
                        return url, None
                        
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout pour {url} (tentative {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return url, None
                
            except Exception as e:
                self.logger.error(f"Erreur pour {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return url, None
        
        return url, None

    def get_embedding(self, text: str) -> List[float]:
        """Obtient l'embedding pour un texte avec gestion robuste des erreurs."""
        # Tentatives multiples avec retry pour les erreurs OpenAI
        for attempt in range(self.max_retries):
            try:
                # Limiter la taille du texte
                text = text[:8000]
                
                # Préparer les paramètres
                params = {
                    "model": self.model,
                    "input": text
                }
                
                # Ajouter les dimensions si spécifiées
                if hasattr(self, 'dimensions') and self.dimensions:
                    params["dimensions"] = self.dimensions
                
                response = self.client.embeddings.create(**params)
                return response.data[0].embedding
                
            except openai.RateLimitError:
                wait_time = min(60, self.retry_delay * (2 ** attempt))  # Backoff exponentiel, max 60s
                self.logger.warning(f"Rate limit OpenAI (tentative {attempt + 1}/{self.max_retries}) - Attente {wait_time}s")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error("Rate limit OpenAI final - Impossible de continuer")
                    raise Exception("Rate limit OpenAI atteint")
                    
            except openai.APIError as e:
                wait_time = self.retry_delay * (attempt + 1)
                self.logger.warning(f"Erreur API OpenAI (tentative {attempt + 1}/{self.max_retries}): {str(e)} - Attente {wait_time}s")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error(f"Erreur API OpenAI finale: {str(e)}")
                    raise Exception(f"Erreur API OpenAI: {str(e)}")
                    
            except openai.AuthenticationError:
                self.logger.error("Erreur d'authentification OpenAI - Vérifiez votre clé API")
                raise Exception("Clé API OpenAI invalide")
                
            except openai.APITimeoutError:
                wait_time = self.retry_delay * (attempt + 1)
                self.logger.warning(f"Timeout OpenAI (tentative {attempt + 1}/{self.max_retries}) - Attente {wait_time}s")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error("Timeout OpenAI final")
                    raise Exception("Timeout OpenAI")
                    
            except Exception as e:
                self.logger.error(f"Erreur embedding inattendue: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception(f"Erreur embedding: {str(e)}")
        
        return None

    def get_embedding_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Obtient les embeddings pour une liste de textes en parallèle avec gestion d'erreurs améliorée."""
        embeddings = []
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_embeddings) as executor:
            # Soumettre toutes les tâches
            future_to_text = {executor.submit(self.get_embedding, text): text for text in texts}
            
            # Collecter les résultats
            for future in as_completed(future_to_text):
                try:
                    embedding = future.result()
                    embeddings.append(embedding)
                except Exception as e:
                    failed_count += 1
                    self.logger.error(f"Erreur embedding dans le batch: {str(e)}")
                    embeddings.append(None)
                    
                    # Si trop d'échecs, arrêter le traitement
                    if failed_count > len(texts) * 0.3:  # Plus de 30% d'échecs
                        self.logger.error(f"Trop d'échecs d'embeddings ({failed_count}/{len(texts)}). Arrêt du traitement.")
                        # Annuler les tâches restantes
                        for f in future_to_text:
                            f.cancel()
                        raise Exception(f"Trop d'échecs d'embeddings: {failed_count}/{len(texts)}")
        
        self.logger.info(f"Embeddings générés: {len([e for e in embeddings if e is not None])}/{len(texts)}")
        return embeddings

    def calculate_similarity_matrix(self):
        """Calcule la matrice de similarité entre toutes les pages."""
        self.logger.info("Calcul de la matrice de similarité...")
        
        urls = list(self.embeddings.keys())
        n = len(urls)
        
        # Vérifier qu'on a des embeddings valides
        if n == 0:
            self.logger.warning("Aucun embedding disponible pour le calcul de similarité")
            self.similarity_scores = {}
            return
        
        if n == 1:
            self.logger.warning("Seulement une page avec embedding, pas de similarité possible")
            self.similarity_scores = {urls[0]: {}}
            return
        
        # Créer la matrice d'embeddings
        embeddings_matrix = []
        valid_urls = []
        
        for url in urls:
            embedding = self.embeddings[url]
            if embedding is not None and len(embedding) > 0:
                embeddings_matrix.append(embedding)
                valid_urls.append(url)
        
        # Vérifier qu'on a des embeddings valides
        if len(embeddings_matrix) == 0:
            self.logger.error("Aucun embedding valide trouvé")
            self.similarity_scores = {}
            return
        
        if len(embeddings_matrix) == 1:
            self.logger.warning("Seulement un embedding valide, pas de similarité possible")
            self.similarity_scores = {valid_urls[0]: {}}
            return
        
        # Convertir en array numpy
        embeddings_matrix = np.array(embeddings_matrix)
        
        # Vérifier la forme de la matrice
        if embeddings_matrix.ndim == 1:
            embeddings_matrix = embeddings_matrix.reshape(1, -1)
        
        # Calculer la similarité cosinus
        try:
            similarity_matrix = cosine_similarity(embeddings_matrix)
            
            # Créer un dictionnaire pour accès facile
            self.similarity_scores = {}
            for i, url1 in enumerate(valid_urls):
                self.similarity_scores[url1] = {}
                for j, url2 in enumerate(valid_urls):
                    if i != j:  # Ignorer la similarité avec soi-même
                        self.similarity_scores[url1][url2] = float(similarity_matrix[i][j])
            
            self.logger.info(f"Matrice de similarité calculée pour {len(valid_urls)} pages")
            
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul de similarité: {str(e)}")
            self.similarity_scores = {}

    def generate_smart_anchor(self, source_url: str, target_url: str, target_data: dict) -> str:
        """Génère une ancre intelligente universelle basée sur le contenu et le contexte."""
        target_title = target_data.get('title', '')
        target_content = target_data.get('content', '')
        
        # Si pas de titre, utiliser le slug
        if not target_title:
            slug = target_url.split('/')[-1]
            target_title = slug.replace('-', ' ').replace('_', ' ')
        
        # Nettoyer le titre du nom du site et des séparateurs communs
        for separator in [' - ', ' | ', ' :: ', ' » ', ' — ']:
            if separator in target_title:
                target_title = target_title.split(separator)[0]
        
        # Définir title_lower pour toutes les comparaisons
        title_lower = target_title.lower()
        
        # Liste universelle de préfixes à supprimer (multi-domaines)
        generic_prefixes = [
            # Français
            'la recette de', 'la recette du', 'la recette des',
            'comment faire', 'comment préparer', 'comment créer',
            'guide pour', 'guide de', 'guide du', 'guide complet',
            'tout savoir sur', 'tout sur', 'découvrez',
            'les meilleurs', 'les meilleures', 'le meilleur', 'la meilleure',
            'top des', 'top 10 des', 'top 5 des',
            # Anglais (si site multilingue)
            'how to', 'guide to', 'the best', 'everything about',
            'the ultimate', 'complete guide to',
            # Génériques
            'tutoriel', 'tutorial', 'article sur', 'post about'
        ]
        
        # Supprimer les préfixes génériques
        for prefix in generic_prefixes:
            if title_lower.startswith(prefix):
                target_title = target_title[len(prefix):].strip()
                title_lower = target_title.lower()
                break
        
        # Analyser le contenu pour identifier le type et extraire les mots-clés
        content_lower = target_content.lower()[:1000] if target_content else ''
        
        # Détecter le type de contenu et adapter l'ancre
        content_keywords = []
        
        # Extraire les mots importants du titre
        title_words = target_title.split()
        
        # Filtrer les mots vides universels
        stop_words = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'à', 'au', 'aux',
            'ce', 'ces', 'cet', 'cette', 'pour', 'par', 'sur', 'sous', 'dans', 'avec', 'sans',
            'qui', 'que', 'quoi', 'dont', 'où', 'est', 'sont', 'être', 'avoir',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'is', 'are', 'was', 'were', 'be', 'been', 'being'
        }
        
        # Garder les mots significatifs
        meaningful_words = []
        for word in title_words:
            if len(word) > 2 and word.lower() not in stop_words:
                meaningful_words.append(word)
        
        # Si on a assez de mots significatifs, les utiliser
        if len(meaningful_words) >= 2:
            # Prendre entre 2 et 5 mots significatifs
            target_title = ' '.join(meaningful_words[:5])
        elif meaningful_words:
            # Si on a peu de mots, essayer d'en extraire du contenu
            if content_lower:
                # Chercher des mots-clés importants dans le contenu
                # Rechercher des noms propres ou termes techniques (commencent par majuscule)
                content_sentences = target_content.split('.')[:5]
                for sentence in content_sentences:
                    words_in_sentence = sentence.split()
                    for word in words_in_sentence:
                        if len(word) > 4 and word[0].isupper() and word.lower() not in stop_words:
                            content_keywords.append(word)
                
                # Combiner avec les mots du titre
                if content_keywords:
                    all_keywords = meaningful_words + content_keywords[:2]
                    target_title = ' '.join(all_keywords[:4])
                else:
                    target_title = ' '.join(meaningful_words)
        
        # Assurer une longueur appropriée (2-6 mots)
        words = target_title.split()
        if len(words) > 6:
            target_title = ' '.join(words[:6])
        elif len(words) < 2:
            # Dernier recours : utiliser le slug nettoyé
            slug = target_url.split('/')[-1].split('?')[0].split('#')[0]
            slug_words = slug.replace('-', ' ').replace('_', ' ').split()
            # Filtrer les mots vides du slug aussi
            slug_meaningful = [w for w in slug_words if len(w) > 2 and w.lower() not in stop_words]
            if slug_meaningful:
                target_title = ' '.join(slug_meaningful[:4])
            else:
                target_title = ' '.join(slug_words[:3])
        
        # Capitalisation intelligente
        if target_title:
            words = target_title.split()
            capitalized = []
            for i, word in enumerate(words):
                # Toujours capitaliser le premier mot et les mots importants (>3 lettres)
                if i == 0 or len(word) > 3:
                    # Préserver les acronymes (tout en majuscules)
                    if word.isupper() and len(word) <= 4:
                        capitalized.append(word)
                    else:
                        capitalized.append(word.capitalize())
                else:
                    capitalized.append(word.lower())
            target_title = ' '.join(capitalized)
        
        # Validation finale
        if not target_title or len(target_title) < 3:
            # Vraiment le dernier recours
            target_title = "Voir Plus"  # Au moins ce sera explicite
        
        return target_title

    def find_relevant_links(self, min_similarity: float = 0.5, max_links: int = 5):
        """Trouve les liens pertinents avec un algorithme amélioré."""
        self.logger.info(f"Recherche de liens pertinents (seuil: {min_similarity})...")
        
        # Vérifier qu'on a des données de similarité
        if not self.similarity_scores:
            self.logger.warning("Aucune donnée de similarité disponible")
            return {}
        
        recommendations = {}
        
        for source_url, source_scores in self.similarity_scores.items():
            # Trier par score de similarité
            sorted_targets = sorted(
                source_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # NOUVEAU: Analyse de la distribution des scores
            scores_only = [score for _, score in sorted_targets]
            if scores_only:
                # Calculer l'écart-type
                mean_score = np.mean(scores_only)
                std_score = np.std(scores_only)
                
                # Si tous les scores sont très proches (std < 0.01), 
                # utiliser une approche différente
                if std_score < 0.01:
                    self.logger.info(f"Scores très proches pour {source_url}, utilisation de critères alternatifs")
                    
                    # Privilégier la diversité thématique
                    selected_links = []
                    used_slugs = set()
                    
                    for target_url, score in sorted_targets[:50]:  # Examiner plus de candidats
                        if target_url == source_url:
                            continue
                        
                        target_slug = target_url.split('/')[-1]
                        
                        # Éviter les pages trop similaires (même début de slug)
                        slug_prefix = target_slug.split('-')[0]
                        if slug_prefix not in used_slugs:
                            selected_links.append({
                                'target_url': target_url,
                                'target_title': self.pages_data.get(target_url, {}).get('title', ''),
                                'similarity_score': score,
                                'anchor_text': self.generate_smart_anchor(
                                    source_url, 
                                    target_url,
                                    self.pages_data.get(target_url, {})
                                )
                            })
                            used_slugs.add(slug_prefix)
                            
                            if len(selected_links) >= max_links:
                                break
                    
                    recommendations[source_url] = {
                        'source_title': self.pages_data.get(source_url, {}).get('title', ''),
                        'recommended_links': selected_links
                    }
                else:
                    # Approche normale: prendre les meilleurs scores
                    selected_links = []
                    
                    for target_url, score in sorted_targets:
                        if target_url == source_url:
                            continue
                            
                        if score >= min_similarity:
                            selected_links.append({
                                'target_url': target_url,
                                'target_title': self.pages_data.get(target_url, {}).get('title', ''),
                                'similarity_score': score,
                                'anchor_text': self.generate_smart_anchor(
                                    source_url,
                                    target_url, 
                                    self.pages_data.get(target_url, {})
                                )
                            })
                            
                            if len(selected_links) >= max_links:
                                break
                    
                    if selected_links:
                        recommendations[source_url] = {
                            'source_title': self.pages_data.get(source_url, {}).get('title', ''),
                            'recommended_links': selected_links
                        }
        
        return recommendations

    def extract_urls_from_sitemap(self, sitemap_path: str) -> List[str]:
        """Extrait les URLs depuis un sitemap."""
        urls = []
        # Extensions d'images à ignorer
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico', '.tiff'}
        
        try:
            if sitemap_path.startswith('http'):
                response = requests.get(sitemap_path, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                root = ET.fromstring(response.content)
            else:
                tree = ET.parse(sitemap_path)
                root = tree.getroot()
            
            # Obtenir le namespace
            namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                        'image': 'http://www.google.com/schemas/sitemap-image/1.1'}
            
            # Chercher uniquement les balises <loc> directes (pas image:loc)
            for elem in root.iter():
                # Vérifier que c'est une balise loc et pas image:loc
                if elem.tag.endswith('loc') and not elem.tag.endswith('image:loc'):
                    url = elem.text
                    # Vérifier que ce n'est pas une image
                    if url and not any(url.lower().endswith(ext) for ext in image_extensions):
                        urls.append(url)
            
            self.logger.info(f"URLs trouvées dans le sitemap (sans images): {len(urls)}")
            return urls
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du sitemap: {str(e)}")
            return []
    
    def crawl_website(self, start_url: str, max_pages: int = 50) -> List[str]:
        """Crawl un site web pour trouver des URLs."""
        self.logger.info(f"Démarrage du crawl depuis: {start_url}")
        
        visited = set()
        to_visit = [start_url]
        found_urls = []
        
        domain = urlparse(start_url).netloc.lower()
        
        while to_visit and len(found_urls) < max_pages:
            current_url = to_visit.pop(0)
            
            if current_url in visited:
                continue
            
            visited.add(current_url)
            
            try:
                response = requests.get(current_url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                found_urls.append(current_url)
                
                # Trouver tous les liens
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    parsed = urlparse(full_url)
                    
                    # Vérifier que c'est le même domaine
                    if parsed.netloc.lower() == domain and full_url not in visited:
                        to_visit.append(full_url)
                
            except Exception as e:
                self.logger.warning(f"Erreur lors du crawl de {current_url}: {str(e)}")
        
        self.logger.info(f"Crawl terminé. {len(found_urls)} pages trouvées")
        return found_urls

    def process_urls(self, urls: List[str], dimensions: int = None):
        """Traite une liste d'URLs."""
        return self.process_urls_with_progress(urls, dimensions=dimensions)
    
    async def process_urls_async(self, urls: List[str], dimensions: int = None, progress_callback=None) -> 'pd.DataFrame':
        """Traite une liste d'URLs de manière asynchrone avec parallélisation."""
        import pandas as pd
        
        self.logger.info(f"Traitement asynchrone de {len(urls)} URLs...")
        
        # Vérifier la mémoire
        memory_info = self.check_memory_usage()
        self.logger.info(f"Mémoire disponible: {memory_info.get('available_mb', 'N/A')} MB")
        
        # Estimer le temps de traitement
        time_estimate = self.estimate_processing_time(len(urls))
        self.logger.info(f"Temps estimé: {time_estimate['formatted']}")
        
        # Si dimensions est spécifié, le stocker
        self.dimensions = dimensions
        if dimensions:
            self.logger.info(f"Utilisation du modèle {self.model} avec dimensions réduites: {dimensions}")
        
        # Traitement par batch
        all_processed_data = []
        total_batches = (len(urls) + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(urls))
            batch_urls = urls[start_idx:end_idx]
            
            self.logger.info(f"Traitement du batch {batch_num + 1}/{total_batches} ({len(batch_urls)} URLs)")
            
            # Mettre à jour la progression
            if progress_callback:
                progress_percent = 10 + int((batch_num / total_batches) * 70)
                progress_callback(progress_percent, 100, f"Batch {batch_num + 1}/{total_batches}")
            
            # Extraction asynchrone du contenu
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=self.max_concurrent_requests),
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as session:
                # Créer les tâches d'extraction
                tasks = [self.extract_page_content_async(session, url) for url in batch_urls]
                
                # Exécuter en parallèle
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Traiter les résultats
                batch_data = []
                texts_for_embedding = []
                urls_for_embedding = []
                
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        self.logger.error(f"Erreur extraction {batch_urls[i]}: {str(result)}")
                        self.failed_urls.append(batch_urls[i])
                        continue
                    
                    url, content = result
                    if content:
                        self.pages_data[url] = content
                        texts_for_embedding.append(content['combined'])
                        urls_for_embedding.append(url)
                        batch_data.append({
                            'url': url,
                            'title': content.get('title', ''),
                            'content': content.get('content', '')[:500],
                            'word_count': content.get('word_count', 0)
                        })
                    else:
                        self.failed_urls.append(url)
                
                # Obtenir les embeddings en parallèle
                if texts_for_embedding:
                    self.logger.info(f"Génération des embeddings pour {len(texts_for_embedding)} pages...")
                    try:
                        embeddings = self.get_embedding_batch(texts_for_embedding)
                        
                        # Associer les embeddings aux URLs
                        for i, (url, embedding) in enumerate(zip(urls_for_embedding, embeddings)):
                            if embedding:
                                self.embeddings[url] = embedding
                                batch_data[i]['embedding'] = embedding
                            else:
                                self.failed_urls.append(url)
                                batch_data[i]['embedding'] = None
                                
                    except Exception as e:
                        self.logger.error(f"Erreur critique lors de la génération des embeddings: {str(e)}")
                        # Marquer toutes les URLs du batch comme échouées
                        for url in batch_urls:
                            if url not in self.failed_urls:
                                self.failed_urls.append(url)
                        
                        # Si c'est un problème de rate limit, faire une pause plus longue
                        if "rate limit" in str(e).lower():
                            self.logger.warning("Rate limit détecté - Pause de 60 secondes...")
                            await asyncio.sleep(60)
                        elif "timeout" in str(e).lower():
                            self.logger.warning("Timeout détecté - Pause de 30 secondes...")
                            await asyncio.sleep(30)
                        else:
                            # Pour les autres erreurs, pause courte
                            await asyncio.sleep(10)
                
                all_processed_data.extend(batch_data)
                
                # Pause entre les batches pour éviter la surcharge
                if batch_num < total_batches - 1:
                    await asyncio.sleep(2)
        
        self.logger.info(f"Pages traitées: {len(self.pages_data)}")
        self.logger.info(f"Échecs: {len(self.failed_urls)}")
        
        # Créer et retourner le DataFrame
        if all_processed_data:
            df = pd.DataFrame(all_processed_data)
            return df
        else:
            return pd.DataFrame()
    
    def process_urls_with_progress(self, urls: List[str], dimensions: int = None, progress_callback=None):
        """Wrapper synchrone pour la méthode asynchrone."""
        # Vérifier si on peut utiliser la version asynchrone
        if len(urls) > 10:  # Utiliser l'async pour les gros volumes
            try:
                # Créer un nouvel event loop si nécessaire
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                return loop.run_until_complete(
                    self.process_urls_async(urls, dimensions, progress_callback)
                )
            except Exception as e:
                self.logger.warning(f"Échec de la version asynchrone, utilisation de la version synchrone: {e}")
                return self._process_urls_sync(urls, dimensions, progress_callback)
        else:
            # Utiliser la version synchrone pour les petits volumes
            return self._process_urls_sync(urls, dimensions, progress_callback)
    
    def _process_urls_sync(self, urls: List[str], dimensions: int = None, progress_callback=None):
        """Version synchrone originale pour les petits volumes."""
        import pandas as pd
        
        self.logger.info(f"Traitement synchrone de {len(urls)} URLs...")
        
        # Si dimensions est spécifié, le stocker séparément
        self.dimensions = dimensions
        if dimensions:
            self.logger.info(f"Utilisation du modèle {self.model} avec dimensions réduites: {dimensions}")
        
        # Listes pour créer le DataFrame
        processed_data = []
        
        # Extraction du contenu
        for i, url in enumerate(urls, 1):
            try:
                self.logger.info(f"[{i}/{len(urls)}] Extraction: {url}")
                
                # Mettre à jour la progression
                if progress_callback:
                    progress_percent = 10 + int((i / len(urls)) * 70)  # 10% à 80%
                    progress_callback(progress_percent, 100, f"Traitement des pages ({i}/{len(urls)})")
                
                content = self.extract_page_content(url)
                if content:
                    self.pages_data[url] = content
                    
                    # Obtenir l'embedding
                    embedding = self.get_embedding(content['combined'])
                    if embedding:
                        self.embeddings[url] = embedding
                        
                        # Ajouter aux données pour le DataFrame
                        processed_data.append({
                            'url': url,
                            'title': content.get('title', ''),
                            'content': content.get('content', '')[:500],  # Limiter pour l'affichage
                            'word_count': content.get('word_count', 0),
                            'embedding': embedding
                        })
                    else:
                        self.failed_urls.append(url)
                        self.logger.warning(f"Échec embedding pour {url}")
                else:
                    self.failed_urls.append(url)
                    self.logger.warning(f"Échec extraction pour {url}")
                
                # Pause intelligente pour éviter la surcharge
                if i % 5 == 0:  # Pause toutes les 5 URLs
                    time.sleep(1)
                elif i % 20 == 0:  # Pause plus longue toutes les 20 URLs
                    time.sleep(3)
                    
            except Exception as e:
                self.logger.error(f"Erreur lors du traitement de {url}: {str(e)}")
                self.failed_urls.append(url)
                continue
        
        self.logger.info(f"Pages traitées: {len(self.pages_data)}")
        self.logger.info(f"Échecs: {len(self.failed_urls)}")
        
        # Créer et retourner le DataFrame
        if processed_data:
            df = pd.DataFrame(processed_data)
            return df
        else:
            return pd.DataFrame()  # DataFrame vide si aucune donnée

    def save_results(self, recommendations: dict, output_dir: str = "output"):
        """Sauvegarde les résultats."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Générer un nom unique si le fichier est verrouillé
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = "internal_linking_recommendations"
        
        # JSON
        json_path = output_path / f"{base_name}.json"
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(recommendations, f, ensure_ascii=False, indent=2)
        except PermissionError:
            json_path = output_path / f"{base_name}_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(recommendations, f, ensure_ascii=False, indent=2)
            self.logger.warning(f"Fichier JSON verrouillé, sauvegardé sous: {json_path}")
        
        # CSV
        csv_path = output_path / f"{base_name}.csv"
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Source URL', 'Source Title', 'Target URL', 'Target Title', 
                               'Anchor Text', 'Similarity Score'])
                
                for source_url, data in recommendations.items():
                    for link in data['recommended_links']:
                        writer.writerow([
                            source_url,
                            data['source_title'],
                            link['target_url'],
                            link['target_title'],
                            link['anchor_text'],
                            f"{link['similarity_score']:.2%}"
                        ])
        except PermissionError:
            csv_path = output_path / f"{base_name}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Source URL', 'Source Title', 'Target URL', 'Target Title', 
                               'Anchor Text', 'Similarity Score'])
                
                for source_url, data in recommendations.items():
                    for link in data['recommended_links']:
                        writer.writerow([
                            source_url,
                            data['source_title'],
                            link['target_url'],
                            link['target_title'],
                            link['anchor_text'],
                            f"{link['similarity_score']:.2%}"
                        ])
            self.logger.warning(f"Fichier CSV verrouillé, sauvegardé sous: {csv_path}")
        
        # HTML
        html_path = output_path / f"{base_name}.html"
        try:
            self.generate_html_report(recommendations, html_path)
        except PermissionError:
            html_path = output_path / f"{base_name}_{timestamp}.html"
            self.generate_html_report(recommendations, html_path)
            self.logger.warning(f"Fichier HTML verrouillé, sauvegardé sous: {html_path}")
        
        # URLs échouées
        if self.failed_urls:
            failed_path = output_path / "failed_urls.txt"
            with open(failed_path, 'w', encoding='utf-8') as f:
                for url in self.failed_urls:
                    f.write(f"{url}\n")
        
        self.logger.info(f"Résultats sauvegardés dans {output_path}")

    def generate_html_report(self, recommendations: dict, output_path: Path):
        """Génère un rapport HTML."""
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport de Maillage Interne</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .page-card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .page-title { font-size: 1.2em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .page-url { font-size: 0.9em; color: #666; margin-bottom: 15px; }
        .link-item { background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 5px; border-left: 3px solid #007bff; }
        .anchor-text { font-weight: bold; color: #007bff; }
        .similarity-score { float: right; background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2em; font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rapport de Maillage Interne SEO</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">""" + str(len(recommendations)) + """</div>
                <div>Pages analysées</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(sum(len(d['recommended_links']) for d in recommendations.values())) + """</div>
                <div>Liens recommandés</div>
            </div>
        </div>
"""
        
        for source_url, data in recommendations.items():
            html += f"""
        <div class="page-card">
            <div class="page-title">{data['source_title'] or 'Sans titre'}</div>
            <div class="page-url">{source_url}</div>
            <h3>Liens recommandés :</h3>
"""
            
            for link in data['recommended_links']:
                score_pct = link['similarity_score'] * 100
                html += f"""
            <div class="link-item">
                <span class="similarity-score">{score_pct:.1f}%</span>
                <div class="anchor-text">→ {link['anchor_text']}</div>
                <div style="font-size: 0.85em; color: #666;">{link['target_url']}</div>
            </div>
"""
            
            html += """
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def test_openai_connection(self) -> bool:
        """Teste la connexion OpenAI avant de commencer l'analyse."""
        try:
            self.logger.info("Test de connexion OpenAI...")
            
            # Test simple avec un petit texte
            response = self.client.embeddings.create(
                model=self.model,
                input="test de connexion"
            )
            
            if response and response.data and len(response.data[0].embedding) > 0:
                self.logger.info("✅ Connexion OpenAI OK")
                return True
            else:
                self.logger.error("❌ Réponse OpenAI invalide")
                return False
                
        except openai.AuthenticationError:
            self.logger.error("❌ Erreur d'authentification OpenAI")
            return False
        except openai.RateLimitError:
            self.logger.error("❌ Rate limit OpenAI atteint")
            return False
        except openai.APIError as e:
            self.logger.error(f"❌ Erreur API OpenAI: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Erreur de connexion OpenAI: {str(e)}")
            return False

    def check_memory_usage(self) -> dict:
        """Vérifie l'utilisation mémoire et retourne les statistiques."""
        try:
            memory = psutil.virtual_memory()
            return {
                'total_mb': memory.total // (1024 * 1024),
                'available_mb': memory.available // (1024 * 1024),
                'used_mb': memory.used // (1024 * 1024),
                'percent': memory.percent,
                'is_safe': memory.percent < 85
            }
        except Exception as e:
            self.logger.warning(f"Impossible de vérifier la mémoire: {e}")
            return {'is_safe': True}  # Par défaut, considérer comme sûr
    
    def estimate_processing_time(self, num_urls: int) -> dict:
        """Estime le temps de traitement basé sur le nombre d'URLs."""
        # Estimations basées sur les tests (en secondes)
        extraction_time_per_url = 2.0  # Extraction + parsing
        embedding_time_per_url = 1.5   # Appel API OpenAI
        similarity_time = 0.1 * num_urls  # Calcul matriciel
        
        total_seconds = (extraction_time_per_url + embedding_time_per_url) * num_urls + similarity_time
        
        # Ajuster pour la parallélisation
        if num_urls <= 50:
            parallel_factor = 0.6  # 40% de gain
        elif num_urls <= 200:
            parallel_factor = 0.5  # 50% de gain
        else:
            parallel_factor = 0.4  # 60% de gain
        
        estimated_seconds = total_seconds * parallel_factor
        
        return {
            'seconds': estimated_seconds,
            'minutes': estimated_seconds / 60,
            'hours': estimated_seconds / 3600,
            'formatted': self._format_time(estimated_seconds)
        }
    
    def _format_time(self, seconds: float) -> str:
        """Formate le temps en format lisible."""
        if seconds < 60:
            return f"{seconds:.1f} secondes"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        else:
            return f"{seconds/3600:.1f} heures"

def main():
    parser = argparse.ArgumentParser(description='Optimiseur de maillage interne SEO')
    parser.add_argument('url', help='URL ou fichier sitemap')
    parser.add_argument('--min-similarity', type=float, default=0.5,
                       help='Score de similarité minimum (0.0-1.0)')
    parser.add_argument('--max-links', type=int, default=5,
                       help='Nombre maximum de liens par page')
    parser.add_argument('--sitemap', action='store_true',
                       help='Utiliser un sitemap au lieu du crawl')
    
    args = parser.parse_args()
    
    # Clé API
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Erreur: OPENAI_API_KEY non définie")
        return
    
    optimizer = InternalLinkingOptimizer(api_key)
    
    # Tester la connexion OpenAI
    if not optimizer.test_openai_connection():
        print("Erreur: Impossible de se connecter à l'API OpenAI. Vérifiez votre clé API.")
        return

    # Obtenir les URLs
    if args.sitemap or args.url.endswith('.xml'):
        # Charger depuis sitemap
        urls = []
        if args.url.startswith('http'):
            response = requests.get(args.url)
            root = ET.fromstring(response.content)
        else:
            tree = ET.parse(args.url)
            root = tree.getroot()
        
        for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(loc.text)
        
        print(f"URLs trouvées dans le sitemap: {len(urls)}")
    else:
        print("Erreur: Utilisez --sitemap avec l'URL du sitemap")
        return
    
    # Traiter les URLs
    optimizer.process_urls(urls)
    
    # Calculer la similarité
    optimizer.calculate_similarity_matrix()
    
    # Trouver les liens
    recommendations = optimizer.find_relevant_links(
        min_similarity=args.min_similarity,
        max_links=args.max_links
    )
    
    # Sauvegarder
    optimizer.save_results(recommendations)
    
    print("\nAnalyse terminée!")

if __name__ == "__main__":
    main()
