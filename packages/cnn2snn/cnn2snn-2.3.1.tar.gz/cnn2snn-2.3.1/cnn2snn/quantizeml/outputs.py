#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Functions to update akida layer output variables from a keras OutputQuantizer.
"""
import numpy as np
from quantizeml.layers import OutputQuantizer
from quantizeml.tensors import FixedPoint, pow2

from ..akida_versions import AkidaVersion, get_akida_version
from .weights import broadcast_and_set_variable


def set_output_variables(layer_ak, out_quantizer):
    """Computes and sets the output variables in an akida layer.

    Args:
        layer_ak (:obj:`akida.Layer`): the targeted akida layer.
        out_quantizer (:obj:`quantizeml.OutputQuantizer`): the source output quantizer.
    """
    assert isinstance(out_quantizer, OutputQuantizer)

    # Extract the OutputQuantizer variables
    scales = out_quantizer.qscales.value.values
    shift = out_quantizer.shift.value

    # We evaluate the outputs as:
    #   y = x / act_step in akida 1.0
    #   y = x * scales * 2^shift In akida 2.0
    if get_akida_version() == AkidaVersion.v1:
        # Calculate the act_step, as the reciprocal of (scales * 2^shift)
        act_step = pow2(-shift) / scales
        # Quantize act_step on 24-bit with 4 fractional bits
        act_step = FixedPoint.quantize(act_step, 24, 4)
        # Store the dequantized act_step float value
        layer_ak.variables["act_step"] = act_step.to_float().numpy().astype(np.float32)
    else:
        output_scales = scales.numpy().astype(np.uint8)
        broadcast_and_set_variable(layer_ak.variables, "output_scales",
                                   output_scales)
        layer_ak.variables["output_shift"] = shift.numpy().astype(np.int8)
