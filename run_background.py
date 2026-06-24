import subprocess
import sys
import os
import time

def start_streamlit():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.headless", "true",
        "--server.port", "8505",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ]
    
    log_file = open("streamlit_output.log", "w", encoding="utf-8")
    
    proc = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    print(f"Streamlit 启动中，PID: {proc.pid}")
    print("等待10秒...")
    time.sleep(10)
    
    if proc.poll() is None:
        print("✅ Streamlit 运行中")
        print("访问地址: http://localhost:8505")
    else:
        print(f"❌ 启动失败，退出码: {proc.returncode}")
        log_file.close()
        with open("streamlit_output.log", "r", encoding="utf-8") as f:
            print(f.read())
        return None
    
    log_file.close()
    return proc

if __name__ == "__main__":
    proc = start_streamlit()
    if proc:
        print("\n后台运行中，脚本退出后服务继续运行...")
        print(f"停止命令: taskkill /F /PID {proc.pid}")