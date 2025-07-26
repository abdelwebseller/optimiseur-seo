#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimiseur de maillage interne SEO - Version corrigée
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
from typing import Dict, List, Tuple, Optional
import argparse
import warnings
warnings.filterwarnings('ignore')

class InternalLinkingOptimizer:
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model = model
        self.dimensions = None  # Sera défini dans process_urls si nécessaire
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SEO Optimizer/1.0)'
        }
        self.timeout = 30
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
            
            # Si pas trouvé, chercher par balise article
            if not article_content:
                article_content = soup.find('article')
            
            # Titre de la page
            title = ''
            # D'abord chercher dans le contenu de l'article
            if article_content:
                h1 = article_content.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
            
            # Sinon chercher un H1 global
            if not title:
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
            
            # Sinon utiliser le title de la page
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True).split(' - ')[0].split(' | ')[0]
            
            # En dernier recours, utiliser le titre de l'URL
            if not title:
                title = url_title
            
            # Si on a trouvé le contenu de l'article
            if article_content:
                # Supprimer les éléments non pertinents DANS l'article
                for elem in article_content.find_all(['script', 'style', 'noscript']):
                    elem.decompose()
                
                # Supprimer les éléments de partage social, commentaires, etc.
                for elem in article_content.find_all(class_=re.compile(r'share|social|comment|related|author-bio|tags|categories')):
                    elem.decompose()
                
                # Extraire le texte
                paragraphs = article_content.find_all(['p', 'li', 'h2', 'h3', 'h4'])
                text_parts = []
                
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 20:  # Ignorer les paragraphes trop courts
                        text_parts.append(text)
                
                content_text = ' '.join(text_parts)
                
                # Extraire les ingrédients et instructions si c'est une recette
                ingredients = []
                instructions = []
                
                # Chercher les ingrédients
                for elem in article_content.find_all(['ul', 'div'], class_=re.compile(r'ingredient|recipe-ingredient')):
                    for li in elem.find_all('li'):
                        ingredients.append(li.get_text(strip=True))
                
                # Chercher les instructions
                for elem in article_content.find_all(['ol', 'div'], class_=re.compile(r'instruction|direction|recipe-instruction')):
                    for li in elem.find_all('li'):
                        instructions.append(li.get_text(strip=True))
                
                # Ajouter les ingrédients et instructions au contenu
                if ingredients:
                    content_text += ' Ingrédients: ' + ' '.join(ingredients)
                if instructions:
                    content_text += ' Instructions: ' + ' '.join(instructions)
                
            else:
                # Fallback: extraire le body mais nettoyer agressivement
                self.logger.warning(f"Pas de contenu article trouvé pour {url}, extraction fallback")
                
                # Supprimer TOUT ce qui n'est pas le contenu principal
                for elem in soup.find_all(['header', 'nav', 'footer', 'aside', 'sidebar', 'script', 'style']):
                    elem.decompose()
                
                # Supprimer les éléments par classe
                classes_to_remove = [
                    'menu', 'widget', 'sidebar', 'nav', 'header', 'footer', 'breadcrumb',
                    'social', 'share', 'comments', 'related', 'author-box', 'newsletter',
                    'popup', 'modal', 'overlay', 'advertisement', 'ads', 'banner'
                ]
                for elem in soup.find_all(class_=re.compile('|'.join(classes_to_remove), re.I)):
                    elem.decompose()
                
                # Supprimer les éléments par ID
                for elem in soup.find_all(id=re.compile('|'.join(classes_to_remove), re.I)):
                    elem.decompose()
                
                # Supprimer les liens de navigation répétitifs
                for elem in soup.find_all('a', string=re.compile(r'^(Home|Accueil|Contact|Menu|Plus|Suivant|Précédent)$', re.I)):
                    elem.decompose()
                
                # Prendre le texte restant
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
            
        except Exception as e:
            self.logger.error(f"Erreur extraction {url}: {str(e)}")
            return None

    def get_embedding(self, text: str) -> List[float]:
        """Obtient l'embedding pour un texte."""
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
            
        except Exception as e:
            self.logger.error(f"Erreur embedding: {str(e)}")
            return None

    def calculate_similarity_matrix(self):
        """Calcule la matrice de similarité entre toutes les pages."""
        self.logger.info("Calcul de la matrice de similarité...")
        
        urls = list(self.embeddings.keys())
        n = len(urls)
        
        # Créer la matrice d'embeddings
        embeddings_matrix = []
        for url in urls:
            embeddings_matrix.append(self.embeddings[url])
        
        embeddings_matrix = np.array(embeddings_matrix)
        
        # Calculer la similarité cosinus
        similarity_matrix = cosine_similarity(embeddings_matrix)
        
        # Créer un dictionnaire pour accès facile
        self.similarity_scores = {}
        for i, url1 in enumerate(urls):
            self.similarity_scores[url1] = {}
            for j, url2 in enumerate(urls):
                if i != j:  # Ignorer la similarité avec soi-même
                    self.similarity_scores[url1][url2] = float(similarity_matrix[i][j])

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
        self.logger.info(f"Traitement de {len(urls)} URLs...")
        
        # Import pandas pour le DataFrame
        import pandas as pd
        
        # Listes pour créer le DataFrame
        processed_data = []
        
        # Si dimensions est spécifié, le stocker séparément
        self.dimensions = dimensions
        if dimensions:
            self.logger.info(f"Utilisation du modèle {self.model} avec dimensions réduites: {dimensions}")
        
        # Extraction du contenu
        for i, url in enumerate(urls, 1):
            self.logger.info(f"[{i}/{len(urls)}] Extraction: {url}")
            
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
            else:
                self.failed_urls.append(url)
            
            # Pause pour éviter la surcharge
            if i % 10 == 0:
                time.sleep(1)
        
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
