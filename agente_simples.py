from transformers import pipeline

def fazer_pergunta(pergunta):
    """Função para fazer perguntas usando modelo local"""
    try:
        # Inicializa o modelo
        gerador = pipeline('text-generation', model='gpt2')
        
        # Gera a resposta
        resposta = gerador(pergunta, max_length=100, num_return_sequences=1)
        
        # Retorna o texto gerado
        return resposta[0]['generated_text']
    except Exception as erro:
        return f"Ocorreu um erro: {str(erro)}"

def main():
    print("=== Assistente de IA ===")
    print("Digite 'sair' para encerrar")
    print("Aguarde enquanto o modelo é carregado...")
    
    while True:
        # Pega a pergunta do usuário
        pergunta = input("\nSua pergunta: ")
        
        # Verifica se quer sair
        if pergunta.lower() == 'sair':
            print("Até logo!")
            break
        
        # Obtém e mostra a resposta
        print("\nProcessando...")
        resposta = fazer_pergunta(pergunta)
        print(f"\nResposta: {resposta}")

if __name__ == "__main__":
    main()