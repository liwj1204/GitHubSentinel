class ReportGenerator:
    def __init__(self, db_client):
        self.db_client = db_client

    def generate_report(self):
        updates = self.db_client.retrieve_updates()
        report = "Update Report:\n"
        for update in updates:
            report += f"Repo: {update.repo_url}\nTime: {update.update_time}\nContent: {update.update_content}\n\n"
        return report
