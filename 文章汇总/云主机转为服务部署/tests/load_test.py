import requests
import time
import json
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Any
import argparse

class LoadTestResult:
    """负载测试结果类"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, success: bool, response_time: float, error: str = None):
        """添加测试结果"""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            self.response_times.append(response_time)
        else:
            self.failed_requests += 1
            if error:
                self.errors.append(error)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.response_times:
            return {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "success_rate": 0,
                "avg_response_time": 0,
                "min_response_time": 0,
                "max_response_time": 0,
                "median_response_time": 0,
                "p95_response_time": 0,
                "test_duration": 0,
                "requests_per_second": 0
            }
        
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (self.successful_requests / self.total_requests) * 100,
            "avg_response_time": statistics.mean(self.response_times),
            "min_response_time": min(self.response_times),
            "max_response_time": max(self.response_times),
            "median_response_time": statistics.median(self.response_times),
            "p95_response_time": statistics.quantiles(self.response_times, n=20)[18] if len(self.response_times) >= 20 else max(self.response_times),
            "test_duration": duration,
            "requests_per_second": self.total_requests / duration if duration > 0 else 0
        }

class APILoadTester:
    """API负载测试器"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'LoadTester/1.0'
        })
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None, timeout: int = 30) -> Dict[str, Any]:
        """测试单个端点"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=timeout)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=timeout)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response_time = time.time() - start_time
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "response_time": response_time,
                "response_size": len(response.content),
                "endpoint": endpoint,
                "method": method,
                "error": None
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "response_size": 0,
                "endpoint": endpoint,
                "method": method,
                "error": str(e)
            }
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            result = self.test_endpoint("/", "GET")
            return result["success"]
        except:
            return False
    
    def run_load_test(self, 
                      test_scenarios: List[Dict], 
                      concurrent_users: int = 10, 
                      test_duration: int = 60,
                      ramp_up_time: int = 10) -> LoadTestResult:
        """运行负载测试"""
        
        print(f"🚀 开始负载测试")
        print(f"📊 测试配置:")
        print(f"   - 并发用户数: {concurrent_users}")
        print(f"   - 测试时长: {test_duration}秒")
        print(f"   - 爬坡时间: {ramp_up_time}秒")
        print(f"   - 目标URL: {self.base_url}")
        
        # 健康检查
        if not self.health_check():
            print("❌ 健康检查失败，服务不可用")
            return LoadTestResult()
        
        print("✅ 健康检查通过")
        
        result = LoadTestResult()
        result.start_time = datetime.now()
        
        def worker(worker_id: int):
            """工作线程"""
            start_delay = (worker_id / concurrent_users) * ramp_up_time
            time.sleep(start_delay)
            
            worker_start_time = time.time()
            request_count = 0
            
            while time.time() - worker_start_time < test_duration:
                # 随机选择测试场景
                scenario = test_scenarios[request_count % len(test_scenarios)]
                
                test_result = self.test_endpoint(
                    scenario["endpoint"],
                    scenario.get("method", "GET"),
                    scenario.get("data"),
                    scenario.get("timeout", 30)
                )
                
                result.add_result(
                    test_result["success"],
                    test_result["response_time"],
                    test_result["error"]
                )
                
                request_count += 1
                
                # 请求间隔
                if "delay" in scenario:
                    time.sleep(scenario["delay"])
        
        # 启动并发测试
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker, i) for i in range(concurrent_users)]
            
            # 等待所有测试完成
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"⚠️ 工作线程异常: {e}")
        
        result.end_time = datetime.now()
        return result

def create_test_scenarios(base_url: str) -> List[Dict]:
    """创建测试场景"""
    scenarios = [
        {
            "name": "健康检查",
            "endpoint": "/",
            "method": "GET",
            "weight": 10
        },
        {
            "name": "获取用户列表",
            "endpoint": "/users",
            "method": "GET",
            "weight": 30
        },
        {
            "name": "获取用户统计",
            "endpoint": "/stats",
            "method": "GET", 
            "weight": 10
        },
        {
            "name": "获取特定用户",
            "endpoint": "/users/1",
            "method": "GET",
            "weight": 20
        },
        {
            "name": "搜索用户",
            "endpoint": "/users/search/张",
            "method": "GET",
            "weight": 15
        },
        {
            "name": "创建用户",
            "endpoint": "/users",
            "method": "POST",
            "data": {
                "name": f"负载测试用户{time.time()}",
                "email": f"loadtest{time.time()}@example.com",
                "age": 25
            },
            "weight": 10
        },
        {
            "name": "年龄范围查询",
            "endpoint": "/users/age-range/20/30",
            "method": "GET",
            "weight": 5
        }
    ]
    
    # 根据权重扩展场景
    weighted_scenarios = []
    for scenario in scenarios:
        weight = scenario.get("weight", 1)
        for _ in range(weight):
            weighted_scenarios.append(scenario)
    
    return weighted_scenarios

def print_test_results(result: LoadTestResult):
    """打印测试结果"""
    stats = result.get_statistics()
    
    print("\n" + "="*60)
    print("📊 负载测试结果报告")
    print("="*60)
    
    print(f"📈 请求统计:")
    print(f"   总请求数:     {stats['total_requests']:,}")
    print(f"   成功请求:     {stats['successful_requests']:,}")
    print(f"   失败请求:     {stats['failed_requests']:,}")
    print(f"   成功率:       {stats['success_rate']:.2f}%")
    
    print(f"\n⏱️ 性能指标:")
    print(f"   测试时长:     {stats['test_duration']:.2f}秒")
    print(f"   请求/秒:      {stats['requests_per_second']:.2f}")
    print(f"   平均响应时间: {stats['avg_response_time']*1000:.2f}ms")
    print(f"   最小响应时间: {stats['min_response_time']*1000:.2f}ms")
    print(f"   最大响应时间: {stats['max_response_time']*1000:.2f}ms")
    print(f"   中位数响应时间: {stats['median_response_time']*1000:.2f}ms")
    print(f"   95%响应时间:  {stats['p95_response_time']*1000:.2f}ms")
    
    if result.errors:
        print(f"\n❌ 错误信息 (显示前10个):")
        for i, error in enumerate(result.errors[:10]):
            print(f"   {i+1}. {error}")
        if len(result.errors) > 10:
            print(f"   ... 还有 {len(result.errors)-10} 个错误")
    
    # 性能评级
    avg_time_ms = stats['avg_response_time'] * 1000
    if avg_time_ms < 100:
        grade = "🚀 优秀"
    elif avg_time_ms < 200:
        grade = "✅ 良好"
    elif avg_time_ms < 500:
        grade = "⚠️ 一般"
    else:
        grade = "❌ 需要优化"
    
    print(f"\n🎯 性能评级: {grade}")
    print("="*60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="API负载测试工具")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="API基础URL (默认: http://localhost:8000)")
    parser.add_argument("--users", type=int, default=10, 
                       help="并发用户数 (默认: 10)")
    parser.add_argument("--duration", type=int, default=60, 
                       help="测试持续时间(秒) (默认: 60)")
    parser.add_argument("--ramp-up", type=int, default=10, 
                       help="爬坡时间(秒) (默认: 10)")
    
    args = parser.parse_args()
    
    # 创建测试器
    tester = APILoadTester(args.url)
    
    # 创建测试场景
    scenarios = create_test_scenarios(args.url)
    
    # 运行测试
    result = tester.run_load_test(
        scenarios, 
        concurrent_users=args.users,
        test_duration=args.duration,
        ramp_up_time=args.ramp_up
    )
    
    # 打印结果
    print_test_results(result)
    
    # 保存结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"load_test_result_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "test_config": {
                "base_url": args.url,
                "concurrent_users": args.users,
                "test_duration": args.duration,
                "ramp_up_time": args.ramp_up
            },
            "results": result.get_statistics(),
            "errors": result.errors
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {filename}")

if __name__ == "__main__":
    main() 