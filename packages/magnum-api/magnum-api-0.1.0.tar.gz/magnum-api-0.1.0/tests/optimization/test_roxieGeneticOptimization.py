from unittest import TestCase

import pandas as pd
import numpy as np

from magnumapi.geometry.GeometryChange import GeometryChange
from magnumapi.geometry.GeometryFactory import GeometryFactory
from magnumapi.cadata.CableDatabase import CableDatabase
from magnumapi.optimization.GeneticOptimization import GeneticOptimization, RoxieGeneticOptimization
from tests.resource_files import create_resources_file_path

json_file_path = create_resources_file_path('resources/optimization/config.json')
csv_file_path = create_resources_file_path('resources/optimization/optim_input_enlarged.csv')
optimization_cfg = GeneticOptimization.initialize_config(json_file_path)

json_path = create_resources_file_path('resources/geometry/roxie/16T/16T_rel.json')
cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
cadata = CableDatabase.read_cadata(cadata_path)
geometry = GeometryFactory.init_with_json(json_path, cadata)


class TestRoxieGeneticOptimization(TestCase):

    def setUp(self) -> None:
        self.gen_opt = RoxieGeneticOptimization(config=optimization_cfg,
                                                design_variables_df=pd.read_csv(csv_file_path),
                                                geometry=geometry,
                                                model_input_path='',
                                                is_script_executed=True,
                                                output_subdirectory_dir='')

    def test_initialize_population(self):
        # arrange
        np.random.seed(0)

        # act
        pop = self.gen_opt.initialize_population()

        # assert
        pop_ref = [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0,
                   1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0,
                   0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0,
                   0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]

        self.assertListEqual(pop_ref, pop[0])

    def test_decode_chromosome(self):
        # arrange
        np.random.seed(0)

        # act
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])

        # assert
        chromosome_ref = {'2:phi_r': 5.953125, '3:phi_r': 9.78125, '4:phi_r': 4.75, '6:phi_r': 5.40625,
                          '7:phi_r': 6.28125, '9:phi_r': 7.703125, '10:phi_r': 5.734375, '12:phi_r': 6.390625,
                          '2:alpha_r': 3.59375, '3:alpha_r': 6.40625, '4:alpha_r': 6.5625, '6:alpha_r': 0.46875,
                          '7:alpha_r': 0.9375, '9:alpha_r': 5.78125, '10:alpha_r': 9.6875, '12:alpha_r': 7.8125,
                          '1:nco': 3, '2:nco': 2, '3:nco': 1, '4:nco': 0, '5:nco': 6, '6:nco': 9, '7:nco': 0,
                          '8:nco': 14, '9:nco': 9, '10:nco': 3, '11:nco': 30, '12:nco': 12}

        self.assertDictEqual(chromosome_ref, chromosome)

    def test_decode_chromosome_with_global_parameter(self):
        # arrange
        np.random.seed(0)
        csv_global_file_path = create_resources_file_path('resources/optimization/optim_input_enlarged_with_global.csv')
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)

        # act
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])

        # assert
        chromosome_ref = {'2:phi_r': 5.953125, '3:phi_r': 9.78125, '4:phi_r': 4.75, '6:phi_r': 5.40625,
                          '7:phi_r': 6.28125, '9:phi_r': 7.703125, '10:phi_r': 5.734375, '12:phi_r': 6.390625,
                          '2:alpha_r': 3.59375, '3:alpha_r': 6.40625, '4:alpha_r': 6.5625, '6:alpha_r': 0.46875,
                          '7:alpha_r': 0.9375, '9:alpha_r': 5.78125, '10:alpha_r': 9.6875, '12:alpha_r': 7.8125,
                          '1:nco': 3, '2:nco': 2, '3:nco': 1, '4:nco': 0, '5:nco': 6, '6:nco': 9, '7:nco': 0,
                          '8:nco': 14, '9:nco': 9, '10:nco': 3, '11:nco': 30, '12:nco': 12, 'R_EE': 1.2109375}

        self.assertDictEqual(chromosome_ref, chromosome)

    def test_decode_chromosome_with_global_parameter_multi_index(self):
        # arrange
        np.random.seed(0)
        path_str = 'resources/optimization/optim_input_enlarged_with_global_multi_index.csv'
        csv_global_file_path = create_resources_file_path(path_str)
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)

        # act
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])

        # assert
        chromosome_ref = {'2:phi_r': 5.953125, '3:phi_r': 9.78125, '4:phi_r': 4.75, '6:phi_r': 5.40625,
                          '7:phi_r': 6.28125, '9:phi_r': 7.703125, '10:phi_r': 5.734375, '12:phi_r': 6.390625,
                          '2:alpha_r': 3.59375, '3:alpha_r': 6.40625, '4:alpha_r': 6.5625, '6:alpha_r': 0.46875,
                          '7:alpha_r': 0.9375, '9:alpha_r': 5.78125, '10:alpha_r': 9.6875, '12:alpha_r': 7.8125,
                          '1:nco': 3, '2:nco': 2, '3:nco': 1, '4:nco': 0, '5:nco': 6, '6:nco': 9, '7:nco': 0,
                          '8:nco': 14, '9:nco': 9, '10:nco': 3, '11:nco': 30, '12:nco': 12, 'R_EE': 1.2109375,
                          '1:current': 12257.8125, '2:current': 12257.8125, '3:current': 12257.8125,
                          '4:current': 12257.8125, '5:current': 12257.8125, '6:current': 12257.8125,
                          '7:current': 12257.8125, '8:current': 12257.8125, '9:current': 12257.8125,
                          '10:current': 12257.8125, '11:current': 12257.8125, '12:current': 12257.8125}

        self.assertDictEqual(chromosome_ref, chromosome)

    def test_update_parameters(self):
        # arrange
        np.random.seed(0)

        # act
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])
        block_layer_defs = self.gen_opt.update_model_parameters(chromosome)

        # assert
        block_defs_ref = {'block_defs': [
            {'no': 1, 'radius': 25.0, 'alpha_r': 0, 'phi_r': 0.57294, 'nco': 3, 'type': 1, 'current': 13500,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 2, 'radius': 25.0, 'alpha_r': 3.59375, 'phi_r': 5.953125, 'nco': 2, 'type': 1, 'current': 13500,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 3, 'radius': 25.0, 'alpha_r': 6.40625, 'phi_r': 9.78125, 'nco': 1, 'type': 1, 'current': 13500,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 5, 'radius': 39.0, 'alpha_r': 0.0, 'phi_r': 0.36728, 'nco': 6, 'type': 1, 'current': 13500,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 6, 'radius': 39.0, 'alpha_r': 0.46875, 'phi_r': 5.40625, 'nco': 9, 'type': 1, 'current': 13500,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 8, 'radius': 53.0, 'alpha_r': 0, 'phi_r': 0.27026, 'nco': 14, 'type': 1, 'current': 13500,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 9, 'radius': 53.0, 'alpha_r': 5.78125, 'phi_r': 7.703125, 'nco': 9, 'type': 1, 'current': 13500,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 10, 'radius': 53.0, 'alpha_r': 9.6875, 'phi_r': 5.734375, 'nco': 3, 'type': 1, 'current': 13500,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 11, 'radius': 67.45, 'alpha_r': 0, 'phi_r': 0.21236, 'nco': 30, 'type': 1, 'current': 13500,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 12, 'radius': 67.45, 'alpha_r': 7.8125, 'phi_r': 6.390625, 'nco': 12, 'type': 1, 'current': 13500,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0}],
            'layer_defs': [{'no': 1, 'symm': 1, 'typexy': 1, 'blocks': [1, 2, 3, 4]},
                           {'no': 2, 'symm': 1, 'typexy': 1, 'blocks': [5, 6, 7]},
                           {'no': 3, 'symm': 1, 'typexy': 1, 'blocks': [8, 9, 10]},
                           {'no': 3, 'symm': 1, 'typexy': 1, 'blocks': [11, 12]}]}

        assert block_defs_ref['block_defs'] == block_layer_defs['block_defs']

    def test_update_parameters_multi_index(self):
        # arrange
        np.random.seed(0)
        path_str = 'resources/optimization/optim_input_enlarged_with_global_multi_index.csv'
        csv_global_file_path = create_resources_file_path(path_str)
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)

        # act
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])
        block_layer_defs = self.gen_opt.update_model_parameters(chromosome)

        # assert
        block_defs_ref = [
            {'no': 1, 'radius': 25.0, 'alpha_r': 0, 'phi_r': 0.57294, 'nco': 3, 'type': 1, 'current': 12257.8125,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 2, 'radius': 25.0, 'alpha_r': 3.59375, 'phi_r': 5.953125, 'nco': 2, 'type': 1, 'current': 12257.8125,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 3, 'radius': 25.0, 'alpha_r': 6.40625, 'phi_r': 9.78125, 'nco': 1, 'type': 1, 'current': 12257.8125,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 5, 'radius': 39.0, 'alpha_r': 0.0, 'phi_r': 0.36728, 'nco': 6, 'type': 1, 'current': 12257.8125,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 6, 'radius': 39.0, 'alpha_r': 0.46875, 'phi_r': 5.40625, 'nco': 9, 'type': 1, 'current': 12257.8125,
             'condname': '16TIL9', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 8, 'radius': 53.0, 'alpha_r': 0, 'phi_r': 0.27026, 'nco': 14, 'type': 1, 'current': 12257.8125,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 9, 'radius': 53.0, 'alpha_r': 5.78125, 'phi_r': 7.703125, 'nco': 9, 'type': 1, 'current': 12257.8125,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 10, 'radius': 53.0, 'alpha_r': 9.6875, 'phi_r': 5.734375, 'nco': 3, 'type': 1, 'current': 12257.8125,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 11, 'radius': 67.45, 'alpha_r': 0, 'phi_r': 0.21236, 'nco': 30, 'type': 1, 'current': 12257.8125,
             'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0},
            {'no': 12, 'radius': 67.45, 'alpha_r': 7.8125, 'phi_r': 6.390625, 'nco': 12, 'type': 1,
             'current': 12257.8125, 'condname': '16TOL8', 'n1': 2, 'n2': 20, 'imag': 0, 'turn': 0}]

        self.assertListEqual(block_defs_ref, block_layer_defs['block_defs'])

    def test_correct_missing_blocks_in_block_and_layer_definitions(self):
        # arrange
        chromosome = {'1:nco_r': 2,
                      '2:nco_r': -3}
        json_path = create_resources_file_path('resources/geometry/roxie/16T/16T_rel.json')
        cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
        cadata = CableDatabase.read_cadata(cadata_path)
        geometry = GeometryFactory.init_with_json(json_path, cadata)

        # act
        # # update number of turns per block_index
        geometry = GeometryChange.update_nco_r(geometry, chromosome)

        assert len(geometry.blocks) == 11
        assert geometry.layer_defs[0].blocks == [1, 3, 4]
        assert geometry.layer_defs[1].blocks == [5, 6, 7]
        assert geometry.layer_defs[2].blocks == [8, 9, 10]
        assert geometry.layer_defs[3].blocks == [11, 12]

    def test_update_targeted_optimization_input_geometry(self):
        np.random.seed(1)

        # act
        path_str = 'resources/optimization/optim_input_enlarged_targeted_optimization.csv'
        csv_global_file_path = create_resources_file_path(path_str)
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])

        # read an input file with geometry definition
        cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
        cadata = CableDatabase.read_cadata(cadata_path)
        json_ref_path = create_resources_file_path('resources/geometry/roxie/16T/16T_rel.json')

        # initialize relative geometry
        geometry_rel = GeometryFactory.init_with_json(json_ref_path, cadata)

        # update phi_r
        geometry_rel = GeometryChange.update_phi_r(geometry_rel, chromosome)

        # update nco_r
        geometry_rel = GeometryChange.update_nco_r(geometry_rel, chromosome)

        # extract absolute geometry
        geometry_abs = geometry_rel.to_abs_geometry()

        # correct block radiality
        geometry_abs = GeometryChange.calculate_radial_alpha(geometry_abs)

        # extract relative geometry
        geometry_rel = geometry_abs.to_rel_geometry()

        # update alpha_rad_r with
        geometry_rel = GeometryChange.update_alpha_radial(geometry_rel, chromosome)

        # assert that the number of turns per layer is the same
        assert 13 == sum([block.block_def.nco for block in geometry_rel.blocks[:4]])
        assert 19 == sum([block.block_def.nco for block in geometry_rel.blocks[4:7]])
        assert 29 == sum([block.block_def.nco for block in geometry_rel.blocks[7:10]])
        assert 39 == sum([block.block_def.nco for block in geometry_rel.blocks[10:]])

    def test_update_model_parameters_targeted(self):
        np.random.seed(1)

        # act
        path_str = 'resources/optimization/optim_input_enlarged_targeted_optimization.csv'
        csv_global_file_path = create_resources_file_path(path_str)
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)
        pop = self.gen_opt.initialize_population()
        chromosome = self.gen_opt.decode_individual(pop[0])
        geometry_rel = self.gen_opt.update_model_parameters_targeted(chromosome)

        # assert that the number of turns per layer is the same
        assert 13 == sum([block.block_def.nco for block in geometry_rel.blocks[:4]])
        assert 19 == sum([block.block_def.nco for block in geometry_rel.blocks[4:7]])
        assert 29 == sum([block.block_def.nco for block in geometry_rel.blocks[7:10]])
        assert 39 == sum([block.block_def.nco for block in geometry_rel.blocks[10:]])

    def test_update_model_parameters_targeted_error(self):
        np.random.seed(1)

        # act
        path_str = 'resources/optimization/optim_input_enlarged_targeted_optimization.csv'
        csv_global_file_path = create_resources_file_path(path_str)
        df = pd.read_csv(csv_global_file_path)
        self.gen_opt.design_variables = RoxieGeneticOptimization.initialize_design_variables(df)
        pop = [[1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1,
                1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1,
                0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0]]

        chromosome = self.gen_opt.decode_individual(pop[0])
        geometry_rel = self.gen_opt.update_model_parameters_targeted(chromosome)

        # assert that the number of turns per layer is the same
        assert 13 == sum([block.block_def.nco for block in geometry_rel.blocks[:3]])
        assert 19 == sum([block.block_def.nco for block in geometry_rel.blocks[3:6]])
        assert 29 == sum([block.block_def.nco for block in geometry_rel.blocks[6:9]])
        assert 39 == sum([block.block_def.nco for block in geometry_rel.blocks[9:]])

