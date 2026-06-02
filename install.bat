@echo off
chcp 65001 >nul
echo ========================================
echo RAG智能问答系统 - 一键安装脚本
echo ========================================
echo.

echo [1/5] 正在安装 Git...
if exist "C:\Program Files\Git\bin\git.exe" (
    echo Git 已安装
) else (
    echo 请从 https://git-scm.com/download/win 下载并安装 Git
    echo 安装完成后请重新运行此脚本
    pause
    exit /b 1
)

echo [2/5] 正在安装 Ollama...
where ollama >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Ollama 已安装
) else (
    echo 请从 https://ollama.com/download 下载并安装 Ollama
    echo 安装完成后请重新运行此脚本
    pause
    exit /b 1
)

echo [3/5] 正在下载 AI 模型...
echo 这可能需要几分钟到几十分钟，取决于您的网络速度...
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text

echo [4/5] 正在安装 Python 依赖...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo [5/5] 验证安装...
python -c "import streamlit; import langchain; import chromadb; print('所有依赖安装成功！')"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 运行应用：streamlit run app.py
echo.
pause