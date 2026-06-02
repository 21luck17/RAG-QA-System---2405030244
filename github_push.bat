@echo off
chcp 65001 >nul
echo ========================================
echo RAG智能问答系统 - GitHub推送脚本
echo ========================================
echo.

echo [前提条件]
echo 1. 已安装 Git
echo 2. 已创建 GitHub 账户
echo 3. 已安装 Ollama 并下载模型
echo.

echo 请在GitHub上创建新仓库，仓库名称格式为：
echo RAG-QA-System-姓名-学号
echo 例如：RAG-QA-System-张三-2025011
echo.

echo 请输入您的GitHub用户名：
set /p GITHUB_USER=
echo.

echo 请输入仓库名称（不含空格）：
set /p REPO_NAME=
echo.

echo 请输入您的姓名和学号（用于项目命名）：
set /p USER_INFO=
echo.

echo [1/6] 正在初始化Git仓库...
git init
git config user.name "%GITHUB_USER%"
git config user.email "%GITHUB_USER%@users.noreply.github.com"

echo [2/6] 正在添加文件...
git add .

echo [3/6] 正在提交...
git commit -m "Initial commit: RAG智能问答系统"

echo [4/6] 正在添加远程仓库...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo [5/6] 正在重命名分支...
git branch -M main

echo [6/6] 正在推送到GitHub...
git push -u origin main

echo.
echo ========================================
echo 推送完成！
echo ========================================
echo.
echo 仓库地址：https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause