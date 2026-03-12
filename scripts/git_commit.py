"""
Git自动提交脚本
支持手动触发Git提交和推送
"""

import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional


def run_git_command(args: list, cwd: Path = None) -> tuple:
    """运行Git命令"""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd or Path.cwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_status() -> dict:
    """获取Git状态"""
    success, stdout, stderr = run_git_command(["status", "--porcelain"])
    
    if not success:
        return {"error": stderr}
    
    changes = []
    if stdout.strip():
        for line in stdout.strip().split('\n'):
            if len(line) >= 3:
                status = line[:2].strip()
                file = line[3:]
                changes.append({"status": status, "file": file})
    
    return {
        "has_changes": bool(changes),
        "changes": changes,
        "count": len(changes)
    }


def get_branch() -> str:
    """获取当前分支"""
    success, stdout, stderr = run_git_command(["branch", "--show-current"])
    return stdout.strip() if success else "unknown"


def commit(message: Optional[str] = None, scenario: str = None) -> dict:
    """执行Git提交"""
    
    status = get_status()
    if not status.get("has_changes"):
        return {"success": False, "message": "没有需要提交的更改"}
    
    if not message:
        if scenario:
            message = f"feat: 完成{scenario}"
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            message = f"chore: 自动提交 {timestamp}"
    
    success, stdout, stderr = run_git_command(["add", "."])
    if not success:
        return {"success": False, "message": f"git add 失败: {stderr}"}
    
    success, stdout, stderr = run_git_command(["commit", "-m", message])
    if not success:
        return {"success": False, "message": f"git commit 失败: {stderr}"}
    
    return {
        "success": True,
        "message": message,
        "files_changed": status["count"],
        "branch": get_branch()
    }


def push() -> dict:
    """推送到远程仓库"""
    branch = get_branch()
    
    success, stdout, stderr = run_git_command(["push", "origin", branch])
    
    if success:
        return {"success": True, "message": f"已推送到 origin/{branch}"}
    else:
        return {"success": False, "message": f"推送失败: {stderr}"}


def commit_and_push(message: Optional[str] = None, scenario: str = None) -> dict:
    """提交并推送"""
    result = commit(message, scenario)
    
    if result.get("success"):
        push_result = push()
        result["push"] = push_result
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Git自动提交工具")
    parser.add_argument("action", choices=["status", "commit", "push", "sync"], 
                       help="执行的操作")
    parser.add_argument("-m", "--message", help="提交消息")
    parser.add_argument("-s", "--scenario", help="场景名称")
    
    args = parser.parse_args()
    
    if args.action == "status":
        status = get_status()
        print(f"当前分支: {get_branch()}")
        print(f"更改数量: {status['count']}")
        if status["changes"]:
            print("\n更改文件:")
            for change in status["changes"]:
                print(f"  {change['status']} {change['file']}")
    
    elif args.action == "commit":
        result = commit(args.message, args.scenario)
        if result["success"]:
            print(f"✅ 提交成功: {result['message']}")
            print(f"   文件数: {result['files_changed']}")
        else:
            print(f"❌ {result['message']}")
    
    elif args.action == "push":
        result = push()
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
    
    elif args.action == "sync":
        result = commit_and_push(args.message, args.scenario)
        if result["success"]:
            print(f"✅ 提交成功: {result['message']}")
            if result.get("push", {}).get("success"):
                print(f"✅ 推送成功")
            else:
                print(f"⚠️ 推送失败: {result.get('push', {}).get('message')}")
        else:
            print(f"❌ {result['message']}")


if __name__ == "__main__":
    main()
