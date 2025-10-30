"""
PR #6: 資料庫查詢優化
作者: Frank（初級工程師）
AI 工具: GitHub Copilot

功能描述:
獲取專案及其所有任務的詳細資訊。
"""

from fastapi import FastAPI
from typing import List

app = FastAPI()

# AI 生成的程式碼
@app.get("/api/v1/projects/{project_id}")
def get_project_with_tasks(project_id):
    # 查詢專案
    project = db.execute(
        f"SELECT * FROM projects WHERE id = {project_id}"
    )

    if not project:
        return None

    # 查詢任務
    tasks = []
    for task_id in project[0]['task_ids']:
        task = db.execute(
            f"SELECT * FROM tasks WHERE id = {task_id}"
        )
        if task:
            # 查詢任務的負責人
            user = db.execute(
                f"SELECT * FROM users WHERE id = {task[0]['assignee_id']}"
            )
            task[0]['assignee'] = user[0] if user else None

            # 查詢任務的評論
            comments = db.execute(
                f"SELECT * FROM comments WHERE task_id = {task_id}"
            )
            task[0]['comments'] = comments

            tasks.append(task[0])

    project[0]['tasks'] = tasks
    return project[0]


# Frank 的註解：
# "這個函數很完整，獲取了專案的所有相關資料！"
