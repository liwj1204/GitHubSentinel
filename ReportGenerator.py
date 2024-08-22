import os

class ReportGenerator:
    def __init__(self, db_client, llm_client):
        self.db_client = db_client
        self.llm_client = llm_client

    def generate_formal_report(self, daily_report_file):
        with open(daily_report_file, 'r', encoding='utf-8') as f:
            content = f.read()

        issues_start = content.find("## Issues")
        pull_requests_start = content.find("## Pull Requests")

        issues = content[issues_start:pull_requests_start].strip()
        pull_requests = content[pull_requests_start:].strip()

        summary = self.llm_client.summarize_report(issues, pull_requests,dry_run=True)

        # Save the summarized report
        report_file_name = daily_report_file.replace('.md', '_formal.md')
        with open(report_file_name, 'w', encoding='utf-8') as f:
            f.write(f"# Formal Daily Report\n\n{summary}")

        print(f"Formal report saved to {report_file_name}")
        return report_file_name