#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Agente de Análisis de Sentimiento para TalentekIA

Este agente analiza el sentimiento en textos y publicaciones de redes sociales.
"""

import logging
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from collections import Counter

# NLP imports
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
from wordcloud import WordCloud
import spacy

from src.agents.base_agent import BaseAgent

# Asegurar que los recursos necesarios estén descargados
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger("TalentekIA-AnalisisSentimiento")

class AnalisisSentimiento(BaseAgent):
    """Agente para análisis de sentimiento en texto y redes sociales."""

    def __init__(self, agent_id: str = "analisis_sentimiento", config: Optional[Dict[str, Any]] = None):
        """Inicializa el agente de análisis de sentimiento.
        
        Args:
            agent_id: Identificador único del agente
            config: Configuración específica del agente
        """
        super().__init__(agent_id, config)
        logger.info(f"Agente de Análisis de Sentimiento inicializado con ID: {agent_id}")
        
        # Configuración específica del agente
        self.language = self.config.get("language", "spanish")
        self.output_dir = Path(self.config.get("output_dir", "./output/analisis_sentimiento"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar recursos lingüísticos según el idioma
        self.setup_nlp_resources()
        
    def setup_nlp_resources(self) -> None:
        """Configura los recursos lingüísticos necesarios según el idioma."""
        logger.info(f"Configurando recursos NLP para idioma: {self.language}")
        
        # Stopwords
        if self.language == "spanish":
            self.stop_words = set(stopwords.words('spanish'))
            self.stemmer = SnowballStemmer('spanish')
            try:
                self.nlp = spacy.load("es_core_news_sm")
            except:
                logger.warning("Modelo spaCy para español no encontrado, descargándolo...")
                import subprocess
                subprocess.call([
                    "python", "-m", "spacy", "download", "es_core_news_sm"
                ])
                self.nlp = spacy.load("es_core_news_sm")
                
        elif self.language == "english":
            self.stop_words = set(stopwords.words('english'))
            self.stemmer = SnowballStemmer('english')
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                logger.warning("Modelo spaCy para inglés no encontrado, descargándolo...")
                import subprocess
                subprocess.call([
                    "python", "-m", "spacy", "download", "en_core_web_sm"
                ])
                self.nlp = spacy.load("en_core_web_sm")
        else:
            logger.warning(f"Idioma {self.language} no soportado completamente, usando inglés como fallback")
            self.stop_words = set(stopwords.words('english'))
            self.stemmer = SnowballStemmer('english')
            self.nlp = spacy.load("en_core_web_sm")
            
        # Léxicos de sentimiento (básicos para demostración)
        self.sentiment_lexicon = self._load_sentiment_lexicon()
        
    def _load_sentiment_lexicon(self) -> Dict[str, float]:
        """Carga un léxico de sentimiento básico para el idioma configurado.
        
        Returns:
            Diccionario de palabras con su polaridad de sentimiento
        """
        # Esta es una versión muy básica para demostración
        # En un escenario real, se cargaría un léxico completo desde un archivo
        
        if self.language == "spanish":
            return {
                "bueno": 0.8, "excelente": 1.0, "genial": 0.9, "maravilloso": 0.9,
                "malo": -0.8, "terrible": -1.0, "pésimo": -0.9, "horrible": -0.9,
                "me gusta": 0.7, "odio": -0.8, "encanta": 0.9, "detesto": -0.9,
                "feliz": 0.8, "triste": -0.7, "enojado": -0.8, "contento": 0.7,
                "satisfecho": 0.6, "insatisfecho": -0.6, "recomiendo": 0.8, "no recomiendo": -0.8,
                "problema": -0.5, "solución": 0.5, "error": -0.6, "funciona": 0.5,
                "caro": -0.4, "barato": 0.4, "calidad": 0.6, "defectuoso": -0.7,
                "rápido": 0.6, "lento": -0.5, "fácil": 0.5, "difícil": -0.5
            }
        else:  # English as default
            return {
                "good": 0.8, "excellent": 1.0, "great": 0.9, "wonderful": 0.9,
                "bad": -0.8, "terrible": -1.0, "awful": -0.9, "horrible": -0.9,
                "like": 0.7, "hate": -0.8, "love": 0.9, "detest": -0.9,
                "happy": 0.8, "sad": -0.7, "angry": -0.8, "content": 0.7,
                "satisfied": 0.6, "dissatisfied": -0.6, "recommend": 0.8, "not recommend": -0.8,
                "problem": -0.5, "solution": 0.5, "error": -0.6, "works": 0.5,
                "expensive": -0.4, "cheap": 0.4, "quality": 0.6, "defective": -0.7,
                "fast": 0.6, "slow": -0.5, "easy": 0.5, "difficult": -0.5
            }
    
    def preprocess_text(self, text: str) -> List[str]:
        """Preprocesa un texto para análisis.
        
        Args:
            text: Texto a preprocesar
            
        Returns:
            Lista de tokens preprocesados
        """
        if not text or not isinstance(text, str):
            return []
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar URLs
        text = re.sub(r'http\S+', '', text)
        
        # Eliminar menciones (@usuario)
        text = re.sub(r'@\w+', '', text)
        
        # Eliminar hashtags
        text = re.sub(r'#\w+', '', text)
        
        # Eliminar emojis (simplificado)
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Eliminar stopwords y palabras cortas
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]
        
        # Stemming
        tokens = [self.stemmer.stem(t) for t in tokens]
        
        return tokens
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analiza el sentimiento de un texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        if not text:
            return {"sentiment": "neutral", "score": 0, "confidence": 0}
        
        # Preprocesar texto
        tokens = self.preprocess_text(text)
        
        if not tokens:
            return {"sentiment": "neutral", "score": 0, "confidence": 0}
        
        # Enfoque básico de análisis léxico
        score = 0
        matches = 0
        
        for token in tokens:
            if token in self.sentiment_lexicon:
                score += self.sentiment_lexicon[token]
                matches += 1
        
        # Análisis con spaCy para entidades y dependencias
        doc = self.nlp(text)
        entities = [(e.text, e.label_) for e in doc.ents]
        
        # Para análisis más avanzado, buscar negaciones y modificadores
        negations = 0
        for token in doc:
            if token.dep_ == "neg":
                negations += 1
        
        # Ajustar score si hay negaciones
        if negations > 0 and matches > 0:
            score = -score
        
        # Normalizar score
        if matches > 0:
            normalized_score = score / matches
        else:
            normalized_score = 0
            
        # Determinar sentimiento y confianza
        if normalized_score > 0.1:
            sentiment = "positive"
            confidence = min(abs(normalized_score), 1.0)
        elif normalized_score < -0.1:
            sentiment = "negative"
            confidence = min(abs(normalized_score), 1.0)
        else:
            sentiment = "neutral"
            confidence = min(0.5, 1.0 - abs(normalized_score) * 5)
            
        return {
            "sentiment": sentiment,
            "score": normalized_score,
            "confidence": confidence,
            "tokens": tokens,
            "entities": entities,
            "negations": negations,
            "matches": matches
        }
        
    def batch_analyze(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analiza el sentimiento de múltiples textos.
        
        Args:
            texts: Lista de textos a analizar
            
        Returns:
            Lista de resultados de análisis de sentimiento
        """
        logger.info(f"Analizando sentimiento en {len(texts)} textos")
        
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
            
        return results
    
    def analyze_social_media_data(self, data: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """Analiza datos de redes sociales.
        
        Args:
            data: DataFrame con los datos de redes sociales
            text_column: Nombre de la columna que contiene el texto
            
        Returns:
            DataFrame con resultados de análisis agregados
        """
        logger.info(f"Analizando datos de redes sociales con {len(data)} entradas")
        
        if data.empty or text_column not in data.columns:
            logger.warning("DataFrame vacío o columna de texto no encontrada")
            return pd.DataFrame()
        
        # Crear copia para no modificar el original
        result_df = data.copy()
        
        # Aplicar análisis de sentimiento a cada texto
        sentiment_results = []
        
        for text in result_df[text_column]:
            if not isinstance(text, str):  # Manejar valores no string
                sentiment_results.append({
                    "sentiment": "neutral",
                    "score": 0,
                    "confidence": 0
                })
                continue
                
            sentiment = self.analyze_sentiment(text)
            sentiment_results.append(sentiment)
            
        # Extraer componentes del análisis a columnas separadas
        result_df['sentiment'] = [r['sentiment'] for r in sentiment_results]
        result_df['sentiment_score'] = [r['score'] for r in sentiment_results]
        result_df['sentiment_confidence'] = [r['confidence'] for r in sentiment_results]
        
        # Agregar columna categórica para facilitar visualización
        result_df['sentiment_category'] = pd.cut(
            result_df['sentiment_score'],
            bins=[-1.1, -0.6, -0.2, 0.2, 0.6, 1.1],
            labels=['Muy Negativo', 'Negativo', 'Neutral', 'Positivo', 'Muy Positivo']
        )
        
        return result_df
    
    def extract_topics(self, texts: List[str], n_topics: int = 5) -> List[Tuple[str, int]]:
        """Extrae los temas principales de una colección de textos.
        
        Args:
            texts: Lista de textos
            n_topics: Cantidad de temas a extraer
            
        Returns:
            Lista de tuplas (tema, frecuencia) ordenadas por frecuencia
        """
        logger.info(f"Extrayendo {n_topics} temas principales de {len(texts)} textos")
        
        # Concatenar todos los textos
        all_tokens = []
        for text in texts:
            if isinstance(text, str):
                all_tokens.extend(self.preprocess_text(text))
                
        # Extraer los temas más frecuentes
        counter = Counter(all_tokens)
        return counter.most_common(n_topics)
    
    def generate_charts(self, df: pd.DataFrame) -> Dict[str, str]:
        """Genera visualizaciones de los resultados de análisis.
        
        Args:
            df: DataFrame con resultados de análisis
            
        Returns:
            Diccionario con rutas a las imágenes generadas
        """
        logger.info("Generando visualizaciones de análisis de sentimiento")
        
        if df.empty:
            return {}
            
        chart_paths = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 1. Distribución de sentimiento
            plt.figure(figsize=(10, 6))
            sns.countplot(x='sentiment', data=df, palette={'positive': 'green', 'neutral': 'gray', 'negative': 'red'})
            plt.title('Distribución de Sentimiento')
            plt.xlabel('Sentimiento')
            plt.ylabel('Frecuencia')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            sentiment_dist_path = self.output_dir / f"sentiment_distribution_{timestamp}.png"
            plt.savefig(sentiment_dist_path)
            chart_paths['sentiment_distribution'] = str(sentiment_dist_path)
            plt.close()
            
            # 2. Distribución de puntuación de sentimiento
            plt.figure(figsize=(10, 6))
            sns.histplot(df['sentiment_score'], bins=20, kde=True)
            plt.axvline(x=0, color='red', linestyle='--')
            plt.title('Distribución de Puntuación de Sentimiento')
            plt.xlabel('Puntuación')
            plt.ylabel('Frecuencia')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            score_dist_path = self.output_dir / f"score_distribution_{timestamp}.png"
            plt.savefig(score_dist_path)
            chart_paths['score_distribution'] = str(score_dist_path)
            plt.close()
            
            # 3. Categorías de sentimiento
            if 'sentiment_category' in df.columns:
                plt.figure(figsize=(10, 6))
                category_counts = df['sentiment_category'].value_counts()
                palette = {
                    'Muy Positivo': '#2ca02c',  # Verde oscuro
                    'Positivo': '#98df8a',      # Verde claro
                    'Neutral': '#c5c5c5',       # Gris
                    'Negativo': '#ff9896',      # Rojo claro
                    'Muy Negativo': '#d62728'   # Rojo oscuro
                }
                
                # Ordenar categorías
                order = ['Muy Negativo', 'Negativo', 'Neutral', 'Positivo', 'Muy Positivo']
                order = [o for o in order if o in category_counts.index]
                
                ax = sns.barplot(x=category_counts.index, y=category_counts.values, 
                            order=order, palette=[palette[cat] for cat in order])
                plt.title('Distribución por Categorías de Sentimiento')
                plt.xlabel('Categoría')
                plt.ylabel('Frecuencia')
                plt.xticks(rotation=45)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                
                category_path = self.output_dir / f"sentiment_categories_{timestamp}.png"
                plt.savefig(category_path)
                chart_paths['sentiment_categories'] = str(category_path)
                plt.close()
            
            # 4. Nube de palabras (si hay datos de texto)
            if 'text' in df.columns:
                # Filtrar textos no-nulos
                all_text = ' '.join([text for text in df['text'] if isinstance(text, str)])
                if all_text:
                    # Preprocesar para eliminar stopwords
                    processed_text = ' '.join(self.preprocess_text(all_text))
                    
                    # Generar nube de palabras
                    wordcloud = WordCloud(width=800, height=400, 
                                         background_color='white',
                                         max_words=150,
                                         colormap='viridis',
                                         contour_width=1, contour_color='steelblue')
                    wordcloud.generate(processed_text)
                    
                    plt.figure(figsize=(10, 7))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    plt.tight_layout()
                    
                    wordcloud_path = self.output_dir / f"wordcloud_{timestamp}.png"
                    plt.savefig(wordcloud_path)
                    chart_paths['wordcloud'] = str(wordcloud_path)
                    plt.close()
            
            logger.info(f"Se generaron {len(chart_paths)} visualizaciones")
            return chart_paths
            
        except Exception as e:
            logger.error(f"Error al generar visualizaciones: {e}")
            return chart_paths
    
    def generate_report(self, df: pd.DataFrame, top_topics: List[Tuple[str, int]]) -> str:
        """Genera un informe de análisis de sentimiento.
        
        Args:
            df: DataFrame con resultados de análisis
            top_topics: Lista de temas principales
            
        Returns:
            Informe en formato texto
        """
        logger.info("Generando informe de análisis de sentimiento")
        
        if df.empty:
            return "No hay datos suficientes para generar un informe."
        
        # Generar informe
        report = []
        report.append("# Informe de Análisis de Sentimiento\n")
        report.append(f"Fecha del informe: {datetime.now().strftime('%Y-%m-%d')}\n")
        
        # Resumen general
        report.append("## Resumen General\n")
        
        total_items = len(df)
        sentiment_counts = df['sentiment'].value_counts()
        positive_count = sentiment_counts.get('positive', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negative', 0)
        
        positive_percent = (positive_count / total_items) * 100
        neutral_percent = (neutral_count / total_items) * 100
        negative_percent = (negative_count / total_items) * 100
        
        report.append(f"- **Total de textos analizados**: {total_items}")
        report.append(f"- **Sentimiento positivo**: {positive_count} textos ({positive_percent:.1f}%)")
        report.append(f"- **Sentimiento neutral**: {neutral_count} textos ({neutral_percent:.1f}%)")
        report.append(f"- **Sentimiento negativo**: {negative_count} textos ({negative_percent:.1f}%)")
        
        # Índice de sentimiento
        avg_score = df['sentiment_score'].mean()
        report.append(f"- **Índice de sentimiento promedio**: {avg_score:.3f} (de -1 a +1)")
        
        # Interpretación del sentimiento promedio
        if avg_score > 0.2:
            report.append("- **Interpretación**: Sentimiento general **positivo**.")
        elif avg_score < -0.2:
            report.append("- **Interpretación**: Sentimiento general **negativo**.")
        else:
            report.append("- **Interpretación**: Sentimiento general **neutral**.")
        
        # Temas principales
        report.append("\n## Temas Principales\n")
        
        if top_topics:
            for i, (topic, count) in enumerate(top_topics, 1):
                report.append(f"{i}. **{topic}**: {count} menciones")
        else:
            report.append("No se identificaron temas recurrentes.")
        
        # Análisis por categoría
        if 'sentiment_category' in df.columns:
            report.append("\n## Distribución por Categoría\n")
            
            category_counts = df['sentiment_category'].value_counts().sort_index()
            for category, count in category_counts.items():
                percent = (count / total_items) * 100
                report.append(f"- **{category}**: {count} textos ({percent:.1f}%)")
        
        # Recomendaciones
        report.append("\n## Recomendaciones\n")
        
        if avg_score < -0.3:
            report.append("- **Acción prioritaria**: Existe un sentimiento negativo predominante que requiere atención.")
            report.append("  - Identificar y abordar las principales quejas o problemas mencionados.")
            report.append("  - Implementar una estrategia de comunicación para mejorar la percepción.")
        elif avg_score < 0:
            report.append("- **Mejora necesaria**: El sentimiento general es ligeramente negativo.")
            report.append("  - Monitorear los temas recurrentes asociados con sentimiento negativo.")
            report.append("  - Desarrollar respuestas específicas para los problemas identificados.")
        elif avg_score < 0.3:
            report.append("- **Oportunidad de mejora**: El sentimiento general es neutral o ligeramente positivo.")
            report.append("  - Reforzar aspectos positivos identificados en los comentarios.")
            report.append("  - Trabajar para convertir experiencias neutrales en positivas.")
        else:
            report.append("- **Mantener estrategia**: El sentimiento general es claramente positivo.")
            report.append("  - Identificar y potenciar los factores que generan comentarios positivos.")
            report.append("  - Compartir casos de éxito y testimonios positivos.")
        
        return "\n".join(report)
    
    def save_results(self, df: pd.DataFrame, report: str, charts: Dict[str, str]) -> Dict[str, str]:
        """Guarda los resultados del análisis de sentimiento.
        
        Args:
            df: DataFrame con resultados del análisis
            report: Informe generado
            charts: Diccionario con rutas de visualizaciones generadas
            
        Returns:
            Diccionario con rutas de archivos guardados
        """
        logger.info("Guardando resultados del análisis de sentimiento")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = {}
        
        try:
            # Guardar DataFrame de resultados
            if not df.empty:
                results_path = self.output_dir / f"resultados_sentimiento_{timestamp}.csv"
                df.to_csv(results_path, index=False)
                output_files['results_data'] = str(results_path)
                
                # También guardar versión Excel si hay pandas_excel disponible
                try:
                    excel_path = self.output_dir / f"resultados_sentimiento_{timestamp}.xlsx"
                    df.to_excel(excel_path, index=False)
                    output_files['results_excel'] = str(excel_path)
                except Exception as e:
                    logger.warning(f"No se pudo guardar en formato Excel: {e}")
            
            # Guardar informe
            if report:
                report_path = self.output_dir / f"informe_sentimiento_{timestamp}.md"
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report)
                output_files['report'] = str(report_path)
                
                # También guardar versión HTML para visualización
                try:
                    import markdown
                    html = markdown.markdown(report)
                    html_report = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Informe de Análisis de Sentimiento</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }}
                            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
                            h2 {{ color: #3498db; margin-top: 30px; }}
                            li {{ margin-bottom: 10px; }}
                            strong {{ color: #2c3e50; }}
                        </style>
                    </head>
                    <body>
                    {html}
                    </body>
                    </html>
                    """
                    
                    html_path = self.output_dir / f"informe_sentimiento_{timestamp}.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_report)
                    output_files['html_report'] = str(html_path)
                except Exception as e:
                    logger.warning(f"No se pudo generar informe HTML: {e}")
            
            # Incluir rutas a visualizaciones
            if charts:
                output_files.update(charts)
                
            logger.info(f"Resultados guardados exitosamente: {len(output_files)} archivos")
            return output_files
            
        except Exception as e:
            logger.error(f"Error al guardar resultados: {e}")
            return output_files
    
    def process_data(self, data: Any) -> pd.DataFrame:
        """Procesa los datos de entrada para análisis.
        
        Args:
            data: Datos para procesar (texto, lista de textos o DataFrame)
            
        Returns:
            DataFrame con resultados de análisis
        """
        logger.info("Procesando datos para análisis de sentimiento")
        
        try:
            # Diferentes tipos de entrada
            if isinstance(data, str):
                # Entrada es un solo texto
                result = self.analyze_sentiment(data)
                return pd.DataFrame([result])
                
            elif isinstance(data, list):
                # Entrada es una lista de textos
                if all(isinstance(item, str) for item in data):
                    results = self.batch_analyze(data)
                    df = pd.DataFrame(results)
                    df['text'] = data
                    return df
                else:
                    logger.error("La lista debe contener solo elementos de texto")
                    return pd.DataFrame()
                    
            elif isinstance(data, pd.DataFrame):
                # Identificar columna de texto
                text_columns = [col for col in data.columns if 'text' in col.lower() 
                               or 'comentario' in col.lower() 
                               or 'mensaje' in col.lower()
                               or 'review' in col.lower()]
                
                if text_columns:
                    text_column = text_columns[0]
                else:
                    # Si no hay columna obvia, usar la primera columna de tipo string
                    string_cols = data.select_dtypes(include=['object']).columns
                    if not string_cols.empty:
                        text_column = string_cols[0]
                    else:
                        logger.error("No se encontró columna de texto en el DataFrame")
                        return pd.DataFrame()
                
                return self.analyze_social_media_data(data, text_column)
                
            else:
                logger.error(f"Tipo de datos no soportado: {type(data)}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error al procesar datos para análisis: {e}")
            return pd.DataFrame()
    
    def run(self) -> bool:
        """Ejecuta el agente de análisis de sentimiento.
        
        Returns:
            True si la ejecución fue exitosa, False en caso contrario
        """
        logger.info("Ejecutando agente de análisis de sentimiento")
        
        try:
            # Para demostración, usamos datos de ejemplo
            texts = [
                "Este producto es excelente, me encanta completamente",
                "No me gustó nada, terrible experiencia de compra",
                "Está bien, pero podría mejorar en algunos aspectos",
                "La atención al cliente fue rápida y amable",
                "El envío llegó con retraso y el producto estaba dañado",
                "Buen producto por el precio pagado",
                "Recomendaría este servicio a mis amigos",
                "Nunca más compro en esta tienda, pésima experiencia",
                "Producto de buena calidad pero un poco caro",
                "Me gusta mucho, funciona perfectamente"
            ]
            
            # Crear DataFrame de ejemplo
            data = pd.DataFrame({
                'text': texts,
                'fecha': pd.date_range(start='2023-01-01', periods=len(texts), freq='D'),
                'fuente': ['twitter'] * 3 + ['facebook'] * 4 + ['instagram'] * 3
            })
            
            # Procesar datos
            results_df = self.process_data(data)
            
            # Extraer temas principales
            top_topics = self.extract_topics(data['text'].tolist())
            
            # Generar visualizaciones
            charts = self.generate_charts(results_df)
            
            # Generar informe
            report = self.generate_report(results_df, top_topics)
            
            # Guardar resultados
            output_files = self.save_results(results_df, report, charts)
            
            logger.info("Ejecución del agente de análisis de sentimiento completada con éxito")
            logger.info(f"Archivos generados: {output_files}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error en la ejecución del agente de análisis de sentimiento: {e}")
            return False