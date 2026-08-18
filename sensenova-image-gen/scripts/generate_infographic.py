#!/usr/bin/env python3
"""
SenseNova U1 Fast 信息图生成脚本

使用商汤 SenseNova U1 Fast API 生成专业信息图
"""

import os
import sys
import argparse
import requests
import json
from datetime import datetime
from pathlib import Path


def _config_path() -> Path:
    """返回所有平台共用的用户配置文件路径。"""
    return Path.home() / ".sensenova" / "config.yml"


def _default_output_dir() -> Path:
    """跨平台默认图片输出目录。"""
    return Path.home() / "Pictures" / "sensenova"


def load_config():
    """加载配置，优先级：环境变量 > 用户配置文件"""
    import yaml

    config = {
        "api_key": "",
        "default_size": "2752x1536",
        "output_dir": str(_default_output_dir()),
    }

    config_path = _config_path()
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            config.update({k: v for k, v in user_config.items() if v})

    # 环境变量优先级最高
    if os.getenv("SENSENOVA_API_KEY"):
        config["api_key"] = os.getenv("SENSENOVA_API_KEY")

    return config


def init_config():
    """首次使用时创建配置文件并引导用户填写"""
    import shutil
    config_path = _config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    template = Path(__file__).parent.parent / "config.template.yml"
    shutil.copy(template, config_path)

    print(f"[OK] 配置文件已创建: {config_path}")
    print(f"\n请编辑配置文件填写你的 API Key:")
    print(f"  获取免费 API Key: https://platform.sensenova.cn/console")
    print("\n请使用文本编辑器打开该文件。")
    print(f"\n填写完成后重新运行即可。")


def generate_infographic(prompt, size="2752x1536", output=None, save_report=False):
    """
    生成信息图
    
    Args:
        prompt: 图像描述文本
        size: 图像尺寸，默认 2752x1536 (16:9)
        output: 输出文件路径，默认自动生成
        save_report: 是否保存详细报告
    
    Returns:
        生成结果字典
    """
    
    # 加载配置（环境变量 > 配置文件）
    config = load_config()
    api_key = config["api_key"]

    if not api_key:
        config_path = _config_path()
        if not config_path.exists():
            print("[INFO] 首次使用，正在初始化配置文件...")
            init_config()
        else:
            print(f"[ERROR] API Key 未填写，请编辑: {config_path}")
            print(f"   获取免费 API Key: https://platform.sensenova.cn/console")
        sys.exit(1)

    # 使用配置文件中的默认值（参数未指定时）
    if size == "2752x1536":
        size = config.get("default_size", size)
    if output is None:
        output_dir = Path(config.get("output_dir", str(_default_output_dir()))).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = str(output_dir / f"infographic_{size}_{timestamp}.png")
    
    # 准备请求
    url = "https://token.sensenova.cn/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sensenova-u1-fast",
        "prompt": prompt,
        "size": size,
        "n": 1
    }
    
    print("[INFO] 开始生成信息图...")
    print(f"   尺寸: {size}")
    print(f"   Prompt 长度: {len(prompt)} 字符")
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and len(data["data"]) > 0:
                image_url = data["data"][0]["url"]
                created_time = datetime.fromtimestamp(data["created"]).strftime("%Y-%m-%d %H:%M:%S")
                
                print("[OK] 生成成功!")
                print(f"   创建时间: {created_time}")
                print("   [!] URL 有效期: 1 小时")
                
                # 下载图片
                print("[INFO] 正在下载图片...")
                img_response = requests.get(image_url, timeout=30)
                
                if img_response.status_code == 200:
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    
                    file_size = output_path.stat().st_size / (1024 * 1024)
                    print(f"[OK] 图片已保存: {output_path}")
                    print(f"   文件大小: {file_size:.2f} MB")
                    
                    result = {
                        "success": True,
                        "file": str(output_path),
                        "size": size,
                        "created": created_time,
                        "url": image_url,
                        "file_size_mb": round(file_size, 2)
                    }
                    
                    # 保存报告
                    if save_report:
                        report_path = output_path.with_suffix('.json')
                        with open(report_path, "w", encoding="utf-8") as f:
                            json.dump(result, f, ensure_ascii=False, indent=2)
                        print(f"[OK] 报告已保存: {report_path}")
                    
                    return result
                else:
                    print(f"[ERROR] 下载图片失败 (HTTP {img_response.status_code})")
                    return {"success": False, "error": "下载失败"}
            else:
                print("[ERROR] 响应数据格式异常")
                return {"success": False, "error": "响应格式异常"}
        else:
            error_msg = response.text
            print(f"[ERROR] 请求失败 (HTTP {response.status_code})")
            print(f"   错误: {error_msg}")
            return {"success": False, "error": error_msg}
            
    except requests.exceptions.Timeout:
        print("[ERROR] 请求超时")
        return {"success": False, "error": "请求超时"}
    except Exception as e:
        print(f"[ERROR] 发生异常: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="SenseNova U1 Fast 信息图生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从命令行传入 prompt
  %(prog)s --prompt "AI技术发展历程信息图" --size "2752x1536"
  
  # 从文件读取 prompt
  %(prog)s --prompt-file prompt.txt --output my_infographic.png
  
  # 保存详细报告
  %(prog)s --prompt "数据分析流程图" --save-report

支持的尺寸:
  2752x1536 (16:9), 1536x2752 (9:16), 2048x2048 (1:1)
  2496x1664 (3:2), 1664x2496 (2:3), 2272x1824 (5:4)
  1824x2272 (4:5), 2368x1760 (4:3), 1760x2368 (3:4)
  3072x1376 (21:9), 1344x3136 (9:21)
        """
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="图像描述文本"
    )
    
    parser.add_argument(
        "--prompt-file",
        type=str,
        help="从文件读取 prompt"
    )
    
    parser.add_argument(
        "--size",
        type=str,
        default="2752x1536",
        help="图像尺寸，默认 2752x1536 (16:9)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径，默认自动生成"
    )
    
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="保存详细报告为 JSON 文件"
    )
    
    args = parser.parse_args()
    
    # 获取 prompt
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("[ERROR] 必须提供 --prompt 或 --prompt-file 参数")
        parser.print_help()
        sys.exit(1)
    
    # 生成信息图
    result = generate_infographic(
        prompt=prompt,
        size=args.size,
        output=args.output,
        save_report=args.save_report
    )
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
