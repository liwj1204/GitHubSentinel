from ConfigManager import ConfigManager
from DatabaseClient import DatabaseClient
from GitHubAPIClient import GitHubAPIClient
from SubscriptionManager import SubscriptionManager
from UpdateFetcher import UpdateFetcher
from NotificationSystem import NotificationSystem
from ReportGenerator import ReportGenerator

def main():
    # 初始化配置
    config_manager = ConfigManager('config.yaml')
    config_manager.load_config()

    # 初始化数据库
    db_client = DatabaseClient(config_manager.get('db_url'))
    db_client.connect()

    # 初始化 GitHub API 客户端
    github_api_client = GitHubAPIClient(config_manager.get('github_token'))

    # 初始化核心模块
    subscription_manager = SubscriptionManager(db_client)
    update_fetcher = UpdateFetcher(github_api_client, db_client)
    notification_system = NotificationSystem(config_manager)
    report_generator = ReportGenerator(db_client)

    # 添加一些订阅
    subscription_manager.add_subscription('https://github.com/user/repo1')
    subscription_manager.add_subscription('https://github.com/user/repo2')

    # 获取更新并生成报告
    update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
    report = report_generator.generate_report()

    # 发送通知
    notification_system.send_notification(report)

if __name__ == '__main__':
    main()
