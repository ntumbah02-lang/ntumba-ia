from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

console = Console()


def load_environment() -> None:
    """Charge les variables d'environnement depuis le fichier .env."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()


def main() -> None:
    """Point d'entrée principal de l'application."""
    load_environment()

    console.print("[bold green]Bienvenue dans ntumba IA[/bold green]")
    console.print("Votre assistant est prêt.")

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        console.print("[dim]Clé API détectée : oui[/dim]")
    else:
        console.print("[yellow]Aucune clé API détectée. Ajoutez OPENAI_API_KEY dans votre .env.[/yellow]")


if __name__ == "__main__":
    main()
