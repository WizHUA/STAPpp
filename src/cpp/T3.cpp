/*****************************************************************************/
/*  STAP++ : A C++ FEM code sharing the same input data file with STAP90     */
/*     Computational Dynamics Laboratory                                     */
/*     School of Aerospace Engineering, Tsinghua University                  */
/*                                                                           */
/*     Release 1.11, November 22, 2017                                       */
/*                                                                           */
/*     http://www.comdyn.cn/                                                 */
/*****************************************************************************/

#include "T3.h"
#include "Material.h"
#include "Node.h"

#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

//! Constructor
CT3::CT3()
{
    cerr << "*** T3 CONSTRUCTOR CALLED ***" << endl;
    cerr.flush();
    
    NEN_ = 3;
    NEN_ = 3;    // 每个单元有3个节点
    nodes_ = new CNode*[NEN_];
    
    ND_ = 6;     // 每个节点有2个自由度（x和y方向）
    LocationMatrix_ = new unsigned int[ND_];
    
    ElementMaterial_ = nullptr;
    
    thickness = 1.0;  // 默认厚度
    area = 0.0;
    
    // 初始化形函数系数
    for (int i = 0; i < 3; i++) {
        a[i] = 0.0;
        b[i] = 0.0;
        c[i] = 0.0;
    }
}

//! Destructor
CT3::~CT3()
{
    // 基类析构函数会处理内存释放
}

//! Read element data from stream Input
bool CT3::Read(ifstream& Input, CMaterial* MaterialSets, CNode* NodeList)
{
    cerr << "*** T3::Read() CALLED ***" << endl;
    cerr.flush();

    unsigned int MSet;        // Material property set number
    unsigned int N1, N2, N3;  // Node numbers

    Input >> N1 >> N2 >> N3 >> MSet;
    
    cout << "T3 Element nodes: " << N1 << ", " << N2 << ", " << N3 
         << ", Material: " << MSet << endl;
    
    // 检查节点编号是否有效
    if (N1 <= 0 || N2 <= 0 || N3 <= 0) {
        cerr << "*** Error *** Invalid node number for T3 element." << endl;
        return false;
    }

    // 检查NodeList是否为空
    if (!NodeList) {
        cerr << "*** Error *** NodeList is null in T3::Read." << endl;
        return false;
    }

    nodes_[0] = &NodeList[N1 - 1];
    nodes_[1] = &NodeList[N2 - 1];
    nodes_[2] = &NodeList[N3 - 1];

    // 检查节点指针
    for (unsigned int i = 0; i < 3; i++) {
        if (!nodes_[i]) {
            cerr << "*** Error *** Node pointer " << i << " is null." << endl;
            return false;
        }
    }

    // 调试：输出节点坐标
    cout << "  Node coordinates: ";
    for (unsigned int i = 0; i < 3; i++) {
        cout << "(" << nodes_[i]->XYZ[0] << "," << nodes_[i]->XYZ[1] << ") ";
    }
    cout << endl;

    // 获取材料指针
    if (!MaterialSets) {
        cerr << "*** Error *** MaterialSets is null in T3::Read." << endl;
        return false;
    }
    
    ElementMaterial_ = &MaterialSets[MSet - 1];
    
    // 从材料获取厚度
    CPlaneStressMaterial* material = dynamic_cast<CPlaneStressMaterial*>(ElementMaterial_);
    if (material) {
        thickness = material->t;
        cout << "Material properties: E=" << material->E 
             << ", nu=" << material->nu << ", t=" << material->t << endl;
    }
    else {
        cerr << "*** Error *** Invalid material type for T3 element." << endl;
        return false;
    }

    // 计算形函数系数
    CalculateShapeFuncCoef();

    // 在形函数系数计算后生成位置矩阵
    GenerateLocationMatrix();
    
    cout << "Final Area: " << area << endl;
    cout << "Final LocationMatrix: ";
    for (unsigned int i = 0; i < ND_; i++) {
        cout << LocationMatrix_[i] << " ";
    }
    cout << endl;
    
    return true;
}

//! Write element data to stream
void CT3::Write(COutputter& output)
{
    output << setw(5) << nodes_[0]->NodeNumber
           << setw(9) << nodes_[1]->NodeNumber
           << setw(9) << nodes_[2]->NodeNumber
           << setw(12) << ElementMaterial_->nset << endl;
}

//! Generate location matrix for T3 element (only x and y DOFs)
void CT3::GenerateLocationMatrix()
{
    unsigned int i = 0;
    
    // T3单元只使用x和y方向的自由度（每个节点2个DOF）
    for (unsigned int N = 0; N < NEN_; N++) {
        // 安全检查
        if (nodes_[N] == nullptr) {
            cerr << "*** Error *** Node " << N << " is null in GenerateLocationMatrix." << endl;
            exit(-1);
        }
        
        // 只处理前2个自由度（x和y方向）
        for (unsigned int D = 0; D < 2; D++) {
            if (i >= ND_) {
                cerr << "*** Error *** Index out of bounds in GenerateLocationMatrix: " 
                     << i << " >= " << ND_ << endl;
                exit(-1);
            }
            LocationMatrix_[i++] = nodes_[N]->bcode[D];
        }
    }
    
    // 调试输出：详细的位置矩阵信息
    cout << "T3 Location Matrix: ";
    for (unsigned int i = 0; i < ND_; i++) {
        cout << LocationMatrix_[i] << " ";
    }
    cout << endl;
    
    // 额外调试：输出节点的边界条件
    cout << "Node boundary codes: ";
    for (unsigned int N = 0; N < NEN_; N++) {
        cout << "Node" << (N+1) << ":[" << nodes_[N]->bcode[0] << "," 
             << nodes_[N]->bcode[1] << "] ";
    }
    cout << endl;
}

//! Calculate coefficients of shape functions - 完全修正版
void CT3::CalculateShapeFuncCoef()
{
    double x1 = nodes_[0]->XYZ[0], y1 = nodes_[0]->XYZ[1];
    double x2 = nodes_[1]->XYZ[0], y2 = nodes_[1]->XYZ[1];
    double x3 = nodes_[2]->XYZ[0], y3 = nodes_[2]->XYZ[1];
    
    // 计算2倍面积的行列式
    double det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
    
    cout << "Original coordinates and det:" << endl;
    cout << "  P1(" << x1 << "," << y1 << "), P2(" << x2 << "," << y2 << "), P3(" << x3 << "," << y3 << ")" << endl;
    cout << "  det = " << det << endl;
    
    // 🔧 关键修复：确保逆时针节点顺序
    bool node_swapped = false;
    if (det < 0) {
        cout << "*** Warning *** Clockwise element detected, swapping nodes 2&3..." << endl;
        
        // 物理交换节点指针
        CNode* temp = nodes_[1];
        nodes_[1] = nodes_[2];
        nodes_[2] = temp;
        node_swapped = true;
        
        // 重新获取坐标
        x2 = nodes_[1]->XYZ[0]; y2 = nodes_[1]->XYZ[1];
        x3 = nodes_[2]->XYZ[0]; y3 = nodes_[2]->XYZ[1];
        
        // 重新计算行列式
        det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
        
        cout << "After swap: P1(" << x1 << "," << y1 << "), P2(" << x2 << "," << y2 << "), P3(" << x3 << "," << y3 << ")" << endl;
        cout << "After swap: det = " << det << endl;
    }
    
    area = det / 2.0;
    
    if (area <= 1e-12) {
        cerr << "*** Error *** Invalid area: " << area << endl;
        return;
    }
    
    // 使用标准公式计算形函数系数（现在节点已经是逆时针）
    a[0] = x2 * y3 - x3 * y2;
    b[0] = y2 - y3;
    c[0] = x3 - x2;
    
    a[1] = x3 * y1 - x1 * y3;
    b[1] = y3 - y1;
    c[1] = x1 - x3;
    
    a[2] = x1 * y2 - x2 * y1;
    b[2] = y1 - y2;
    c[2] = x2 - x1;

    cout << "Shape function coefficients:" << endl;
    cout << "  Area: " << area << endl;
    cout << "  a coefficients: [" << a[0] << ", " << a[1] << ", " << a[2] << "]" << endl;
    cout << "  b coefficients: [" << b[0] << ", " << b[1] << ", " << b[2] << "]" << endl;
    cout << "  c coefficients: [" << c[0] << ", " << c[1] << ", " << c[2] << "]" << endl;
    
    // 验证B矩阵主要元素的符号（这些可能为负，是正常的）
    double inv_2A = 1.0 / (2.0 * area);
    cout << "  B[0][0] = b[0]/(2*area) = " << b[0] * inv_2A << endl;
    cout << "  B[0][2] = b[1]/(2*area) = " << b[1] * inv_2A << endl;
    cout << "  B[1][1] = c[0]/(2*area) = " << c[0] * inv_2A << endl;
    cout << "  B[1][3] = c[1]/(2*area) = " << c[1] * inv_2A << endl;
    
    // 🔧 关键：如果交换了节点，重新生成LocationMatrix
    if (node_swapped) {
        cout << "Regenerating LocationMatrix after node swap..." << endl;
        GenerateLocationMatrix();
    }
}

//! Calculate the area of the triangle
double CT3::CalculateArea()
{
    return area;
}

//! Calculate element stiffness matrix - 最终修复版：按列存储兼容STAPpp
void CT3::ElementStiffness(double* Matrix)
{
    // 清零刚度矩阵
    unsigned int size = SizeOfStiffnessMatrix();
    for (unsigned int i = 0; i < size; i++)
        Matrix[i] = 0.0;
    
    // 获取材料属性
    CPlaneStressMaterial* material = dynamic_cast<CPlaneStressMaterial*>(ElementMaterial_);
    if (!material) {
        cerr << "*** Error *** Invalid material for T3 element" << endl;
        return;
    }
    
    double E = material->E;
    double nu = material->nu;
    
    // 确保形函数系数是最新的
    if (area <= 0) {
        cerr << "*** Error *** Invalid element area in ElementStiffness: " << area << endl;
        return;
    }
    
    // 🔧 关键修复：构建平面应力弹性矩阵D
    double factor = E / (1.0 - nu * nu);
    double D[3][3] = {{0.0}};  // 初始化为0
    
    D[0][0] = factor;                       // E/(1-ν²)
    D[0][1] = factor * nu;                  // Eν/(1-ν²)
    D[0][2] = 0.0;
    
    D[1][0] = factor * nu;                  // Eν/(1-ν²)
    D[1][1] = factor;                       // E/(1-ν²)
    D[1][2] = 0.0;
    
    D[2][0] = 0.0;
    D[2][1] = 0.0;
    D[2][2] = factor * (1.0 - nu) / 2.0;   // G = E/[2(1+ν)]
    
    // 🔧 关键修复：构建应变-位移矩阵B
    double B[3][6] = {{0.0}};  // 初始化为0
    double inv_2A = 1.0 / (2.0 * area);
    
    for (unsigned int i = 0; i < 3; i++) {
        // 第1行：εxx = ∂u/∂x
        B[0][2*i]   = b[i] * inv_2A;     
        B[0][2*i+1] = 0.0;
        
        // 第2行：εyy = ∂v/∂y
        B[1][2*i]   = 0.0;
        B[1][2*i+1] = c[i] * inv_2A;     
        
        // 第3行：γxy = ∂u/∂y + ∂v/∂x
        B[2][2*i]   = c[i] * inv_2A;     
        B[2][2*i+1] = b[i] * inv_2A;     
    }
    
    // 🔧 关键修复：计算 DB = D * B
    double DB[3][6] = {{0.0}};  // 初始化为0
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 6; j++) {
            for (int k = 0; k < 3; k++) {
                DB[i][j] += D[i][k] * B[k][j];
            }
        }
    }
    
    // 🚀 最终修复：按列存储兼容STAPpp Assembly
    // STAPpp期望每列从上到下存储：K[0][j], K[1][j], ..., K[j][j]
    unsigned int index = 0;
    double volume = thickness * area;
    
    for (unsigned int j = 0; j < 6; j++) {          // 外层循环：列
        for (unsigned int i = j; i >= 0 && i <= j; i--) {  // 内层循环：从对角线向上
            double sum = 0.0;
            
            // 计算 K[i][j] = B^T[i] * DB[j]
            for (int k = 0; k < 3; k++) {
                sum += B[k][i] * DB[k][j];
            }
            
            Matrix[index] = sum * volume;
            index++;
            
            if (i == 0) break;  // 防止无符号数下溢
        }
    }
    
    // 验证存储格式
    cout << "\n=== STAPpp兼容存储格式验证 ===" << endl;
    index = 0;
    for (unsigned int j = 0; j < 6; j++) {
        cout << "第" << j << "列 (对角元素先): ";
        for (unsigned int i = j; i >= 0 && i <= j; i--) {
            cout << "K[" << i << "][" << j << "]=" << setprecision(3) << Matrix[index] << " ";
            index++;
            if (i == 0) break;
        }
        cout << endl;
    }
    
    // 验证Assembly兼容性
    cout << "\n=== Assembly兼容性验证（修复后）===" << endl;
    for (unsigned int j = 0; j < 3; j++) {
        unsigned int DiagjElement = (j+1)*j/2;
        cout << "第" << j << "列对角元素位置: " << DiagjElement << endl;
        
        for (unsigned int i = 0; i <= j; i++) {
            unsigned int assemblyIndex = DiagjElement + j - i;
            if (assemblyIndex < size) {
                cout << "  Assembly: K[" << i << "][" << j << "] 从 Matrix[" 
                     << assemblyIndex << "] = " << Matrix[assemblyIndex] << endl;
            }
        }
    }
}

//! Calculate element stress - 与刚度矩阵保持一致
void CT3::ElementStress(double* stress, double* Displacement)
{
    // 初始化应力数组
    for (unsigned int i = 0; i < 3; i++)
        stress[i] = 0.0;
    
    if (!Displacement) {
        cerr << "*** Error *** Null displacement array in ElementStress" << endl;
        return;
    }
    
    // 获取材料属性
    CPlaneStressMaterial* material = dynamic_cast<CPlaneStressMaterial*>(ElementMaterial_);
    if (!material) {
        cerr << "*** Error *** Invalid material type in ElementStress" << endl;
        return;
    }
    
    double E = material->E;
    double nu = material->nu;
    
    if (area <= 0) {
        cerr << "*** Error *** Invalid area in stress calculation: " << area << endl;
        return;
    }
    
    // 构建弹性矩阵D（与刚度矩阵完全一致）
    double factor = E / (1.0 - nu * nu);
    double D[3][3];
    
    D[0][0] = factor;
    D[0][1] = factor * nu;
    D[0][2] = 0.0;
    
    D[1][0] = factor * nu;
    D[1][1] = factor;
    D[1][2] = 0.0;
    
    D[2][0] = 0.0;
    D[2][1] = 0.0;
    D[2][2] = factor * (1.0 - nu) / 2.0;
    
    // 构建应变矩阵B（与刚度矩阵完全一致）
    double B[3][6];
    double inv_2A = 1.0 / (2.0 * area);
    
    for (unsigned int i = 0; i < 3; i++) {
        B[0][2*i]   = b[i] * inv_2A;
        B[0][2*i+1] = 0.0;
        
        B[1][2*i]   = 0.0;
        B[1][2*i+1] = c[i] * inv_2A;
        
        B[2][2*i]   = c[i] * inv_2A;
        B[2][2*i+1] = b[i] * inv_2A;
    }
    
    // 提取单元节点位移向量
    double d[6] = {0.0};
    
    for (unsigned int i = 0; i < 6; i++) {
        if (LocationMatrix_[i] > 0) {
            unsigned int disp_index = LocationMatrix_[i] - 1;
            d[i] = Displacement[disp_index];
        }
        // 约束自由度位移为0（已初始化）
    }
    
    // 计算应变：ε = B * d
    double strain[3] = {0.0};
    for (unsigned int i = 0; i < 3; i++) {
        for (unsigned int j = 0; j < 6; j++) {
            strain[i] += B[i][j] * d[j];
        }
    }
    
    // 计算应力：σ = D * ε
    for (unsigned int i = 0; i < 3; i++) {
        for (unsigned int j = 0; j < 3; j++) {
            stress[i] += D[i][j] * strain[j];
        }
    }

    cout << "T3 Element stress calculation:" << endl;
    cout << "  Displacements: [";
    for (int k = 0; k < 6; k++) cout << setw(10) << setprecision(6) << d[k] << " ";
    cout << "]" << endl;
    cout << "  Strains: [" << setw(12) << strain[0] << ", " << setw(12) << strain[1] 
         << ", " << setw(12) << strain[2] << "]" << endl;
    cout << "  Stresses: [" << setw(12) << stress[0] << ", " << setw(12) << stress[1] 
         << ", " << setw(12) << stress[2] << "]" << endl;
}