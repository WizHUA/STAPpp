# T3三角形单元的收敛性分析、分片试验与验证算例

现在让我们系统地进行T3单元的验证工作。我将为您创建一系列测试案例来全面验证T3单元的正确性和收敛性。

## 1. 分片试验（Patch Test）

分片试验是验证有限元单元是否能够精确表示常应变状态的基本测试。

### 1.1 常应变拉伸试验

创建一个更严格的分片试验文件：

```plaintext
T3 Patch Test - Constant Strain
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 2.0 0.0 0.0
3 0 0 1 2.0 2.0 0.0
4 1 0 1 0.0 2.0 0.0
1
4
2 1 1000.0
2 2 0.0
3 1 1000.0
3 2 0.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
```

### 1.2 纯剪切分片试验

```plaintext
T3 Patch Test - Pure Shear
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
3 2 100.0
4 2 -100.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
```

## 2. 收敛性分析

为了验证T3单元的收敛性，我们需要创建不同网格密度的悬臂梁模型。

### 2.1 粗网格悬臂梁（2x1网格）

```plaintext
T3 Cantilever Beam - Coarse Mesh
6 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 0.5 0.0
3 1 1 1 0.0 1.0 0.0
4 0 0 1 1.0 0.0 0.0
5 0 0 1 1.0 0.5 0.0
6 0 0 1 1.0 1.0 0.0
1
1
6 2 -1000.0
3 4 1
1 210000.0 0.3 1.0
1 1 4 5 1
2 1 5 2 1
3 2 5 6 1
4 2 6 3 1
```

### 2.2 中等网格悬臂梁（4x2网格）

```plaintext
T3 Cantilever Beam - Medium Mesh
15 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 0.25 0.0
3 1 1 1 0.0 0.5 0.0
4 1 1 1 0.0 0.75 0.0
5 1 1 1 0.0 1.0 0.0
6 0 0 1 0.5 0.0 0.0
7 0 0 1 0.5 0.25 0.0
8 0 0 1 0.5 0.5 0.0
9 0 0 1 0.5 0.75 0.0
10 0 0 1 0.5 1.0 0.0
11 0 0 1 1.0 0.0 0.0
12 0 0 1 1.0 0.25 0.0
13 0 0 1 1.0 0.5 0.0
14 0 0 1 1.0 0.75 0.0
15 0 0 1 1.0 1.0 0.0
1
1
15 2 -1000.0
3 16 1
1 210000.0 0.3 1.0
1 1 6 7 1
2 1 7 2 1
3 2 7 8 1
4 2 8 3 1
5 3 8 9 1
6 3 9 4 1
7 4 9 10 1
8 4 10 5 1
9 6 11 12 1
10 6 12 7 1
11 7 12 13 1
12 7 13 8 1
13 8 13 14 1
14 8 14 9 1
15 9 14 15 1
16 9 15 10 1
```

### 2.3 细网格悬臂梁（8x4网格）

类似地创建更细的网格...

## 3. 经典验证算例

### 3.1 Cook膜问题

Cook膜是一个经典的有限元验证算例，用于测试单元在大变形情况下的性能：

```plaintext
T3 Cook Membrane Problem
8 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 44.0 0.0
3 0 0 1 48.0 44.0 0.0
4 0 0 1 48.0 60.0 0.0
5 0 0 1 16.0 0.0 0.0
6 0 0 1 16.0 22.0 0.0
7 0 0 1 32.0 22.0 0.0
8 0 0 1 32.0 38.0 0.0
1
2
4 1 1.0
4 2 0.0
3 8 1
1 1.0 0.3 1.0
1 1 5 6 1
2 1 6 2 1
3 2 6 7 1
4 2 7 8 1
5 5 7 6 1
6 6 7 8 1
7 8 3 4 1
8 8 4 2 1
```

### 3.2 受集中载荷的正方形板

```plaintext
T3 Square Plate with Point Load
9 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 0.5 0.0 0.0
3 0 1 1 1.0 0.0 0.0
4 1 0 1 0.0 0.5 0.0
5 0 0 1 0.5 0.5 0.0
6 0 0 1 1.0 0.5 0.0
7 1 0 1 0.0 1.0 0.0
8 0 0 1 0.5 1.0 0.0
9 0 0 1 1.0 1.0 0.0
1
1
5 2 -1000.0
3 8 1
1 210000.0 0.3 1.0
1 1 2 5 1
2 1 5 4 1
3 2 3 6 1
4 2 6 5 1
5 4 5 8 1
6 4 8 7 1
7 5 6 9 1
8 5 9 8 1
```

## 4. 验证脚本

创建一个批处理脚本来运行所有测试案例：

```bash
#!/bin/bash
# T3单元验证测试套件

echo "=========================================="
echo "T3三角形单元验证测试套件"
echo "=========================================="

# 测试案例列表
tests=(
    "t3_patch_test.dat"
    "t3_patch_constant_strain.dat"
    "t3_patch_pure_shear.dat"
    "t3_cantilever_coarse.dat"
    "t3_cantilever_medium.dat"
    "t3_cook_membrane.dat"
    "t3_square_plate.dat"
)

# 运行所有测试
for test in "${tests[@]}"; do
    echo "------------------------------------------"
    echo "运行测试: $test"
    echo "------------------------------------------"
    
    if [ -f "../data/$test" ]; then
        ./stap++ "../data/$test" > "results_${test%.dat}.out"
        
        if [ $? -eq 0 ]; then
            echo "✅ $test 测试成功"
        else
            echo "❌ $test 测试失败"
        fi
    else
        echo "⚠️  文件 $test 不存在"
    fi
    echo ""
done

echo "=========================================="
echo "所有测试完成！"
echo "=========================================="
```

## 5. 结果分析工具

创建一个Python脚本来分析结果：

```python
#!/usr/bin/env python3
"""T3单元验证结果分析工具"""

import numpy as np
import matplotlib.pyplot as plt
import re

def parse_stap_output(filename):
    """解析STAPpp输出文件"""
    displacements = {}
    stresses = {}
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # 提取位移数据
    disp_pattern = r'(\d+)\s+([-+]?\d*\.?\d+[eE]?[-+]?\d*)\s+([-+]?\d*\.?\d+[eE]?[-+]?\d*)'
    disp_matches = re.findall(disp_pattern, content)
    
    for match in disp_matches:
        node = int(match[0])
        ux = float(match[1])
        uy = float(match[2])
        displacements[node] = {'ux': ux, 'uy': uy}
    
    # 提取应力数据
    stress_pattern = r'(\d+)\s+([-+]?\d*\.?\d+[eE]?[-+]?\d*)\s+([-+]?\d*\.?\d+[eE]?[-+]?\d*)\s+([-+]?\d*\.?\d+[eE]?[-+]?\d*)'
    stress_matches = re.findall(stress_pattern, content)
    
    for match in stress_matches:
        element = int(match[0])
        sxx = float(match[1])
        syy = float(match[2])
        sxy = float(match[3])
        stresses[element] = {'sxx': sxx, 'syy': syy, 'sxy': sxy}
    
    return displacements, stresses

def convergence_analysis():
    """收敛性分析"""
    mesh_sizes = [2, 4, 8]  # 不同网格密度
    tip_displacements = []
    
    for size in mesh_sizes:
        filename = f"results_t3_cantilever_{size}x{size//2}.out"
        try:
            displacements, _ = parse_stap_output(filename)
            # 提取悬臂梁末端位移
            tip_node = get_tip_node(size)
            tip_disp = displacements[tip_node]['uy']
            tip_displacements.append(abs(tip_disp))
        except:
            print(f"无法读取文件 {filename}")
    
    # 绘制收敛曲线
    plt.figure(figsize=(10, 6))
    plt.loglog(mesh_sizes, tip_displacements, 'bo-', label='T3单元')
    plt.xlabel('网格密度')
    plt.ylabel('末端位移 (m)')
    plt.title('T3单元收敛性分析')
    plt.grid(True)
    plt.legend()
    plt.savefig('t3_convergence.png', dpi=300, bbox_inches='tight')
    plt.show()

def patch_test_analysis():
    """分片试验分析"""
    print("分片试验结果分析:")
    print("="*50)
    
    # 常应变试验
    disp, stress = parse_stap_output("results_t3_patch_constant_strain.out")
    print("常应变试验:")
    for elem, s in stress.items():
        print(f"  单元 {elem}: σxx={s['sxx']:.2f}, σyy={s['syy']:.2f}, τxy={s['sxy']:.2f}")
    
    # 检查应力是否为常值
    stress_values = list(stress.values())
    if len(stress_values) > 1:
        sxx_std = np.std([s['sxx'] for s in stress_values])
        syy_std = np.std([s['syy'] for s in stress_values])
        sxy_std = np.std([s['sxy'] for s in stress_values])
        
        print(f"  应力标准差: σxx={sxx_std:.2e}, σyy={syy_std:.2e}, τxy={sxy_std:.2e}")
        
        if sxx_std < 1e-6 and syy_std < 1e-6 and sxy_std < 1e-6:
            print("  ✅ 分片试验通过：应力为常值")
        else:
            print("  ❌ 分片试验失败：应力不为常值")

if __name__ == "__main__":
    print("T3单元验证结果分析")
    print("="*50)
    
    # 运行分析
    patch_test_analysis()
    convergence_analysis()
```

## 6. 运行验证

```bash
cd ~/WorkSpace/STAPpp/build

# 创建所有测试文件
# (将上述测试案例保存到对应的.dat文件中)

# 运行验证脚本
chmod +x run_t3_validation.sh
./run_t3_validation.sh

# 分析结果
python3 analyze_t3_results.py
```

## 7. 预期验证结果

通过这套完整的验证体系，您应该能够验证：

1. **分片试验**：T3单元能够精确表示常应变状态
2. **收敛性**：随着网格加密，解收敛到理论值
3. **稳定性**：不出现零能模式或数值不稳定
4. **精度**：与理论解或商业软件结果一致

这套验证体系将全面证明您的T3三角形单元实现的正确性和可靠性。