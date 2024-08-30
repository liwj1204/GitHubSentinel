from openai import OpenAI
import os
import json
class LLMClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(
            #302.AI后台-API超市-API列表 生成的API KEY
            api_key=api_key,
            #302.AI的base-url
            base_url="https://api.302.ai/v1"
        )

    def summarize_report(self, issues, pull_requests, dry_run=False):
        content = f"""
        Summarize the following GitHub repository daily progress:

        Issues:
        {issues}

        Pull Requests:
        {pull_requests}
        """
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            with open("daily_progress/prompt.txt", "w+") as f:
                # 格式化JSON字符串的保存
                json.dump(messages, f, indent=4, ensure_ascii=False)
            return "DRY RUN"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        summary = response.choices[0].message.content
        return summary