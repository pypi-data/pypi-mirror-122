from copy import deepcopy

from magnumapi.geometry.Geometry import Geometry
from magnumapi.geometry.blocks.Block import Block
from magnumapi.geometry.blocks.CosThetaBlock import AbsoluteCosThetaBlock
from magnumapi.geometry.primitives.Line import Line


class GeometryChange:
    @classmethod
    def calculate_radial_alpha(cls, geometry: Geometry) -> Geometry:
        """ Method correcting radiality of cos-theta blocks in a geometry.

        """
        # check whether areas were initialize before performing radiality correction
        is_any_area_initialized = any([area for block in geometry.blocks for area in block.areas])

        # Set alpha equal to phi for all blocks except the mid-plane
        geometry = cls._set_alpha_equal_to_phi(geometry)

        # Build blocks and calculate turn positions
        geometry.build_blocks()

        # Calculate alpha corrections
        alpha_corrections = cls._calculate_alpha_corrections(geometry)

        # Correct alpha
        geometry = cls._apply_alpha_correction(geometry, alpha_corrections)

        # Return to the external context of the geometry before entering
        if is_any_area_initialized:
            geometry.build_blocks()
        else:
            geometry.empty_block_areas()

        return geometry

    @staticmethod
    def _set_alpha_equal_to_phi(geometry):
        for layer_def in geometry.layer_defs:
            for block_index in layer_def.blocks[1:]:
                index_in_blocks = geometry.get_index_in_blocks_for_layer_block_index(block_index)
                block = geometry.blocks[index_in_blocks]
                if isinstance(block, AbsoluteCosThetaBlock):
                    block.block_def.alpha = block.block_def.phi
        return geometry

    @classmethod
    def _calculate_alpha_corrections(cls, geometry):
        alpha_corrections = []
        for layer_def in geometry.layer_defs:
            for index, block_index in enumerate(layer_def.blocks):
                index_in_blocks = geometry.get_index_in_blocks_for_layer_block_index(block_index)
                block = geometry.blocks[index_in_blocks]
                # Calculate correction for all blocks except the mid-plane one
                if index and isinstance(block, AbsoluteCosThetaBlock):
                    alpha_correction = cls.compute_radial_alpha(block)
                else:
                    alpha_correction = 0.0
                alpha_corrections.append(alpha_correction)

        return alpha_corrections

    @staticmethod
    def compute_radial_alpha(block: Block) -> float:
        """ Static method calculating a radiality correction angle for a cos-theta block. It is based on an assumption
        that block alpha angle (inclination angle) is equal to phi angle (positioning angle).

        :param block: a block instance with initialized areas
        :return: an alpha angle correction factor
        """
        if not block.areas:
            raise IndexError('The list of areas is empty, please build block first with build_block() method.')

        l_down = block.areas[0].get_line(0)
        p_down = l_down.p1
        l_up = block.areas[-1].get_line(2)
        p_up = l_up.p2

        angle_ref = (p_up.get_phi() + p_down.get_phi()) / 2

        alpha_down = angle_ref - Line.calculate_relative_alpha_angle(l_down)
        alpha_up = Line.calculate_relative_alpha_angle(l_up) - angle_ref

        return (alpha_down - alpha_up) / 2

    @staticmethod
    def _apply_alpha_correction(geometry, alpha_corrections):
        for index, block in enumerate(geometry.blocks):
            if isinstance(block, AbsoluteCosThetaBlock):
                block.block_def.alpha += alpha_corrections[index]

        return geometry

    @classmethod
    def update_layer_indexing(cls, geometry) -> Geometry:
        """ Method updating block and layer indexing in case a block has no turns.
        The algorithm works as follows:
        1. Take old block indices and map them to None
        2. Keep blocks with at least one conductor
        3. Update the numbering of blocks; update mapping from old to new indices from point 1
        4. Update block indices in each layer definition with map; if a new index is None, then it means that a block
        was removed

        :return: method returns a dictionary from old to new block indices
        """
        # # initialize map
        geometry = deepcopy(geometry)
        old_to_new_index = {block.block_def.no: None for block in geometry.blocks}

        # # remove the missing blocks
        # # keep only block indices that are not missing
        blocks = []
        for index, block in enumerate(geometry.blocks):
            if block.block_def.nco > 0:
                blocks.append(block)
                old_to_new_index[block.block_def.no] = block.block_def.no

        geometry.blocks = blocks

        # # update layers definition
        for layer_def in geometry.layer_defs:
            layer_def.blocks = [old_to_new_index[block] for block in layer_def.blocks]
            layer_def.blocks = [block for block in layer_def.blocks if block is not None]

        return geometry

    @classmethod
    def update_phi_r(cls, geometry, chromosome):
        geometry = deepcopy(geometry)
        for block_index_variable, value in chromosome.items():
            if ':phi_r' in block_index_variable:
                block_index, variable = block_index_variable.split(':')
                block_index = int(block_index)
                for block in geometry.blocks:
                    if block.block_def.no == block_index:
                        block.block_def.phi_r = value

        return geometry

    @classmethod
    def update_nco_r(cls, geometry, chromosome):
        geometry = deepcopy(geometry)
        for block_index_variable, value in chromosome.items():
            if ':nco_r' in block_index_variable:
                block_index, variable = block_index_variable.split(':')
                block_index = int(block_index)

                # ToDo: this requires a correction in case the next one would receive some
                block_def_curr = geometry.blocks[block_index - 1].block_def
                block_def_next = geometry.blocks[block_index].block_def
                if value >= 0:
                    block_def_curr.nco += min(value, block_def_next.nco)
                    block_def_next.nco -= min(value, block_def_next.nco)
                else:
                    block_def_curr.nco -= min(abs(value), block_def_curr.nco)
                    block_def_next.nco += min(abs(value), block_def_next.nco)
        geometry = GeometryChange.update_layer_indexing(geometry)
        return geometry

    @classmethod
    def update_alpha_radial(cls, geometry, chromosome):
        geometry = deepcopy(geometry)
        for block_index_variable, value in chromosome.items():
            if ':alpha_rad_r' in block_index_variable:
                block_index = block_index_variable.split(':')[0]
                block_index = int(block_index)
                for block in geometry.blocks:
                    if block.block_def.no == block_index:
                        block.block_def.alpha_r += value

        return geometry
