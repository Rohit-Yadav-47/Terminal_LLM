import os
from groq import Groq
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
from typing import Optional, List, Dict
from datetime import datetime
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

# Enable Rich's traceback for better error visualization
install()

# Initialize Rich console
console = Console()

# Initialize Typer app
app = typer.Typer()

class GroqTerminal:
    def __init__(self):

        self.api_key = ""  # Replace with your GROQ API key

        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Initialize conversation histories with a default tab
        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {"default": []}
        self.current_tab: str = "default"
        
        # Available models with detailed information
        self.models = {
            "1": {
                "model_id": "gemma2-9b-it",
                "developer": "Google",
                "context_window": 8192,
                "max_output_tokens": None,
                "max_file_size": None,
            },
            "2": {
                "model_id": "llama-3.3-70b-versatile",
                "developer": "Meta",
                "context_window": 128000,
                "max_output_tokens": 32768,
                "max_file_size": None,
            },
            "3": {
                "model_id": "llama-3.1-8b-instant",
                "developer": "Meta",
                "context_window": 128000,
                "max_output_tokens": 8192,
                "max_file_size": None,
            },
            "4": {
                "model_id": "llama-guard-3-8b",
                "developer": "Meta",
                "context_window": 8192,
                "max_output_tokens": None,
                "max_file_size": None,
            },
            "5": {
                "model_id": "llama3-70b-8192",
                "developer": "Meta",
                "context_window": 8192,
                "max_output_tokens": None,
                "max_file_size": None,
            },
            "6": {
                "model_id": "llama3-8b-8192",
                "developer": "Meta",
                "context_window": 8192,
                "max_output_tokens": None,
                "max_file_size": None,
            },
            "7": {
                "model_id": "mixtral-8x7b-32768",
                "developer": "Mistral",
                "context_window": 32768,
                "max_output_tokens": None,
                "max_file_size": None,
            },
        }
        self.current_model = self.models["2"]  # Default to llama-3.3-70b-versatile
        
        # Define available commands
        self.commands = [
            "/help", "/clear", "/save", "/load",
            "/model", "/exit", "/history", "/tabs", "/switch",
            "/newtab", "/closetab", "/listtabs"
        ]
        self.command_completer = WordCompleter(self.commands, ignore_case=True)
        
        # Initialize PromptSession with history and completer
        self.session_history = InMemoryHistory()
        self.session = PromptSession(
            history=self.session_history,
            completer=self.command_completer,
            complete_while_typing=True
        )
        
        # Setup key bindings
        self.bindings = self._setup_keybindings()
        
        # Initialize tabs
        self.tabs: Dict[str, List[Dict[str, str]]] = {"default": []}
        self.tab_order: List[str] = ["default"]

    def _setup_keybindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add('c-c')
        def _(event):
            """Handle Ctrl+C to prompt exit."""
            event.app.exit(exception=KeyboardInterrupt, style='class:aborting')

        return kb

    def save_conversation(self, filename: Optional[str] = None):
        if not filename:
            filename = f"conversation_{self.current_tab}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.tabs[self.current_tab], f, indent=2)
        console.print(f"[green]Conversation saved to {filename}[/green]")

    def load_conversation(self, filename: str):
        try:
            with open(filename, 'r') as f:
                self.tabs[self.current_tab] = json.load(f)
            console.print(f"[green]Conversation loaded from {filename}[/green]")
        except FileNotFoundError:
            console.print(f"[red]File not found: {filename}[/red]")
        except json.JSONDecodeError:
            console.print(f"[red]Invalid JSON format in file: {filename}[/red]")

    def switch_model(self):
        table = Table(title="Available Models", show_header=True, header_style="bold magenta")
        table.add_column("Number", style="dim", width=6)
        table.add_column("Model ID", min_width=25)
        table.add_column("Developer", min_width=15)
        table.add_column("Context Window (Tokens)", min_width=20)
        table.add_column("Max Output Tokens", min_width=18)
        table.add_column("Max File Size", min_width=15)

        for key, model in self.models.items():
            context_window = model["context_window"] if model["context_window"] else "-"
            max_output = model["max_output_tokens"] if model["max_output_tokens"] else "-"
            max_file = model["max_file_size"] if model["max_file_size"] else "-"
      
            table.add_row(
                key,
                model["model_id"],
                model["developer"],
                str(context_window),
                str(max_output),
                str(max_file),
                
            )
        console.print(table)
        choice = typer.prompt("Select model number", type=str)
        if choice in self.models:
            self.current_model = self.models[choice]
            console.print(f"[green]Switched to model: {self.current_model['model_id']}[/green]")
        else:
            console.print(f"[red]Invalid model number: {choice}[/red]")

    def get_completion(self, messages: List[Dict[str, str]]) -> Optional[str]:
        try:
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                progress.add_task(description="Generating response...", total=None)
                response = self.client.chat.completions.create(
                    messages=messages,
                    model=self.current_model["model_id"],
                    stream=False,
                    temperature=0.7,
                )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return None

    def display_help(self):
        help_text = """
        **Available Commands:**
        - `/help` - Show this help message
        - `/clear` - Clear the conversation history of the current tab
        - `/save [filename]` - Save current conversation to a file
        - `/load <filename>` - Load conversation from a file into the current tab
        - `/model` - Switch between available models
        - `/exit` - Exit the application
        - `/history` - Show conversation history of the current tab
        - `/tabs` - Manage conversation tabs
        - `/newtab <tab_name>` - Create a new conversation tab
        - `/closetab <tab_name>` - Close an existing conversation tab
        - `/listtabs` - List all active conversation tabs
        - `/switch <tab_name>` - Switch to a different conversation tab
        """
        console.print(Panel(Markdown(help_text), title="Help", border_style="blue"))

    def display_history(self):
        history = self.tabs.get(self.current_tab, [])
        if not history:
            console.print(f"[yellow]No conversation history in tab '{self.current_tab}'.[/yellow]")
            return
        table = Table(title=f"Conversation History - Tab: {self.current_tab}", show_header=True, header_style="bold magenta")
        table.add_column("Role", style="dim", width=12)
        table.add_column("Message")
        for msg in history:
            role = msg["role"].capitalize()
            content = msg["content"]
            role_color = "green" if msg["role"] == "user" else "blue"
            table.add_row(f"[{role_color}]{role}[/{role_color}]", content)
        console.print(table)

    def manage_tabs(self):
        help_text = """
        **Tab Management Commands:**
        - `/newtab <tab_name>` - Create a new conversation tab
        - `/closetab <tab_name>` - Close an existing conversation tab
        - `/listtabs` - List all active conversation tabs
        - `/switch <tab_name>` - Switch to a different conversation tab
        """
        console.print(Panel(Markdown(help_text), title="Tab Management", border_style="cyan"))

    def handle_command(self, user_input: str):
        parts = user_input.strip().split()
        command = parts[0]
        args = parts[1:]

        if command == '/exit':
            if Confirm.ask("Are you sure you want to exit?"):
                raise typer.Exit()
        elif command == '/help':
            self.display_help()
        elif command == '/clear':
            self.tabs[self.current_tab] = []
            console.print(f"[yellow]Conversation history cleared in tab '{self.current_tab}'.[/yellow]")
        elif command == '/save':
            filename = args[0] if args else None
            self.save_conversation(filename)
        elif command == '/load':
            if not args:
                console.print("[red]Please specify a filename to load.[/red]")
                return
            self.load_conversation(args[0])
        elif command == '/model':
            self.switch_model()
        elif command == '/history':
            self.display_history()
        elif command == '/tabs':
            self.manage_tabs()
        elif command == '/newtab':
            if not args:
                console.print("[red]Please specify a name for the new tab.[/red]")
                return
            tab_name = args[0]
            if tab_name in self.tabs:
                console.print(f"[red]Tab '{tab_name}' already exists.[/red]")
                return
            self.tabs[tab_name] = []
            self.tab_order.append(tab_name)
            console.print(f"[green]New tab '{tab_name}' created.[/green]")
        elif command == '/closetab':
            if not args:
                console.print("[red]Please specify the name of the tab to close.[/red]")
                return
            tab_name = args[0]
            if tab_name not in self.tabs:
                console.print(f"[red]Tab '{tab_name}' does not exist.[/red]")
                return
            if tab_name == "default":
                console.print("[red]Cannot close the default tab.[/red]")
                return
            del self.tabs[tab_name]
            self.tab_order.remove(tab_name)
            console.print(f"[green]Tab '{tab_name}' closed.[/green]")
            if self.current_tab == tab_name:
                self.current_tab = self.tab_order[0]
                console.print(f"[yellow]Switched to tab '{self.current_tab}'.[/yellow]")
        elif command == '/listtabs':
            table = Table(title="Active Tabs", show_header=True, header_style="bold magenta")
            table.add_column("Tab Name", style="bold cyan")
            for tab in self.tab_order:
                indicator = "*" if tab == self.current_tab else ""
                table.add_row(f"{tab} {indicator}")
            console.print(table)
        elif command == '/switch':
            if not args:
                console.print("[red]Please specify the name of the tab to switch to.[/red]")
                return
            tab_name = args[0]
            if tab_name not in self.tabs:
                console.print(f"[red]Tab '{tab_name}' does not exist.[/red]")
                return
            self.current_tab = tab_name
            console.print(f"[green]Switched to tab '{self.current_tab}'.[/green]")
        else:
            console.print(f"[red]Unknown command: {command}[/red]")

    def run(self):
        console.print("[bold bright_green]Welcome to Groq Terminal![/bold bright_green]")
        console.print("Type [bold]/help[/bold] for available commands")

        while True:
            try:
                # Create a FormattedText prompt for colored and styled prompt
                prompt_text = FormattedText([
                    ('bold green', f"{self.current_tab}"),
                    ('', '> ')
                ])

                user_input = self.session.prompt(
                    prompt_text,
                    key_bindings=self.bindings
                )

                # Handle empty input
                if not user_input.strip():
                    continue

                # Handle commands
                if user_input.startswith('/'):
                    self.handle_command(user_input)
                    continue

                # Add user message to current tab's history
                self.tabs[self.current_tab].append({"role": "user", "content": user_input})

                # Get and display response
                response = self.get_completion(self.tabs[self.current_tab])

                if response:
                    # Add assistant response to history
                    self.tabs[self.current_tab].append({"role": "assistant", "content": response})
                    # Display formatted response
                    console.print("\n[bold blue]Assistant:[/bold blue]")
                    console.print(Markdown(response))

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user. Type /exit to quit.[/yellow]")
            except typer.Exit:
                console.print("[bold red]Goodbye![/bold red]")
                break
            except Exception as e:
                console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")

@app.command()
def main():
    """
    Launch the Groq Terminal.
    """
    try:
        terminal = GroqTerminal()
        terminal.run()
    except EnvironmentError as ee:
        console.print(f"[red]{str(ee)}[/red]")
    except Exception as e:
        console.print(f"[red]Failed to start Groq Terminal: {str(e)}[/red]")

if __name__ == "__main__":
    main()
