/*****************************************************************************/
/*  STAP++ : A C++ FEM code sharing the same input data file with STAP90     */
/*     Computational Dynamics Laboratory                                     */
/*     School of Aerospace Engineering, Tsinghua University                  */
/*                                                                           */
/*     Release 1.11, November 22, 2017                                       */
/*                                                                           */
/*     http://www.comdyn.cn/                                                 */
/*****************************************************************************/

#include "Material.h"

#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

//	Read material data from stream Input
bool CBarMaterial::Read(ifstream& Input)
{
	Input >> nset;	// Number of property set

	Input >> E >> Area;	// Young's modulus and section area

	return true;
}

//	Write material data to Stream
void CBarMaterial::Write(COutputter& output)
{
	output << setw(16) << E << setw(16) << Area << endl;
}

//! Read material data from stream Input
bool CPlaneStressMaterial::Read(ifstream& Input)
{
    Input >> nset >> E >> nu >> t;
    return true;
}

//! Write material data to Stream
void CPlaneStressMaterial::Write(COutputter& output)
{
    output << setw(5) << nset
           << setw(16) << E
           << setw(16) << nu
           << setw(16) << t << endl;
}