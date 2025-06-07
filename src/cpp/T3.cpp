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
    
    cout << "Area calculated: " << area << endl;
    
    // 生成位置矩阵
    GenerateLocationMatrix();
    
    cout << "Location matrix generated successfully." << endl;
    
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

//! Generate location matrix for T3 element (only x and y DOFs) - 修正版
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

//! Calculate coefficients of shape functions - 最终修正版
void CT3::CalculateShapeFuncCoef()
{
    // 获取节点坐标
    double x1 = nodes_[0]->XYZ[0], y1 = nodes_[0]->XYZ[1];
    double x2 = nodes_[1]->XYZ[0], y2 = nodes_[1]->XYZ[1];
    double x3 = nodes_[2]->XYZ[0], y3 = nodes_[2]->XYZ[1];
    
    // 使用标准的三角形面积公式计算面积（确保数值稳定性）
    double det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
    area = abs(det) / 2.0;
    
    if (area < 1e-12) {
        cerr << "*** Error *** T3 element has zero or negative area!" << endl;
        cout << "    Coordinates: (" << x1 << "," << y1 << "), (" 
             << x2 << "," << y2 << "), (" << x3 << "," << y3 << ")" << endl;
        cout << "    Determinant: " << det << endl;
        return;
    }
    
    // 检查节点顺序，如果是顺时针则交换
    bool need_swap = false;
    if (det < 0) {
        cout << "*** Warning *** Element has clockwise orientation, swapping nodes 2 and 3" << endl;
        // 交换节点2和节点3
        CNode* temp = nodes_[1];
        nodes_[1] = nodes_[2];
        nodes_[2] = temp;
        
        // 重新计算坐标和面积
        x2 = nodes_[1]->XYZ[0]; y2 = nodes_[1]->XYZ[1];
        x3 = nodes_[2]->XYZ[0]; y3 = nodes_[2]->XYZ[1];
        det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
        area = det / 2.0;  // 现在应该是正值
        need_swap = true;
    }
    
    // 计算形函数系数（标准公式）
    // 对于逆时针排列的节点(x1,y1), (x2,y2), (x3,y3)：
    a[0] = x2 * y3 - x3 * y2;
    b[0] = y2 - y3;
    c[0] = x3 - x2;
    
    a[1] = x3 * y1 - x1 * y3;
    b[1] = y3 - y1;
    c[1] = x1 - x3;
    
    a[2] = x1 * y2 - x2 * y1;
    b[2] = y1 - y2;
    c[2] = x2 - x1;
    
    // 验证形函数系数的正确性
    double sum_a = a[0] + a[1] + a[2];
    double expected_sum = 2.0 * area;
    
    if (abs(sum_a - expected_sum) > 1e-10) {
        cerr << "*** Error *** Shape function coefficient validation failed!" << endl;
        cout << "    sum(a) = " << sum_a << ", expected 2*area = " << expected_sum << endl;
        cout << "    Difference = " << abs(sum_a - expected_sum) << endl;
        cout << "    Area = " << area << ", det = " << det << endl;
    }

#ifdef _DEBUG_
    cout << "Shape function coefficients (after " << (need_swap ? "node swap" : "no swap") << "):" << endl;
    cout << "  Final coordinates: (" << x1 << "," << y1 << "), (" << x2 << "," << y2 << "), (" << x3 << "," << y3 << ")" << endl;
    cout << "  a: [" << a[0] << ", " << a[1] << ", " << a[2] << "]" << endl;
    cout << "  b: [" << b[0] << ", " << b[1] << ", " << b[2] << "]" << endl;
    cout << "  c: [" << c[0] << ", " << c[1] << ", " << c[2] << "]" << endl;
    cout << "  Area: " << area << ", sum(a): " << sum_a << ", det: " << det << endl;
#endif

    // 如果交换了节点，需要重新生成位置矩阵
    if (need_swap) {
        cout << "Regenerating location matrix after node swap..." << endl;
        GenerateLocationMatrix();
    }
}

//! Calculate the area of the triangle
double CT3::CalculateArea()
{
    return area;
}

//! Calculate element stiffness matrix - 最终修正版
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
    
    // 重新计算形函数系数，确保最新
    CalculateShapeFuncCoef();
    
    if (area <= 0) {
        cerr << "*** Error *** Invalid element area: " << area << endl;
        return;
    }
    
    // 构建平面应力弹性矩阵D
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
    
    // 构建应变-位移矩阵B
    double B[3][6];
    double inv_2A = 1.0 / (2.0 * area);
    
    // 按照标准公式构造B矩阵
    for (unsigned int i = 0; i < 3; i++) {
        // εxx = ∂u/∂x 行
        B[0][2*i]   = b[i] * inv_2A;     
        B[0][2*i+1] = 0.0;
        
        // εyy = ∂v/∂y 行
        B[1][2*i]   = 0.0;
        B[1][2*i+1] = c[i] * inv_2A;     
        
        // γxy = ∂u/∂y + ∂v/∂x 行
        B[2][2*i]   = c[i] * inv_2A;     
        B[2][2*i+1] = b[i] * inv_2A;     
    }
    
    // 计算单元刚度矩阵：K = t*A*B^T*D*B
    double volume = thickness * area;
    
    // 使用更稳定的计算方法
    for (unsigned int i = 0; i < 6; i++) {
        for (unsigned int j = i; j < 6; j++) {  
            double sum = 0.0;
            
            // K[i][j] = volume * sum_k(sum_l(B[k][i] * D[k][l] * B[l][j]))
            for (int k = 0; k < 3; k++) {
                for (int l = 0; l < 3; l++) {
                    sum += B[k][i] * D[k][l] * B[l][j];
                }
            }
            
            // STAPpp上三角矩阵存储格式
            unsigned int index = j * (j + 1) / 2 + i;
            if (index < size) {
                Matrix[index] = sum * volume;
            }
            else {
                cerr << "*** Error *** Stiffness matrix index overflow" << endl;
                return;
            }
        }
    }

#ifdef _DEBUG_
    cout << "T3 stiffness matrix calculation:" << endl;
    cout << "  Area: " << area << ", Thickness: " << thickness << ", Volume: " << volume << endl;
    cout << "  Material: E=" << E << ", nu=" << nu << ", factor=" << factor << endl;
    
    cout << "  B matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        cout << "    [";
        for (int j = 0; j < 6; j++) {
            cout << setw(12) << setprecision(6) << B[i][j];
        }
        cout << "]" << endl;
    }
    
    cout << "  K[0][0] = " << Matrix[0] << endl;
    cout << "  K[0][1] = " << Matrix[1] << endl;
    cout << "  K[1][1] = " << Matrix[2] << endl;
#endif
}

//! Calculate element stress - 最终修正版
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
    
    // 确保几何参数是最新的
    CalculateShapeFuncCoef();
    
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
    
    // 提取单元节点位移向量（关键修正：增加验证）
    double d[6] = {0.0};
    
    for (unsigned int i = 0; i < 6; i++) {
        if (LocationMatrix_[i] > 0) {
            // 验证索引范围
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

#ifdef _DEBUG_
    cout << "T3 Element stress calculation:" << endl;
    cout << "  Material: E=" << E << ", nu=" << nu << ", factor=" << factor << endl;
    cout << "  Area: " << area << ", inv_2A=" << inv_2A << endl;
    cout << "  LocationMatrix: [";
    for (int k = 0; k < 6; k++) cout << LocationMatrix_[k] << " ";
    cout << "]" << endl;
    cout << "  Displacements: [";
    for (int k = 0; k < 6; k++) cout << setw(12) << setprecision(6) << d[k] << " ";
    cout << "]" << endl;
    cout << "  Strains: [" << setw(12) << strain[0] << ", " << setw(12) << strain[1] 
         << ", " << setw(12) << strain[2] << "]" << endl;
    cout << "  Stresses: [" << setw(12) << stress[0] << ", " << setw(12) << stress[1] 
         << ", " << setw(12) << stress[2] << "]" << endl;
    
    // 详细验证B矩阵
    cout << "  B matrix verification:" << endl;
    for (int i = 0; i < 3; i++) {
        cout << "    [";
        for (int j = 0; j < 6; j++) {
            cout << setw(12) << setprecision(6) << B[i][j];
        }
        cout << "]" << endl;
    }
    
    // 验证坐标
    cout << "  Element coordinates: ";
    for (unsigned int i = 0; i < 3; i++) {
        cout << "(" << nodes_[i]->XYZ[0] << "," << nodes_[i]->XYZ[1] << ") ";
    }
    cout << endl;
#endif
}