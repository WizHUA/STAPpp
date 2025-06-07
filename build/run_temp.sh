#!/bin/bash
# filepath: /home/wiz/WorkSpace/STAPpp/build/run_temp_fixed.sh

echo "T3单元最终修正验证测试"
echo "="*60

cd ~/WorkSpace/STAPpp/build

# 创建改进的分片试验数据
cat > ../data/t3_patch_constant_strain_standard.dat << 'EOF'
T3 Patch Test - Constant Strain Standard
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
2 1 1000.0
3 1 1000.0
3 2 1
1 210000.0 0.3 0.01
1 1 2 3 1
2 1 3 4 1
EOF

cat > ../data/t3_patch_pure_shear_standard.dat << 'EOF'
T3 Patch Test - Pure Shear Standard  
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
3 2 500.0
4 1 500.0
3 2 1
1 210000.0 0.3 0.01
1 1 2 3 1
2 1 3 4 1
EOF

# 创建改进的分析脚本
cat > analyze_final.py << 'PYTHON_EOF'
# 将上面的Python分析代码插入此处
PYTHON_EOF

echo "重新编译（开启调试）..."
make clean && make CFLAGS="-D_DEBUG_"

echo "运行修正后的分片试验..."
./stap++ ../data/t3_patch_constant_strain_standard.dat > ../data/results_t3_patch_constant_strain_standard.out 2>&1
./stap++ ../data/t3_patch_pure_shear_standard.dat > ../data/results_t3_patch_pure_shear_standard.out 2>&1

echo "详细分析结果..."
python3 analyze_fi.py

echo "检查关键调试信息..."
echo "常应变试验B矩阵:"
grep -A5 "B matrix:" ../data/results_t3_patch_constant_strain_standard.out | head -20

echo "验证完成!"