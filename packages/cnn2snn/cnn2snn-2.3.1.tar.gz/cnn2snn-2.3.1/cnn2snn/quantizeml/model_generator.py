#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
"""Parsing functions to generate an Akida model from a Keras model quantized with quantizeml api.
"""

import quantizeml.layers as qlayers
from quantizeml.models import record_quantization_variables
from akida import Model

from .dense import convert_dense_block
from .add import convert_quantized_add
from .input_data import convert_input
from .shiftmax import convert_quantized_shiftmax
from .attention import convert_quantized_attention
from .madnorm import convert_quantized_madnorm
from .stem import convert_quantized_stem_layers
from .concatenate import convert_quantized_concatenate
from .convolution import convert_conv_block
from .separable_convolution import convert_sepconv_block
from .batchnorm import convert_batchnorm_block
from ..akida_versions import AkidaVersion, get_akida_version


def generate_model(model, input_is_image):
    """Generates an Akida model.

    This function creates an Akida model by iterating through the layers of the
    quantized model. For each layer, the corresponding akida layer is created and
    added to the Akida model.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model to convert.
        input_is_image (bool): True if input is an 8-bit unsigned tensors (like images).

    Returns:
        :obj:`akida.Model`: the generated Akida model.
    """

    # First store necessary variables for conversion
    record_quantization_variables(model)

    model_ak = Model()

    # Set index of first layer to be checked
    index = 1
    if isinstance(model.layers[1], qlayers.QuantizedRescaling):
        # ignore rescaling
        index += 1
    # Identify the input block
    ak_version = get_akida_version()
    input_block_size = 0
    if ak_version == AkidaVersion.v2:
        # Convert the akida 2.0 stem block layer if the keras model has one.
        input_block_size = convert_quantized_stem_layers(model_ak, model.layers[index:])
    if input_block_size == 0:
        # Look for an input convolution layer
        input_block_size = convert_conv_block(model_ak, model.layers[index:])
    if input_block_size == 0:
        # Convert the keras InputLayer into an InputData layer
        convert_input(model_ak, model.layers[0], input_is_image)
    index += input_block_size

    # Convert the remaining layers. A while is used to be able to advance if needed.
    layers_size = len(model.layers)

    while index < layers_size:
        layer = model.layers[index]
        # Create and add layer to the akida model
        # The next check converts the potential dense_block layers to a QuantizedDense,
        block_size = convert_dense_block(model_ak, model.layers[index:])
        if block_size > 0:
            index += block_size
            continue
        # conv_block layers to a QuantizedConv2D
        block_size = convert_conv_block(model_ak, model.layers[index:])
        if block_size > 0:
            index += block_size
            continue
        # and sepconv_block to a QuantizedSeparableConv2D
        block_size = convert_sepconv_block(model_ak, model.layers[index:])
        if block_size > 0:
            index += block_size
            continue
        # The other modules are for v2 only
        if get_akida_version() != AkidaVersion.v2:
            # If you got here, the layer is not supported: raise an error.
            raise RuntimeError(f"Layer {layer.name}: unsupported type "
                               f"{layer.__class__.__name__}.")
        block_size = convert_batchnorm_block(model_ak, model.layers[index:])
        if block_size > 0:
            index += block_size
            continue
        if isinstance(layer, qlayers.QuantizedAdd):
            convert_quantized_add(model_ak, layer)
        elif isinstance(layer, qlayers.QuantizedShiftmax):
            convert_quantized_shiftmax(model_ak, layer)
        elif isinstance(layer, qlayers.QuantizedAttention):
            convert_quantized_attention(model_ak, layer)
        elif isinstance(layer, qlayers.QuantizedLayerNormalization):
            convert_quantized_madnorm(model_ak, layer)
        elif isinstance(layer, qlayers.QuantizedConcatenate):
            convert_quantized_concatenate(model_ak, layer)
        else:
            # If you got here, the layer is not supported: raise an error.
            raise RuntimeError(f"Layer {layer.name}: unsupported type "
                               f"{layer.__class__.__name__}.")
        index += 1

    return model_ak
