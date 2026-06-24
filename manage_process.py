import os
import subprocess
import sys

def check_processes():
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split('\n')
        python_procs = [line for line in lines if 'python.exe' in line.lower()]
        if python_procs:
            print("运行中的Python进程:")
            for proc in python_procs:
                parts = proc.split()
                if len(parts) >= 2:
                    pid = parts[1]
                    print(f"  PID: {pid}")
            return [parts[1] for parts in [p.split() for p in python_procs] if len(parts) >= 2]
        else:
            print("没有运行中的Python进程")
            return []
    except Exception as e:
        print(f"检查进程失败: {e}")
        return []

def kill_process(pid):
    try:
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True, timeout=5)
        print(f"已停止 PID: {pid}")
    except Exception as e:
        print(f"停止进程失败 {pid}: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("进程管理工具")
    print("=" * 50)
    
    procs = check_processes()
    
    if procs:
        print("\n停止所有Python进程...")
        for pid in procs:
            kill_process(pid)
        
        print("\n重新启动RAG系统...")
        subprocess.Popen([sys.executable, 'run_background.py'], cwd=os.getcwd())
        print("系统已重新启动，等待10秒后访问 http://localhost:8505")
    else:
        print("\n启动RAG系统...")
        subprocess.Popen([sys.executable, 'run_background.py'], cwd=os.getcwd())
        print("系统已启动，等待10秒后访问 http://localhost:8505")