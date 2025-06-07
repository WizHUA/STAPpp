/*****************************************************************************/
/*  STAP++ : A C++ FEM code sharing the same input data file with STAP90     */
/*     Computational Dynamics Laboratory                                     */
/*     School of Aerospace Engineering, Tsinghua University                  */
/*                                                                           */
/*     Release 1.11, November 22, 2017                                       */
/*                                                                           */
/*     http://www.comdyn.cn/                                                 */
/*****************************************************************************/

#pragma once

#include "Element.h"

using namespace std;

//! 3-node Triangle (T3) element class for plane stress problems
class CT3 : public CElement
{
private:
    // Shape function coefficients
    double a[3], b[3], c[3];
    
    // Element area
    double area;
    
    // Element thickness
    double thickness;
    
    // Calculate shape function coefficients
    void CalculateShapeFuncCoef();
    
    // Calculate the area of the triangle
    double CalculateArea();

public:
    //! Constructor
    CT3();

    //! Destructor
    ~CT3();

    //! Read element data from stream Input
    virtual bool Read(ifstream& Input, CMaterial* MaterialSets, CNode* NodeList);

    //! Write element data to stream
    virtual void Write(COutputter& output);

    //! Generate location matrix for T3 element (only x and y DOFs)
    virtual void GenerateLocationMatrix() override;

    //! Calculate element stiffness matrix
    virtual void ElementStiffness(double* Matrix);

    //! Calculate element stress
    virtual void ElementStress(double* stress, double* Displacement);
    
    //! Return area of the element
    inline double GetArea() { return area; }
    
    //! Return thickness of the element
    inline double GetThickness() { return thickness; }
};