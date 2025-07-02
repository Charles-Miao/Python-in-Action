import smtplib
import re
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_git_log(commit_block):
    """
    解析单个 git 提交块的内容, 提取关键信息。
    """
    parsed_data = {
        'author': 'N/A',
        'commit_date': 'N/A',
        'version': 'N/A',
        'remote_url': 'N/A',
        'message': 'No commit message found.',
        'diff': 'No diff information available.'
    }

    try:
        # 使用正则表达式提取各个部分
        author_match = re.search(r"Author: (.*)", commit_block)
        if author_match:
            parsed_data['author'] = author_match.group(1).strip()

        date_match = re.search(r"Commit date: (.*)", commit_block)
        if date_match:
            parsed_data['commit_date'] = date_match.group(1).strip()

        version_match = re.search(r"Current Version: (.*)", commit_block)
        if version_match:
            parsed_data['version'] = version_match.group(1).strip()

        remote_url_match = re.search(r"Remote URL: (.*)", commit_block)
        if remote_url_match:
            parsed_data['remote_url'] = remote_url_match.group(1).strip()

        # 优化后的Regex：精确捕获“Commit messages”和“Full diff”之间的内容
        message_match = re.search(r"-+Commit messages-+\s*(.*?)\s*-+Full diff", commit_block, re.DOTALL)
        if message_match:
            parsed_data['message'] = message_match.group(1).strip()

        # 优化后的Regex：精确捕获“Full diff”之后的所有内容
        diff_match = re.search(r"-+Full diff HEAD vs HEAD~1-+\s*(.*)", commit_block, re.DOTALL)
        if diff_match:
            parsed_data['diff'] = diff_match.group(1).strip()

    except Exception as e:
        print(f"Error parsing git log block: {e}")

    return parsed_data

def format_diff_for_html(diff_text):
    """
    将 diff 文本格式化为带颜色高亮的 HTML。
    """
    html_lines = []
    # 对特殊HTML字符进行转义，防止XSS
    escaped_diff = html.escape(diff_text)
    
    for line in escaped_diff.splitlines():
        if line.startswith('+'):
            html_lines.append(f'<div class="diff-line add">{line}</div>')
        elif line.startswith('-'):
            html_lines.append(f'<div class="diff-line del">{line}</div>')
        elif line.startswith('@@'):
            html_lines.append(f'<div class="diff-line info">{line}</div>')
        elif line.startswith('diff --git'):
            html_lines.append(f'<div class="diff-line header">{line}</div>')
        else:
            html_lines.append(f'<div class="diff-line">{line}</div>')
            
    return "\n".join(html_lines)


def create_html_body(commits_data_list):
    """
    根据解析后的提交列表，生成美观的 HTML 邮件正文。
    """
    commit_cards_html = []
    for index, parsed_data in enumerate(commits_data_list):
        formatted_diff = format_diff_for_html(parsed_data.get('diff', ''))
        commit_card = f'''
        <div class="commit-card">
            <h2 class="commit-title">Commit #{index + 1}</h2>
            <!-- Section: Commit Details -->
            <div class="section">
                <h3 class="section-title">提交详情</h3>
                <div class="commit-details">
                    <p><strong>Author:</strong> {parsed_data['author']}</p>
                    <p><strong>Commit Date:</strong> {parsed_data['commit_date']}</p>
                    <p><strong>Version (SHA):</strong> {parsed_data['version']}</p>
                    <p><strong>Remote URL:</strong> <a href="{parsed_data['remote_url']}" class="repo-link">{parsed_data['remote_url']}</a></p>
                </div>
            </div>
            <!-- Section: Commit Message -->
            <div class="section">
                <h3 class="section-title">提交信息</h3>
                <div class="commit-message">
                    <blockquote>{parsed_data['message']}</blockquote>
                </div>
            </div>
            <!-- Section: Code Diff -->
            <div class="section">
                <h3 class="section-title">代码变更</h3>
                <div class="diff-block">
                    {formatted_diff}
                </div>
            </div>
        </div>
        '''
        commit_cards_html.append(commit_card)

    # 将所有卡片组合起来
    all_commits_content = "".join(commit_cards_html)
    num_commits = len(commits_data_list)

    # 完整的 HTML 模板
    html_template = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Git 仓库提交记录</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                width: 100% !important;
                background-color: #f4f7f6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #333;
            }}
            .email-container {{
                max-width: 800px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
                border: 1px solid #e0e0e0;
            }}
            .email-header {{
                background: linear-gradient(135deg, #0052d4, #43a047);
                color: #ffffff;
                padding: 30px;
                text-align: center;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: 600;
            }}
            .email-content {{
                padding: 20px 35px 35px;
            }}
            .summary-title {{
                font-size: 22px;
                font-weight: 600;
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            .commit-card {{
                border: 1px solid #ddd;
                border-radius: 10px;
                margin-bottom: 30px;
                padding: 20px;
                background-color: #fdfdfd;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}
            .commit-title {{
                font-size: 20px;
                font-weight: 600;
                color: #43a047;
                margin-top: 0;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #eee;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .section:last-child {{
                margin-bottom: 0;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: 600;
                color: #0052d4;
                margin-top: 0;
                margin-bottom: 15px;
            }}
            .commit-details p {{
                margin: 5px 0;
                font-size: 15px;
                color: #555;
                word-break: break-all;
            }}
            .commit-details strong {{
                color: #333;
                min-width: 100px;
                display: inline-block;
            }}
            .repo-link {{
                color: #007bff;
                text-decoration: none;
            }}
            .repo-link:hover {{
                text-decoration: underline;
            }}
            .commit-message blockquote {{
                margin: 0;
                padding: 15px;
                background-color: #f8f9fa;
                border-left: 4px solid #43a047;
                font-style: italic;
                color: #555;
                border-radius: 0 5px 5px 0;
            }}
            .diff-block {{
                background-color: #0d1117; /* GitHub Dark BG */
                color: #c9d1d9; /* GitHub Dark Text */
                padding: 20px;
                border-radius: 8px;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                font-size: 14px;
                line-height: 1.5;
                overflow-x: auto;
            }}
            .diff-line {{ white-space: pre; }}
            .diff-line.add {{ color: #3fb950; }}
            .diff-line.del {{ color: #f85149; }}
            .diff-line.info {{ color: #a371f7; }}
            .diff-line.header {{ color: #58a6ff; font-weight: bold;}}
            .email-footer {{
                text-align: center;
                padding: 20px;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>TE Git 仓库提交记录</h1>
            </div>
            <div class="email-content">
                <h2 class="summary-title">发现 {num_commits} 条新提交</h2>
                {all_commits_content}
            </div>
            <div class="email-footer">
                This is an automated notification from TE Server.
            </div>
        </div>
    </body>
    </html>
    '''
    return html_template

def send_email(html_content):
    """
    配置并发送邮件。
    """
    # --- 请在这里配置您的邮件信息 ---
    mail_host = '10.196.2.20'
    sender = 'Charles.Miao@luxshare-ict.com'
    receivers = ['Charles.Miao@luxshare-ict.com', 'David.Ge2@luxshare-ict.com']
    # --------------------------------

    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = ', '.join(receivers)
    message['Subject'] = 'Git Commit Notifier'

    # 附加 HTML 正文
    html_part = MIMEText(html_content, 'html', 'utf-8')
    message.attach(html_part)

    try:
        # 登录并发送
        with smtplib.SMTP(mail_host, 25) as smtp_server:
            smtp_server.sendmail(sender, receivers, message.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

def main():
    """
    主执行函数
    """
    file_path = r'D:\ServerJobs\CheckGit\git_send.txt'
    separator = '---------------------Author/ Commit Date/ Current Ver-------------------'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 1. 按分隔符分割文件内容
        content_blocks = file_content.split(separator)
        
        # 2. 循环解析每个提交块
        parsed_commits = []
        for block in content_blocks:
            if block.strip():  # 确保块不为空或仅包含空白字符
                parsed_data = parse_git_log(block)
                parsed_commits.append(parsed_data)
        
        if not parsed_commits:
            print("No valid commit blocks found in the file.")
            return

        # 3. 创建 HTML 邮件正文
        html_body = create_html_body(parsed_commits)
        
        # 4. 发送邮件
        send_email(html_body)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == "__main__":
    main()