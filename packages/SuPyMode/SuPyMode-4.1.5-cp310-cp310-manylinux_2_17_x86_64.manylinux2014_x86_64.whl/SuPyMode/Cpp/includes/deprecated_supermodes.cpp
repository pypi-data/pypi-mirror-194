#pragma once

#include "definitions.cpp"
#include "utils.cpp"
#include "numpy_interface.cpp"


struct SuperMode
{
  
  size_t mode_number, n_slice, n_x, n_y;
  ScalarType k_initial;

  MatrixType Fields, Coupling, Adiabatic;
  VectorType mesh_gradient;
  std::vector<double> itr_list;
  VectorType Betas, EigenValues, Index;

  SuperMode(){}
  SuperMode(size_t mode_number, 
            ScalarType &k_initial, 
            VectorType &mesh_gradient, 
            std::vector<double> &itr_list,
            size_t &n_x,
            size_t &n_y)
            : k_initial(k_initial), mode_number(mode_number), mesh_gradient(mesh_gradient), itr_list(itr_list), n_x(n_x), n_y(n_y)
            {
                n_slice = itr_list.size();
                Betas = VectorType(n_slice);
                EigenValues = VectorType(n_slice);
                Index = VectorType(n_slice);
                Fields = MatrixType(n_x * n_y, n_slice);
            }

    void copy_other_slice(SuperMode& other_supermode, size_t slice)
    {
        this->Fields.col(slice) = other_supermode.Fields.col(slice);
        this->Betas[slice]      = other_supermode.Betas[slice];
        this->Index[slice]      = other_supermode.Index[slice];
    }

    ScalarType compute_overlap(SuperMode& other_supermode, size_t &slice)
    {
        return this->Fields.col(slice).transpose() * other_supermode.Fields.col(slice);
    }

    ScalarType compute_overlap(SuperMode& other_supermode, size_t &&slice)
    {
        return this->Fields.col(slice).transpose() * other_supermode.Fields.col(slice);
    }

    ScalarType compute_overlap(SuperMode& other_supermode, size_t &&slice0, size_t &&slice1)
    {
        return this->Fields.col(slice0).transpose() * other_supermode.Fields.col(slice1);
    }

    ScalarType compute_overlap(SuperMode& other_supermode, size_t &slice0, size_t &&slice1)
    {
        return this->Fields.col(slice0).transpose() * other_supermode.Fields.col(slice1);
    }


    VectorType get_overlap_with_mode(SuperMode& other_supermode)
    {
        MatrixType overlap = this->Fields.cwiseProduct(other_supermode.Fields);

        return overlap.colwise().sum();
    }


    VectorType get_gradient_overlap_with_mode(SuperMode& other_supermode)
    {
        MatrixType overlap = this->Fields.cwiseProduct(other_supermode.Fields).cwiseProduct(mesh_gradient);

        return overlap.colwise().sum();
    }


    VectorType get_coupling_with_mode(SuperMode& other_supermode)
    {
        VectorType Intergral = get_gradient_overlap_with_mode(other_supermode);

        VectorType beta_0 = this->Betas, 
                   beta_1 = other_supermode.Betas;

        ComplexVectorType delta_beta = (ComplexVectorType) (beta_0 - beta_1),
                          term0 = delta_beta.cwiseInverse().cwiseAbs(),
                          term1 = (ComplexVectorType) beta_0.cwiseProduct(beta_1).cwiseSqrt().cwiseInverse();

        ComplexScalarType term2 = - (ComplexScalarType) 0.5 * J * k_initial * k_initial; 
 
        ComplexVectorType Coupling = term0 * term1 * term2 * Intergral;

        return Coupling.cwiseAbs();
    }


    VectorType get_adiabatic_with_mode(SuperMode& other_supermode)
    {
        ComplexVectorType delta_beta = (ComplexVectorType) (this->Betas - other_supermode.Betas);

        ComplexVectorType coupling = get_coupling_with_mode(other_supermode);

        return delta_beta.cwiseProduct(coupling.cwiseInverse()).cwiseAbs();
    }


    ndarray get_overlap_with_mode_py(SuperMode& supermode){ 
        return eigen_to_ndarray_( get_overlap_with_mode(supermode), {n_slice} ); 
    }

    ndarray get_gradient_overlap_with_mode_py(SuperMode& supermode){ 
        return eigen_to_ndarray_( get_gradient_overlap_with_mode(supermode), {n_slice} ); 
    }

    ndarray get_coupling_with_mode_py(SuperMode& supermode){ 
        return eigen_to_ndarray_( get_coupling_with_mode(supermode), {n_slice} ); 
    }

    ndarray get_adiabatic_with_mode_py(SuperMode& supermode){ 
        return eigen_to_ndarray_( get_adiabatic_with_mode(supermode), {n_slice} ); 
    }



  ndarray get_fields(){ return eigen_to_ndarray_( this->Fields, { n_slice, n_x, n_y} ); }
  ndarray get_index_py(){ return eigen_to_ndarray_( this->Index, { n_slice} ); }
  ndarray get_betas_py(){ return eigen_to_ndarray_( this->Betas, { n_slice} ); }

};



