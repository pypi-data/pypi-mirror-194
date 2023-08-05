#pragma once

#include "definitions.cpp"
#include "utils.cpp"
#include "numpy_interface.cpp"


struct SuperMode
{
    size_t mode_number;
    double wavenumber, wavelength;
    pybind11::array_t<double> itr_list_py, mesh_gradient_py;
    Eigen::MatrixXd fields;
    Eigen::VectorXd index, betas, eigen_value, itr_list, mesh_gradient;
    size_t nx, ny, n_slice;

    SuperMode(){}
    SuperMode(
        size_t mode_number,
        double wavenumber,
        pybind11::array_t<double> itr_list_py,
        pybind11::array_t<double> mesh_gradient_py,
        pybind11::array_t<double> fields_py,
        pybind11::array_t<double> index_py,
        pybind11::array_t<double> betas_py,
        pybind11::array_t<double> eigen_value_py
        )
        : mode_number(mode_number), wavenumber(wavenumber)
        {
            this->wavelength = 2. * PI / wavenumber;
            this->nx = mesh_gradient_py.request().shape[0];
            this->ny = mesh_gradient_py.request().shape[1];
            this->n_slice = itr_list_py.request().shape[0];

            double *field_ptr = (double*) fields_py.request().ptr;
            Eigen::Map<Eigen::MatrixXd> mapping_fields(field_ptr, nx * ny, n_slice);
            this->fields = mapping_fields;

            double *index_ptr = (double*) index_py.request().ptr;
            Eigen::Map<Eigen::VectorXd> mapping_index(index_ptr, n_slice, 1);
            this->index = mapping_index;

            double *beta_ptr = (double*) betas_py.request().ptr;
            Eigen::Map<Eigen::VectorXd> mapping_betas(beta_ptr, n_slice, 1);
            this->betas = mapping_betas;

            double *eigen_value_ptr = (double*) eigen_value_py.request().ptr;
            Eigen::Map<Eigen::VectorXd> mapping_eigen_value(eigen_value_ptr, n_slice, 1);
            this->eigen_value = mapping_eigen_value;

            double *itr_list_ptr = (double*) itr_list_py.request().ptr;
            Eigen::Map<Eigen::VectorXd> mapping_itr_list(itr_list_ptr, n_slice);
            this->itr_list = mapping_itr_list;

            double *mesh_gradient_ptr = (double*) mesh_gradient_py.request().ptr;
            Eigen::Map<Eigen::VectorXd> mapping_mesh_gradient(mesh_gradient_ptr, nx*ny);
            this->mesh_gradient = mapping_mesh_gradient;
        }

    SuperMode(
        size_t mode_number,
        double wavenumber,
        Eigen::VectorXd &mesh_gradient,
        Eigen::VectorXd &itr_list,
        size_t nx,
        size_t ny)
        : mode_number(mode_number), wavenumber(wavenumber), itr_list(itr_list), mesh_gradient(mesh_gradient)
        {
            this->wavelength = 2. * PI / wavenumber;
            this->nx = nx;
            this->ny = ny;
            this->n_slice = itr_list.size();

            this->fields = MatrixType(nx * ny, n_slice);
            this->eigen_value = VectorType(n_slice);
            this->betas = VectorType(n_slice);
            this->index = VectorType(n_slice);

        }

    pybind11::tuple get_state()
    {
        return pybind11::make_tuple(
            this->mode_number,
            this->wavenumber,
            this->get_itr_list(),
            this->get_mesh_gradient(),
            this->get_fields_py(),
            this->get_index_py(),
            this->get_betas_py(),
            this->get_eigen_value_py()
            );
    }

    double compute_overlap(SuperMode& other_supermode, size_t &slice)
    {
        return this->fields.col(slice).transpose() * other_supermode.fields.col(slice);
    }

    double compute_overlap(SuperMode& other_supermode, size_t &&slice)
    {
        return this->fields.col(slice).transpose() * other_supermode.fields.col(slice);
    }

    double compute_overlap(SuperMode& other_supermode, size_t &&slice_0, size_t &&slice_1)
    {
        return this->fields.col(slice_0).transpose() * other_supermode.fields.col(slice_1);
    }

    double compute_overlap(SuperMode& other_supermode, size_t &slice_0, size_t &&slice_1)
    {
        return this->fields.col(slice_0).transpose() * other_supermode.fields.col(slice_1);
    }

    double compute_overlap(SuperMode& other_supermode, size_t &&slice_0, size_t &slice_1)
    {
        return this->fields.col(slice_0).transpose() * other_supermode.fields.col(slice_1);
    }

    double compute_overlap(SuperMode& other_supermode, size_t &slice_0, size_t &slice_1)
    {
        return this->fields.col(slice_0).transpose() * other_supermode.fields.col(slice_1);
    }

    Eigen::VectorXd get_overlap_with_mode(SuperMode& other_supermode)
    {
        Eigen::MatrixXd overlap = this->fields.cwiseProduct(other_supermode.fields);

        return overlap.colwise().sum().cwiseAbs();
    }

    Eigen::VectorXd get_gradient_overlap_with_mode(SuperMode& other_supermode)
    {
        Eigen::MatrixXd overlap = this->fields.cwiseProduct(other_supermode.fields).array().colwise() * mesh_gradient.array();

        return overlap.colwise().sum().cwiseAbs();
    }

    Eigen::Matrix<std::complex<double>, Eigen::Dynamic, 1> get_normalized_coupling_with_mode(SuperMode& other_supermode)
    {
        Eigen::VectorXd integral = this->get_gradient_overlap_with_mode(other_supermode),
                        beta_0 = this->betas,
                        beta_1 = other_supermode.betas,
                        delta_beta = (beta_0 - beta_1),
                        term0 = delta_beta.cwiseInverse(),
                        term1 = (beta_0.cwiseProduct(beta_1)).cwiseSqrt().cwiseInverse();

        std::complex<double> scalar = - (std::complex<double>) 0.5 * J * wavenumber * wavenumber;

        return scalar * term0.cwiseProduct(term1).cwiseProduct(integral);
    }

    Eigen::VectorXd get_beating_length_with_mode(SuperMode& other_supermode)
    {
        Eigen::VectorXd beta_0 = this->betas,
                        beta_1 = other_supermode.betas;

        return (beta_0 - beta_1) / (2 * PI);
    }

    Eigen::VectorXd get_adiabatic_with_mode(SuperMode& other_supermode)
    {
        Eigen::VectorXd delta_beta = this->betas - other_supermode.betas;

        Eigen::Matrix<std::complex<double>, Eigen::Dynamic, 1> coupling = this->get_normalized_coupling_with_mode(other_supermode);

        return delta_beta.cwiseProduct(coupling.cwiseInverse()).cwiseAbs();
    }

    pybind11::array_t<double> get_overlap_with_mode_py(SuperMode& supermode)
    {
        return templated_eigen_to_ndarray(
            this->get_overlap_with_mode(supermode),
            { n_slice }
        );
    }

    pybind11::array_t<double> get_gradient_overlap_with_mode_py(SuperMode& supermode)
    {
        return templated_eigen_to_ndarray(
            this->get_gradient_overlap_with_mode(supermode),
            { n_slice }
        );
    }

    pybind11::array_t<std::complex<double>> get_normalized_coupling_with_mode_py(SuperMode& supermode)
    {
        return templated_eigen_to_ndarray(
            this->get_normalized_coupling_with_mode(supermode),
            { n_slice }
        );
    }

    pybind11::array_t<double> get_adiabatic_with_mode_py(SuperMode& supermode)
    {
        return templated_eigen_to_ndarray(
            this->get_adiabatic_with_mode(supermode),
            { n_slice }
        );
    }

    pybind11::array_t<double> get_beating_length_with_mode_py(SuperMode& supermode)
    {
        return templated_eigen_to_ndarray(
            this->get_beating_length_with_mode(supermode),
            { n_slice }
        );
    }

    pybind11::array_t<double> get_fields_py()
    {
        return templated_eigen_to_ndarray(
            this->fields,
            { n_slice, nx, ny }
        );
    }

    pybind11::array_t<double> get_index_py()
    {
        return templated_eigen_to_ndarray(
            this->index,
            { n_slice }
        );
    }

    pybind11::array_t<double> get_eigen_value_py()
    {
        return templated_eigen_to_ndarray(
            this->eigen_value,
            { n_slice }
        );
    }

    pybind11::array_t<double> get_betas_py()
    {
        return templated_eigen_to_ndarray(
            this->betas,
            { n_slice }
        );
    }

    pybind11::array_t<double> get_itr_list()
    {
        return templated_eigen_to_ndarray(
            this->itr_list,
            { n_slice }
        );
    }

    pybind11::array_t<double> get_mesh_gradient()
    {
        return templated_eigen_to_ndarray(
            this->mesh_gradient,
            { nx, ny }
        );
    }
};



