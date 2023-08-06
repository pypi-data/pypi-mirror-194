import h5py
import cupy as cp
from pygpe.shared.grid import Grid
from pygpe.shared import data_manager_paths as dmp
from pygpe.spinhalf.wavefunction import SpinHalfWavefunction


class DataManager:
    """This object handles all the data of the simulation, including the
    wavefunction, grid, and parameter data.

    :param filename: The name of the data file.
    :type filename: str
    :param data_path: The relative path to the folder containing the data file.
    :type data_path: str

    :ivar filename: The name of the data file.
    :ivar data_path: The relative path to the folder containing the data file.
    """

    def __init__(self, filename: str, data_path: str):
        self.filename = filename
        self.data_path = data_path
        self._time_index = 0

        # Create file
        h5py.File(f"{self.data_path}/{self.filename}", "w")

    def save_initial_parameters(
        self, grid: Grid, wfn: SpinHalfWavefunction, parameters: dict
    ) -> None:
        """Saves the initial grid, wavefunction and parameters to a HDF5 file.

        :param grid: The grid object of the system.
        :type grid: :class:`Grid`
        :param wfn: The wavefunction of the system.
        :type wfn: :class:`Wavefunction`
        :param parameters: The parameter dictionary.
        :type parameters: dict
        """
        if grid.ndim > 3 or grid.ndim < 1:
            raise ValueError(
                f"Grid with dimension of {grid.ndim} is unsupported, "
                "please use a 1D, 2D, or 3D grid."
            )
        self._save_initial_grid_params(grid)
        self._save_initial_wfn(wfn)
        self._save_params(parameters)

    def _save_initial_grid_params(self, grid: Grid) -> None:
        """Creates new datasets in file for grid-related parameters and saves
        initial values.
        """
        with h5py.File(f"{self.data_path}/{self.filename}", "r+") as file:
            if grid.ndim == 1:
                file.create_dataset(dmp.GRID_NX, data=grid.num_points_x)
                file.create_dataset(dmp.GRID_DX, data=grid.grid_spacing_x)
            elif grid.ndim == 2:
                file.create_dataset(dmp.GRID_NX, data=grid.num_points_x)
                file.create_dataset(dmp.GRID_NY, data=grid.num_points_y)
                file.create_dataset(dmp.GRID_DX, data=grid.grid_spacing_x)
                file.create_dataset(dmp.GRID_DY, data=grid.grid_spacing_y)
            elif grid.ndim == 3:
                file.create_dataset(dmp.GRID_NX, data=grid.num_points_x)
                file.create_dataset(dmp.GRID_NY, data=grid.num_points_y)
                file.create_dataset(dmp.GRID_NZ, data=grid.num_points_z)
                file.create_dataset(dmp.GRID_DX, data=grid.grid_spacing_x)
                file.create_dataset(dmp.GRID_DY, data=grid.grid_spacing_y)
                file.create_dataset(dmp.GRID_DZ, data=grid.grid_spacing_z)

    def _save_initial_wfn(self, wfn: SpinHalfWavefunction) -> None:
        """Creates new datasets in file for the wavefunction and saves
        initial values.
        """
        with h5py.File(f"{self.data_path}/{self.filename}", "r+") as file:
            if wfn.grid.ndim == 1:
                file.create_dataset(
                    dmp.SPINHALF_WAVEFUNCTION_PLUS,
                    (wfn.grid.shape, 1),
                    maxshape=(wfn.grid.shape, None),
                    dtype="complex128",
                )
                file.create_dataset(
                    dmp.SPINHALF_WAVEFUNCTION_MINUS,
                    (wfn.grid.shape, 1),
                    maxshape=(wfn.grid.shape, None),
                    dtype="complex128",
                )
            else:
                file.create_dataset(
                    dmp.SPINHALF_WAVEFUNCTION_PLUS,
                    (*wfn.grid.shape, 1),
                    maxshape=(*wfn.grid.shape, None),
                    dtype="complex128",
                )
                file.create_dataset(
                    dmp.SPINHALF_WAVEFUNCTION_MINUS,
                    (*wfn.grid.shape, 1),
                    maxshape=(*wfn.grid.shape, None),
                    dtype="complex128",
                )

    def _save_params(self, parameters: dict) -> None:
        """Creates new datasets in file for condensate & time parameters
        and saves initial values.
        """
        with h5py.File(f"{self.data_path}/{self.filename}", "r+") as file:
            for key in parameters:
                file.create_dataset(f"parameters/{key}", data=parameters[key])

    def save_wavefunction(self, wfn: SpinHalfWavefunction) -> None:
        """Saves the current wavefunction data to the dataset.

        :param wfn: The wavefunction of the system.
        :type wfn: :class:`Wavefunction`
        """
        wfn.ifft()  # Update real-space wavefunction before saving
        with h5py.File(f"{self.data_path}/{self.filename}", "r+") as data:
            if wfn.grid.ndim == 1:
                new_psi_plus = data[dmp.SPINHALF_WAVEFUNCTION_PLUS]
                new_psi_plus.resize(
                    (wfn.grid.num_points_x, self._time_index + 1)
                )
                new_psi_plus[:, self._time_index] = cp.asnumpy(
                    wfn.plus_component
                )

                new_psi_minus = data[dmp.SPINHALF_WAVEFUNCTION_MINUS]
                new_psi_minus.resize(
                    (wfn.grid.num_points_x, self._time_index + 1)
                )
                new_psi_minus[:, self._time_index] = cp.asnumpy(
                    wfn.minus_component
                )
            else:
                new_psi_plus = data[dmp.SPINHALF_WAVEFUNCTION_PLUS]
                new_psi_plus.resize((*wfn.grid.shape, self._time_index + 1))
                new_psi_plus[..., self._time_index] = cp.asnumpy(
                    wfn.plus_component
                )

                new_psi_minus = data[dmp.SPINHALF_WAVEFUNCTION_MINUS]
                new_psi_minus.resize((*wfn.grid.shape, self._time_index + 1))
                new_psi_minus[..., self._time_index] = cp.asnumpy(
                    wfn.minus_component
                )

        self._time_index += 1
