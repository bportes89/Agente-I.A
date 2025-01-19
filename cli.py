import typer
from .agent import IAAgent

app = typer.Typer()
agent = IAAgent()

@app.command()
def perguntar(
    prompt: str = typer.Argument(..., help="Sua pergunta para o agente"),
    max_length: int = typer.Option(100, help="Tamanho máximo da resposta")
):
    """Faz uma pergunta ao agente de IA"""
    resposta = agent.gerar_resposta(prompt, max_length)
    typer.echo(f"\nResposta: {resposta}")

@app.command()
def interativo():
    """Modo interativo para conversar com o agente"""
    typer.echo("=== Modo Interativo do Agente IA ===")
    typer.echo("Digite 'sair' para encerrar")
    
    while True:
        prompt = typer.prompt("\nSua pergunta")
        
        if prompt.lower() == 'sair':
            typer.echo("Até logo!")
            break
            
        resposta = agent.gerar_resposta(prompt)
        typer.echo(f"\nResposta: {resposta}")

if __name__ == "__main__":
    app()