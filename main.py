from rich.console import Console
from rich.table import Table
import sys
from llm import parse_expense, generate_insights
from storage import init_db, save_expense, fetch_all
from analytics import summarize, alert_overspend

console = Console()

def add_expense(text: str):
    console.print(f"[dim]Parsing:[/dim] {text}")
    try:
        expense = parse_expense(text)
    except Exception as e:
        console.print(f"[red]Could not parse expense:[/red] {e}")
        return
    save_expense(expense)
    console.print(
        f"[green]✓ Saved[/green]  "
        f"[bold]${expense['amount']:.2f}[/bold] • "
        f"{expense['category']} • {expense['date']}"
    )

def show_summary():
    expenses = fetch_all()
    if not expenses:
        console.print("[yellow]No expenses yet.[/yellow]")
        return

    summary = summarize(expenses)

    table = Table(title="Expenses by Category")
    table.add_column("Category", style="cyan")
    table.add_column("Total", justify="right", style="bold")
    for cat, amt in sorted(summary["by_category"].items(), key=lambda x: -x[1]):
        table.add_row(cat, f"${amt:.2f}")

    console.print(table)
    console.print(
        f"\nTotal spent: [bold]${summary['total_spent']:.2f}[/bold]  "
        f"across {summary['expense_count']} expenses\n"
    )

    alert = alert_overspend(summary)
    if alert:
        console.print(alert)

    console.print("\n[bold]Generating AI insights...[/bold]")
    insights = generate_insights(summary)
    console.print(insights)

def main():
    init_db()
    if len(sys.argv) < 2:
        console.print("Usage:\n  python main.py add <text>\n  python main.py summary")
        return
    cmd = sys.argv[1]
    if cmd == "add":
        add_expense(" ".join(sys.argv[2:]))
    elif cmd == "summary":
        show_summary()
    else:
        console.print(f"[red]Unknown command:[/red] {cmd}")

if __name__ == "__main__":
    main()