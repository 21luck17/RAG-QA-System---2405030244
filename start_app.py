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
    
    print(f"启动Streamlit...")
    
    log_file = open("streamlit_output.log", "w", encoding="utf-8")
    
    proc = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    print(f"进程ID: {proc.pid}")
    print("等待启动 (10秒)...")
    
    time.sleep(10)
    
    if proc.poll() is None:
        print("=" * 50)
        print("✅ Streamlit 启动成功！")
        print("访问地址: http://localhost:8505")
        print("=" * 50)
    else:
        print(f"❌ Streamlit 启动失败，退出码: {proc.returncode}")
        log_file.close()
        with open("streamlit_output.log", "r", encoding="utf-8") as f:
            print("--- 日志 ---")
            print(f.read())
        return None
    
    log_file.close()
    return proc

if __name__ == "__main__":
    proc = start_streamlit()
    if proc:
        print("\n服务正在后台运行...")
        print("按 Enter 键停止服务")
        try:
            input()
        except KeyboardInterrupt:
            pass
        print("\n正在停止...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("已停止")