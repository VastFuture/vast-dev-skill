#!/usr/bin/env python3
"""
SenseNova U1 Fast 批量测试脚本

测试所有支持的尺寸比例
"""

import os
import sys
import requests
import json
from datetime import datetime
from pathlib import Path


def _config_path() -> Path:
    return Path.home() / ".sensenova" / "config.yml"


def load_config():
    """加载配置，优先级：环境变量 > 用户配置文件"""
    try:
        import yaml
    except ImportError:
        return {"api_key": os.getenv("SENSENOVA_API_KEY", ""), "default_size": "2752x1536"}

    config = {"api_key": "", "default_size": "2752x1536",
              "output_dir": str(Path.home() / "Pictures" / "sensenova")}
    config_path = _config_path()
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            config.update({k: v for k, v in user_config.items() if v})
    if os.getenv("SENSENOVA_API_KEY"):
        config["api_key"] = os.getenv("SENSENOVA_API_KEY")
    return config


def test_sensenova_u1_fast():
    """测试 SenseNova U1 Fast 图像生成接口"""
    
    # 加载配置（环境变量 > 配置文件）
    config = load_config()
    api_key = config["api_key"]

    if not api_key:
        config_path = _config_path()
        if not config_path.exists():
            print("[INFO] 首次使用，请先运行 generate_infographic.py 初始化配置文件")
        else:
            print(f"[ERROR] API Key 未填写，请编辑: {config_path}")
            print(f"   获取免费 API Key: https://platform.sensenova.cn/console")
        sys.exit(1)

    print("[OK] API Key 已加载")
    
    # 2. 准备请求参数
    url = "https://token.sensenova.cn/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 测试用的 prompt
    test_prompt = """
    这张信息图展示了"AI代码助手"的核心能力。采用现代扁平设计风格,以蓝色和绿色为主色调。
    整体布局分为三个部分:
    
    1. 左侧区域 - 核心功能:
       - 代码生成与补全
       - 错误诊断与修复  
       - 代码审查与优化
       
    2. 中间区域 - 工作流程:
       - 步骤1: 理解需求
       - 步骤2: 生成代码
       - 步骤3: 测试验证
       
    3. 右侧区域 - 技术优势:
       - 支持30+编程语言
       - 实时上下文理解
       - 安全可靠的代码生成
    """
    
    # 测试所有支持的尺寸
    sizes = [
        ("2752x1536", "16:9"),  # 默认尺寸
        ("2048x2048", "1:1"),   # 正方形
        ("1664x2496", "2:3"),   # 竖版
        ("2496x1664", "3:2"),   # 横版
    ]
    
    # 3. 开始测试
    print("\n" + "="*60)
    print("开始测试 SenseNova U1 Fast 图像生成接口")
    print("="*60)
    
    results = []
    
    for size, ratio in sizes:
        print(f"\n[INFO] 测试尺寸: {size} (比例 {ratio})")
        
        payload = {
            "model": "sensenova-u1-fast",
            "prompt": test_prompt.strip(),
            "size": size,
            "n": 1
        }
        
        try:
            # 发送请求
            print("   发送请求中...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # 检查响应状态
            if response.status_code == 200:
                data = response.json()
                
                if "data" in data and len(data["data"]) > 0:
                    image_url = data["data"][0]["url"]
                    created_time = datetime.fromtimestamp(data["created"]).strftime("%Y-%m-%d %H:%M:%S")
                    
                    print(f"   [OK] 生成成功!")
                    print(f"   创建时间: {created_time}")
                    print(f"   图片URL: {image_url}")
                    print(f"   [!] 注意: URL有效期仅1小时")
                    
                    results.append({
                        "size": size,
                        "ratio": ratio,
                        "success": True,
                        "url": image_url,
                        "created": created_time
                    })
                    
                    # 尝试下载图片保存到本地
                    try:
                        img_response = requests.get(image_url, timeout=30)
                        if img_response.status_code == 200:
                            # 创建输出目录
                            output_dir = Path("test_outputs")
                            output_dir.mkdir(parents=True, exist_ok=True)
                            
                            # 保存图片
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"sensenova_u1_fast_{size}_{timestamp}.png"
                            filepath = output_dir / filename
                            
                            with open(filepath, "wb") as f:
                                f.write(img_response.content)
                            
                            print(f"   [OK] 图片已保存: {filepath}")
                            results[-1]["local_file"] = str(filepath)
                    except Exception as e:
                        print(f"   [WARN] 下载图片失败: {e}")
                        
                else:
                    print(f"   [ERROR] 响应数据格式异常: {data}")
                    results.append({
                        "size": size,
                        "ratio": ratio,
                        "success": False,
                        "error": "响应数据格式异常"
                    })
            else:
                error_msg = response.text
                print(f"   [ERROR] 请求失败 (HTTP {response.status_code})")
                print(f"   错误信息: {error_msg}")
                results.append({
                    "size": size,
                    "ratio": ratio,
                    "success": False,
                    "error": error_msg
                })
                
        except requests.exceptions.Timeout:
            print(f"   [ERROR] 请求超时")
            results.append({
                "size": size,
                "ratio": ratio,
                "success": False,
                "error": "请求超时"
            })
        except Exception as e:
            print(f"   [ERROR] 发生异常: {e}")
            results.append({
                "size": size,
                "ratio": ratio,
                "success": False,
                "error": str(e)
            })
    
    # 4. 输出测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"\n总测试数: {total_count}")
    print(f"成功: {success_count}")
    print(f"失败: {total_count - success_count}")
    
    if success_count > 0:
        print("\n[OK] 成功的测试:")
        for r in results:
            if r["success"]:
                print(f"   - {r['size']} ({r['ratio']})")
                if "local_file" in r:
                    print(f"     文件: {r['local_file']}")
    
    if success_count < total_count:
        print("\n[ERROR] 失败的测试:")
        for r in results:
            if not r["success"]:
                print(f"   - {r['size']} ({r['ratio']}): {r['error']}")
    
    # 5. 保存测试报告
    report_dir = Path("test_outputs")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "total": total_count,
            "success": success_count,
            "failed": total_count - success_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 测试报告已保存: {report_file}")
    
    return success_count == total_count


if __name__ == "__main__":
    success = test_sensenova_u1_fast()
    sys.exit(0 if success else 1)
