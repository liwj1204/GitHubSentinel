from ConfigManager import ConfigManager
from SubscriptionManager import SubscriptionManager
from GitHubAPIClient import GitHubAPIClient
from UpdateFetcher import UpdateFetcher
from ReportGenerator import ReportGenerator
from LLMClient import LLMClient
from Scheduler import Scheduler
import threading
from cli import create_parser  # 引入新的 CLI 模块
from DatabaseClient import DatabaseClient
from NotificationSystem import NotificationSystem
def setup_environment():
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
    report_generator = ReportGenerator(db_client, llm_client)
    notification_system = NotificationSystem(config_manager)

    return {
        'subscription_manager': subscription_manager,
        'update_fetcher': update_fetcher,
        'report_generator': report_generator,
        'notification_system': notification_system,
        'github_api_client': github_api_client
    }

def start_scheduler(scheduler, subscription_manager, update_fetcher, report_generator, notification_system):
    scheduler.schedule_daily(lambda: check_updates_and_notify(subscription_manager, update_fetcher, report_generator, notification_system))
    print("Scheduler started for daily updates.")

def check_updates_and_notify(subscription_manager, update_fetcher, report_generator, notification_system):
    update_fetcher.fetch_updates(subscription_manager.load_subscriptions())
    report = report_generator.generate_report()
    notification_system.send_notification(report)
def main():
    env = setup_environment()
    parser = create_parser()  # 使用新的 CLI 模块创建解析器

    # 打印一次帮助信息，让用户了解可用命令
    parser.print_help()

    while True:
        try:
            # 提示用户输入命令
            command_input = input("GitHub Sentinel > ").strip().split()

            if not command_input:
                continue
# 手动处理 "help" 命令
            if command_input[0] == "help":
                parser.print_help()
                continue
            # 解析命令输入
            args = parser.parse_args(command_input)

            if args.command == 'add':
                env['subscription_manager'].add_subscription(args.repo_url)
            elif args.command == 'remove':
                env['subscription_manager'].remove_subscription(args.repo_url)
            elif args.command == 'list':
                subscriptions = env['subscription_manager'].list_subscriptions()
                print("Current subscriptions:")
                for repo in subscriptions:
                    print(f"- {repo}")
            elif args.command == 'fetch':
                check_updates_and_notify(env['subscription_manager'], env['update_fetcher'], env['report_generator'], env['notification_system'])
            elif args.command == 'export':
                env['github_api_client'].export_daily_progress(args.repo_url)
            elif args.command == 'generate':
                env['report_generator'].generate_formal_report(args.report_file)
            elif args.command == 'exit':
                print("Exiting GitHub Sentinel...")
                break
            else:
                parser.print_help()

        except SystemExit:
            # 捕获 argparse 的退出行为，并继续运行
            print("Invalid command. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting GitHub Sentinel...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()