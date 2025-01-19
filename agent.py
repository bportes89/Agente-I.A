from transformers import pipeline
from typing import Optional, Dict
import logging
from datetime import datetime
import json
import os
from functools import lru_cache

# Configuração de logging
logging.basicConfig(
    filename='agente_ia.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IAAgent:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        self.summarizer = pipeline('summarization')
        self.history: Dict[str, list] = {}
        
    @lru_cache(maxsize=100)
    def gerar_resposta(self, prompt: str, max_length: Optional[int] = 100) -> str:
        """Gera uma resposta para o prompt dado com cache"""
        try:
            logging.info(f"Gerando resposta para prompt: {prompt[:50]}...")
            resposta = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1
            )
            self._salvar_historico(prompt, resposta[0]['generated_text'])
            return resposta[0]['generated_text']
        except Exception as e:
            logging.error(f"Erro ao gerar resposta: {str(e)}")
            return f"Erro ao gerar resposta: {str(e)}"
    
    def analisar_sentimento(self, texto: str) -> dict:
        """Analisa o sentimento do texto"""
        try:
            resultado = self.sentiment_analyzer(texto)
            return resultado[0]
        except Exception as e:
            logging.error(f"Erro na análise de sentimento: {str(e)}")
            return {"erro": str(e)}
    
    def resumir_texto(self, texto: str, max_length: int = 130) -> str:
        """Resumir textos longos"""
        try:
            resumo = self.summarizer(texto, max_length=max_length, min_length=30)
            return resumo[0]['summary_text']
        except Exception as e:
            logging.error(f"Erro ao resumir texto: {str(e)}")
            return f"Erro ao resumir: {str(e)}"
    
    def _salvar_historico(self, prompt: str, resposta: str):
        """Salva o histórico de interações"""
        timestamp = datetime.now().isoformat()
        if not os.path.exists('historico'):
            os.makedirs('historico')
            
        with open(f'historico/historico_{datetime.now().date()}.json', 'a') as f:
            json.dump({
                'timestamp': timestamp,
                'prompt': prompt,
                'resposta': resposta
            }, f)
            f.write('\n')