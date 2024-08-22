from ConfigManager import ConfigManager
from DatabaseClient import DatabaseClient
from GitHubAPIClient import GitHubAPIClient
from SubscriptionManager import SubscriptionManager
from UpdateFetcher import UpdateFetcher
from NotificationSystem import NotificationSystem
from ReportGenerator import ReportGenerator
from Scheduler import Scheduler
import threading
from LLMClient import LLMClient
def print_help():
    help_text = """
GitHub Sentinel Help:

Available commands:
- add     : Add a new repository subscription.
            Usage: add
            Follow the prompt to enter the repository URL.

- remove  : Remove an existing repository subscription.
            Usage: remove
            Follow the prompt to enter the repository URL.

- list    : List all currently subscribed repositories.
            Usage: list

- fetch   : Manually fetch updates from all subscribed repositories and generate a report.
            Usage: fetch

- help    : Display this help message.
            Usage: help

- exit    : Exit the GitHub Sentinel tool.
            Usage: exit
"""
    print(help_text)

def check_updates_and_notify(subscription_manager, update_fetcher, report_generator, notification_system):
    update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
    report = report_generator.generate_report()
    notification_system.send_notification(report)

def interactive_menu(subscription_manager, update_fetcher, report_generator, notification_system, github_api_client):
    while True:
        command = input("Enter command (add, remove, list, fetch, export, generate, help, exit): ").strip().lower()

        if command == "add":
            repo_url = input("Enter repository URL to subscribe: ").strip()
            subscription_manager.add_subscription(repo_url)
        elif command == "remove":
            repo_url = input("Enter repository URL to unsubscribe: ").strip()
            subscription_manager.remove_subscription(repo_url)
        elif command == "list":
            subscriptions = subscription_manager.list_subscriptions()
            print("Current subscriptions:")
            for repo in subscriptions:
                print(f"- {repo}")
        elif command == "fetch":
            check_updates_and_notify(subscription_manager, update_fetcher, report_generator, notification_system)
        elif command == "export":
            repo_url = input("Enter repository URL to export daily progress: ").strip()
            daily_report_file = github_api_client.export_daily_progress(repo_url)
        elif command == "generate":
            report_file = input("Enter the path of the daily report file to generate a formal report: ").strip()
            report_generator.generate_formal_report(report_file)
        elif command == "help":
            print_help()
        elif command == "exit":
            print("Exiting GitHub Sentinel...")
            break
        else:
            print("Unknown command. Please enter 'add', 'remove', 'list', 'fetch', 'export', 'generate', 'help', or 'exit'.")


def start_scheduler(scheduler, subscription_manager, update_fetcher, report_generator, notification_system):
    scheduler.schedule_daily(lambda: check_updates_and_notify(subscription_manager, update_fetcher, report_generator, notification_system))
    print("Scheduler started for daily updates.")

def main():
    # Initialize configuration
    config_manager = ConfigManager('config.yaml')
    config_manager.load_config()

    # Initialize database
    db_client = DatabaseClient(config_manager.get('db_url'))
    db_client.connect()

    # Initialize GitHub API client
    github_api_client = GitHubAPIClient(config_manager.get('github_token'))

    # Initialize LLM client
    llm_client = LLMClient()

    # Initialize core modules
    subscriptions_file = config_manager.get('subscriptions_file', 'subscriptions.json')
    subscription_manager = SubscriptionManager(subscriptions_file)
    update_fetcher = UpdateFetcher(github_api_client, db_client)
    notification_system = NotificationSystem(config_manager)
    report_generator = ReportGenerator(db_client, llm_client)

    # Start scheduler in a separate thread
    scheduler = Scheduler()
    scheduler_thread = threading.Thread(target=start_scheduler, args=(scheduler, subscription_manager, update_fetcher, report_generator, notification_system))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Print help information at startup
    print_help()

    # Start interactive command loop
    interactive_menu(subscription_manager, update_fetcher, report_generator, notification_system, github_api_client)

if __name__ == '__main__':
    main()