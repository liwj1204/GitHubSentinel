import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog="github-sentinel",
        description="GitHub Sentinel CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Add subcommand
    add_parser = subparsers.add_parser('add', help='Add a repository subscription')
    add_parser.add_argument('repo_url', help='The GitHub repository URL to subscribe')

    # Remove subcommand
    remove_parser = subparsers.add_parser('remove', help='Remove a repository subscription')
    remove_parser.add_argument('repo_url', help='The GitHub repository URL to unsubscribe')

    # List subcommand
    list_parser = subparsers.add_parser('list', help='List all repository subscriptions')

    # Fetch subcommand
    fetch_parser = subparsers.add_parser('fetch', help='Fetch updates for all subscribed repositories')

    # Export subcommand
    export_parser = subparsers.add_parser('export', help='Export daily progress for a repository')
    export_parser.add_argument('repo_url', help='The GitHub repository URL to export progress')

    # Generate report subcommand
    generate_parser = subparsers.add_parser('generate', help='Generate a formal report from a daily progress file')
    generate_parser.add_argument('report_file', help='The path of the daily report file to generate a formal report')

    # Exit subcommand
    exit_parser = subparsers.add_parser('exit', help='Exit the GitHub Sentinel tool')

    return parser