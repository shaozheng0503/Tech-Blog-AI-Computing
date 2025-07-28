from typing import List

class Solution:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        """
        行相等的最少多米诺旋转
        
        解题思路：
        1. 首先确定可能的目标值（只能是 tops[0] 或 bottoms[0]）
        2. 对于每个可能的目标值，计算使 tops 或 bottoms 全部相等所需的最小旋转次数
        3. 返回所有可能情况中的最小值，如果都不可能则返回 -1
        
        时间复杂度：O(n)
        空间复杂度：O(1)
        """
        n = len(tops)
        
        # 可能的目标值只能是第一个骨牌的两个数字
        candidates = {tops[0], bottoms[0]}
        
        min_rotations = float('inf')
        
        for target in candidates:
            # 计算使 tops 全部等于 target 的旋转次数
            rotations_for_tops = self.count_rotations(tops, bottoms, target, True)
            
            # 计算使 bottoms 全部等于 target 的旋转次数
            rotations_for_bottoms = self.count_rotations(tops, bottoms, target, False)
            
            # 取较小值
            if rotations_for_tops != -1:
                min_rotations = min(min_rotations, rotations_for_tops)
            if rotations_for_bottoms != -1:
                min_rotations = min(min_rotations, rotations_for_bottoms)
        
        return min_rotations if min_rotations != float('inf') else -1
    
    def count_rotations(self, tops: List[int], bottoms: List[int], target: int, make_tops_equal: bool) -> int:
        """
        计算使指定行全部等于目标值所需的旋转次数
        
        Args:
            tops: 上半部分数组
            bottoms: 下半部分数组
            target: 目标值
            make_tops_equal: True 表示使 tops 相等，False 表示使 bottoms 相等
        
        Returns:
            所需的最小旋转次数，如果不可能则返回 -1
        """
        rotations = 0
        n = len(tops)
        
        for i in range(n):
            if make_tops_equal:
                # 要使 tops 等于 target
                if tops[i] == target:
                    # 当前 tops[i] 已经是目标值，不需要旋转
                    continue
                elif bottoms[i] == target:
                    # 需要旋转，使 bottoms[i] 变成 tops[i]
                    rotations += 1
                else:
                    # 两个都不是目标值，无法达到目标
                    return -1
            else:
                # 要使 bottoms 等于 target
                if bottoms[i] == target:
                    # 当前 bottoms[i] 已经是目标值，不需要旋转
                    continue
                elif tops[i] == target:
                    # 需要旋转，使 tops[i] 变成 bottoms[i]
                    rotations += 1
                else:
                    # 两个都不是目标值，无法达到目标
                    return -1
        
        return rotations


class SolutionOptimized:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        """
        优化版本：一次遍历解决
        
        解题思路：
        1. 统计每个数字在 tops 和 bottoms 中出现的次数
        2. 对于每个数字，计算使 tops 或 bottoms 全部等于该数字所需的旋转次数
        3. 返回所有可能情况中的最小值
        """
        n = len(tops)
        
        # 统计每个数字在 tops 和 bottoms 中出现的次数
        count_tops = [0] * 7
        count_bottoms = [0] * 7
        count_same = [0] * 7  # 统计 tops[i] == bottoms[i] 的情况
        
        for i in range(n):
            count_tops[tops[i]] += 1
            count_bottoms[bottoms[i]] += 1
            if tops[i] == bottoms[i]:
                count_same[tops[i]] += 1
        
        min_rotations = float('inf')
        
        # 检查每个数字（1-6）是否可以作为目标值
        for target in range(1, 7):
            # 要使 tops 全部等于 target
            if count_tops[target] + count_bottoms[target] - count_same[target] == n:
                # 需要旋转的次数 = n - count_tops[target]
                rotations = n - count_tops[target]
                min_rotations = min(min_rotations, rotations)
            
            # 要使 bottoms 全部等于 target
            if count_tops[target] + count_bottoms[target] - count_same[target] == n:
                # 需要旋转的次数 = n - count_bottoms[target]
                rotations = n - count_bottoms[target]
                min_rotations = min(min_rotations, rotations)
        
        return min_rotations if min_rotations != float('inf') else -1


class SolutionDetailed:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        """
        带详细调试信息的版本，帮助理解算法过程
        """
        print(f"输入 tops: {tops}")
        print(f"输入 bottoms: {bottoms}")
        print()
        
        n = len(tops)
        
        # 统计每个数字的出现次数
        count_tops = [0] * 7
        count_bottoms = [0] * 7
        count_same = [0] * 7
        
        for i in range(n):
            count_tops[tops[i]] += 1
            count_bottoms[bottoms[i]] += 1
            if tops[i] == bottoms[i]:
                count_same[tops[i]] += 1
        
        print("统计信息:")
        for i in range(1, 7):
            if count_tops[i] > 0 or count_bottoms[i] > 0:
                print(f"数字 {i}: tops={count_tops[i]}, bottoms={count_bottoms[i]}, 相同={count_same[i]}")
        print()
        
        min_rotations = float('inf')
        
        print("检查每个数字作为目标值:")
        for target in range(1, 7):
            total_occurrences = count_tops[target] + count_bottoms[target] - count_same[target]
            print(f"目标值 {target}: 总出现次数 = {total_occurrences}")
            
            if total_occurrences == n:
                # 可以使 tops 全部等于 target
                rotations_for_tops = n - count_tops[target]
                print(f"  使 tops 相等需要旋转 {rotations_for_tops} 次")
                min_rotations = min(min_rotations, rotations_for_tops)
                
                # 可以使 bottoms 全部等于 target
                rotations_for_bottoms = n - count_bottoms[target]
                print(f"  使 bottoms 相等需要旋转 {rotations_for_bottoms} 次")
                min_rotations = min(min_rotations, rotations_for_bottoms)
            else:
                print(f"  无法使任何一行全部等于 {target}")
        
        result = min_rotations if min_rotations != float('inf') else -1
        print(f"\n最终结果: {result}")
        return result


# 测试代码
def test_solution():
    """测试函数"""
    solution = Solution()
    
    # 测试用例 1
    tops1 = [2, 1, 2, 4, 2, 2]
    bottoms1 = [5, 2, 6, 2, 3, 2]
    result1 = solution.minDominoRotations(tops1, bottoms1)
    print(f"测试用例 1:")
    print(f"tops = {tops1}")
    print(f"bottoms = {bottoms1}")
    print(f"期望输出: 2, 实际输出: {result1}")
    print(f"测试结果: {'通过' if result1 == 2 else '失败'}")
    print()
    
    # 测试用例 2
    tops2 = [3, 5, 1, 2, 3]
    bottoms2 = [3, 6, 3, 3, 4]
    result2 = solution.minDominoRotations(tops2, bottoms2)
    print(f"测试用例 2:")
    print(f"tops = {tops2}")
    print(f"bottoms = {bottoms2}")
    print(f"期望输出: -1, 实际输出: {result2}")
    print(f"测试结果: {'通过' if result2 == -1 else '失败'}")
    print()
    
    # 额外测试用例
    tops3 = [1, 2, 1, 1, 1, 2, 2, 2]
    bottoms3 = [2, 1, 2, 2, 2, 1, 1, 1]
    result3 = solution.minDominoRotations(tops3, bottoms3)
    print(f"测试用例 3:")
    print(f"tops = {tops3}")
    print(f"bottoms = {bottoms3}")
    print(f"实际输出: {result3}")
    print()


if __name__ == "__main__":
    # 运行测试
    test_solution()
    
    print("=" * 50)
    print("详细版本演示:")
    solution_detailed = SolutionDetailed()
    solution_detailed.minDominoRotations([2, 1, 2, 4, 2, 2], [5, 2, 6, 2, 3, 2]) 