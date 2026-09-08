#!/usr/bin/env python3
import os
import subprocess
import sys

def compress_video(input_path, output_path):
    """使用ffmpeg压缩视频到适合网页播放的大小"""
    
    # 检查文件大小
    file_size = os.path.getsize(input_path)
    size_mb = file_size / (1024 * 1024)
    print(f"原视频大小: {size_mb:.1f} MB")
    
    if size_mb <= 100:
        print("视频已经在100MB以下，无需压缩")
        return
    
    # 计算目标比特率 (目标80MB)
    target_size_mb = 80
    # 获取视频时长
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', input_path],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        print(f"视频时长: {duration:.1f} 秒")
    except:
        duration = 60  # 默认60秒
        print(f"无法获取时长，假设为 {duration} 秒")
    
    # 计算视频比特率 (bytes per second)
    # 目标大小 - 音频大小(假设128k) / 时长
    target_video_bitrate = (target_size_mb * 1024 * 1024 * 8 / duration) - 128000
    target_video_bitrate = max(target_video_bitrate, 500000)  # 最小500k
    
    print(f"目标视频比特率: {target_video_bitrate/1000:.0f} kbps")
    
    # 压缩命令
    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264',
        '-b:v', f'{int(target_video_bitrate)}',
        '-preset', 'medium',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y',  # 覆盖输出文件
        output_path
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"压缩完成! 新大小: {new_size:.1f} MB")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 未找到 ffmpeg，请先安装 ffmpeg")
        print("安装方法: brew install ffmpeg")
        sys.exit(1)

if __name__ == '__main__':
    input_file = "11行咗未/11.MP4"
    output_file = "11行咗未/11_compressed.mp4"
    compress_video(input_file, output_file)
