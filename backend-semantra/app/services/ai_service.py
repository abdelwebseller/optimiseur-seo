import openai
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
from app.core.config import settings

class AIService:
    def __init__(self):
        # Configuration OpenAI
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
        # Configuration Gemini
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
    
    async def generate_embeddings(
        self,
        pages: List[Dict[str, Any]],
        model: str = "text-embedding-3-large"
    ) -> List[Dict[str, Any]]:
        """Générer les embeddings pour les pages"""
        embeddings = []
        
        for page in pages:
            try:
                # Préparer le texte pour l'embedding
                text_content = self._prepare_text_for_embedding(page)
                
                # Générer l'embedding
                embedding = await self._generate_single_embedding(text_content, model)
                
                embeddings.append({
                    "url": page["url"],
                    "embedding": embedding,
                    "text_content": text_content
                })
                
            except Exception as e:
                print(f"Erreur lors de la génération d'embedding pour {page['url']}: {str(e)}")
                continue
        
        return embeddings
    
    async def _generate_single_embedding(
        self,
        text: str,
        model: str
    ) -> List[float]:
        """Générer un embedding pour un texte"""
        try:
            response = openai.Embedding.create(
                input=text,
                model=model
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Erreur OpenAI: {str(e)}")
            # Retourner un embedding vide en cas d'erreur
            return [0.0] * 1536  # Dimension par défaut
    
    def _prepare_text_for_embedding(self, page: Dict[str, Any]) -> str:
        """Préparer le texte pour l'embedding"""
        text_parts = []
        
        # Titre
        if page.get("title"):
            text_parts.append(f"Titre: {page['title']}")
        
        # Description
        if page.get("description"):
            text_parts.append(f"Description: {page['description']}")
        
        # Titres (H1, H2, etc.)
        if page.get("headings"):
            headings_text = " ".join(page["headings"])
            text_parts.append(f"Titres: {headings_text}")
        
        # Contenu (limité pour éviter les tokens excessifs)
        if page.get("content"):
            # Nettoyer le HTML et limiter la longueur
            clean_content = self._clean_html_content(page["content"])
            text_parts.append(f"Contenu: {clean_content[:2000]}")  # Limiter à 2000 caractères
        
        return " ".join(text_parts)
    
    def _clean_html_content(self, html_content: str) -> str:
        """Nettoyer le contenu HTML"""
        import re
        
        # Supprimer les balises HTML
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        
        # Supprimer les espaces multiples
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        # Supprimer les caractères spéciaux
        clean_text = re.sub(r'[^\w\s\-.,!?;:]', '', clean_text)
        
        return clean_text.strip()
    
    async def analyze_similarities(
        self,
        pages: List[Dict[str, Any]],
        embeddings: List[Dict[str, Any]],
        ai_settings: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Analyser les similarités et générer les suggestions"""
        suggestions = []
        similarity_threshold = ai_settings.get("similarity_threshold", 0.7) if ai_settings else 0.7
        
        # Convertir les embeddings en matrice
        embedding_matrix = np.array([emb["embedding"] for emb in embeddings])
        
        # Calculer les similarités
        similarity_matrix = cosine_similarity(embedding_matrix)
        
        # Générer les suggestions
        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                similarity_score = similarity_matrix[i][j]
                
                if similarity_score >= similarity_threshold:
                    # Créer une suggestion
                    suggestion = self._create_suggestion(
                        pages[i], pages[j], similarity_score, embeddings[i], embeddings[j]
                    )
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _create_suggestion(
        self,
        source_page: Dict[str, Any],
        target_page: Dict[str, Any],
        similarity_score: float,
        source_embedding: Dict[str, Any],
        target_embedding: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Créer une suggestion de maillage interne"""
        from app.schemas.suggestion import SuggestionCreate
        
        # Générer un texte d'ancre basé sur le contenu
        anchor_text = self._generate_anchor_text(target_page)
        
        # Raisonnement pour la suggestion
        reasoning = f"Pages similaires avec un score de {similarity_score:.2f}. "
        reasoning += f"Source: {source_page.get('title', 'Sans titre')} -> "
        reasoning += f"Cible: {target_page.get('title', 'Sans titre')}"
        
        return SuggestionCreate(
            analysis_id="temp",  # Sera remplacé par l'ID réel
            source_page=source_page["url"],
            target_page=target_page["url"],
            anchor_text=anchor_text,
            score=similarity_score,
            reasoning=reasoning,
            metadata={
                "source_title": source_page.get("title", ""),
                "target_title": target_page.get("title", ""),
                "similarity_score": similarity_score
            }
        )
    
    def _generate_anchor_text(self, target_page: Dict[str, Any]) -> str:
        """Générer un texte d'ancre basé sur le contenu de la page cible"""
        # Utiliser le titre comme ancre par défaut
        if target_page.get("title"):
            return target_page["title"]
        
        # Utiliser le premier titre H1 ou H2
        if target_page.get("headings"):
            for heading in target_page["headings"]:
                if heading.strip():
                    return heading.strip()
        
        # Utiliser la description
        if target_page.get("description"):
            return target_page["description"][:50] + "..."
        
        # Fallback
        return "En savoir plus"
    
    async def optimize_anchor(
        self,
        current_anchor: str,
        target_page_title: str,
        context: str,
        provider: str = "openai",
        style: str = "natural",
        max_length: int = 50
    ) -> Dict[str, Any]:
        """Optimiser un texte d'ancre"""
        if provider == "openai":
            return await self._optimize_anchor_openai(
                current_anchor, target_page_title, context, style, max_length
            )
        elif provider == "gemini":
            return await self._optimize_anchor_gemini(
                current_anchor, target_page_title, context, style, max_length
            )
        else:
            raise ValueError(f"Provider non supporté: {provider}")
    
    async def _optimize_anchor_openai(
        self,
        current_anchor: str,
        target_page_title: str,
        context: str,
        style: str,
        max_length: int
    ) -> Dict[str, Any]:
        """Optimiser une ancre avec OpenAI"""
        try:
            prompt = f"""
            Optimisez le texte d'ancre suivant pour un lien vers la page "{target_page_title}".
            
            Contexte: {context}
            Ancre actuelle: "{current_anchor}"
            Style souhaité: {style}
            Longueur maximale: {max_length} caractères
            
            Règles:
            - L'ancre doit être descriptive et naturelle
            - Éviter les ancres génériques comme "cliquez ici"
            - Utiliser des mots-clés pertinents
            - Respecter la longueur maximale
            
            Ancre optimisée:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert SEO spécialisé dans l'optimisation des ancres de liens."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length * 2,
                temperature=0.7
            )
            
            optimized_anchor = response.choices[0].message.content.strip()
            
            # Générer des alternatives
            alternatives = await self._generate_anchor_alternatives_openai(
                target_page_title, context, style, max_length
            )
            
            return {
                "optimized_anchor": optimized_anchor,
                "confidence_score": 0.9,
                "alternatives": alternatives,
                "reasoning": f"Ancre optimisée pour {target_page_title} avec style {style}"
            }
            
        except Exception as e:
            print(f"Erreur OpenAI: {str(e)}")
            return {
                "optimized_anchor": current_anchor,
                "confidence_score": 0.5,
                "alternatives": [],
                "reasoning": f"Erreur lors de l'optimisation: {str(e)}"
            }
    
    async def _optimize_anchor_gemini(
        self,
        current_anchor: str,
        target_page_title: str,
        context: str,
        style: str,
        max_length: int
    ) -> Dict[str, Any]:
        """Optimiser une ancre avec Gemini"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Optimisez le texte d'ancre suivant pour un lien vers la page "{target_page_title}".
            
            Contexte: {context}
            Ancre actuelle: "{current_anchor}"
            Style souhaité: {style}
            Longueur maximale: {max_length} caractères
            
            Règles:
            - L'ancre doit être descriptive et naturelle
            - Éviter les ancres génériques comme "cliquez ici"
            - Utiliser des mots-clés pertinents
            - Respecter la longueur maximale
            
            Ancre optimisée:
            """
            
            response = model.generate_content(prompt)
            optimized_anchor = response.text.strip()
            
            # Générer des alternatives
            alternatives = await self._generate_anchor_alternatives_gemini(
                target_page_title, context, style, max_length
            )
            
            return {
                "optimized_anchor": optimized_anchor,
                "confidence_score": 0.85,
                "alternatives": alternatives,
                "reasoning": f"Ancre optimisée pour {target_page_title} avec style {style}"
            }
            
        except Exception as e:
            print(f"Erreur Gemini: {str(e)}")
            return {
                "optimized_anchor": current_anchor,
                "confidence_score": 0.5,
                "alternatives": [],
                "reasoning": f"Erreur lors de l'optimisation: {str(e)}"
            }
    
    async def _generate_anchor_alternatives_openai(
        self,
        target_page_title: str,
        context: str,
        style: str,
        max_length: int
    ) -> List[str]:
        """Générer des alternatives d'ancres avec OpenAI"""
        try:
            prompt = f"""
            Générez 3 alternatives d'ancres pour la page "{target_page_title}".
            
            Contexte: {context}
            Style: {style}
            Longueur maximale: {max_length} caractères
            
            Alternatives:
            1.
            2.
            3.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Générez des ancres alternatives pour des liens SEO."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            alternatives = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith(('1.', '2.', '3.'))]
            
            return alternatives[:3]
            
        except Exception as e:
            print(f"Erreur génération alternatives OpenAI: {str(e)}")
            return []
    
    async def _generate_anchor_alternatives_gemini(
        self,
        target_page_title: str,
        context: str,
        style: str,
        max_length: int
    ) -> List[str]:
        """Générer des alternatives d'ancres avec Gemini"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Générez 3 alternatives d'ancres pour la page "{target_page_title}".
            
            Contexte: {context}
            Style: {style}
            Longueur maximale: {max_length} caractères
            
            Alternatives:
            1.
            2.
            3.
            """
            
            response = model.generate_content(prompt)
            content = response.text
            
            alternatives = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith(('1.', '2.', '3.'))]
            
            return alternatives[:3]
            
        except Exception as e:
            print(f"Erreur génération alternatives Gemini: {str(e)}")
            return [] 