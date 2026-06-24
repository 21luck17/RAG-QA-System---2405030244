@echo off
chcp 65001 >nul
echo ========================================
echo RAG智能问答系统 - 打包脚本
echo ========================================
echo.

if not exist "venv" (
    echo [错误] 请先运行 install.bat 安装依赖
    pause
    exit /b 1
)

echo [1/3] 正在激活虚拟环境...
call venv\Scripts\activate

echo.
echo [2/3] 正在安装 pyinstaller...
pip install pyinstaller

echo.
echo [3/3] 正在打包应用...
pyinstaller app.spec --clean

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo exe文件位于: dist\RAG-QA-System.exe
echo.
echo 注意事项：
echo 1. 运行exe前请确保已安装Ollama
echo 2. 首次运行需要下载qwen2:0.5b模型和nomic-embed-text嵌入模型
echo 3. 模型文件较大，首次启动可能需要几分钟
echo.
pause