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
"""Utility function to convert layer to akida.
"""

import quantizeml
from quantizeml.layers import QuantizedMaxPool2D, QuantizedReLU

from .pooling import parse_max_pooling
from .activations import parse_relu


def get_inbound_layers(ak_model, k_layer):
    """Returns the inbound layers in an Akida model from a Keras layer.

    Args:
        ak_model (:obj:`Model`): the model where to find the inbounds layers.
        k_layer (:obj:`tf.keras.Layer`): the source layer.

    Returns:
        :list: the inbounds layers names.
    """

    # The list of supported Keras layers not represented in Akida
    skippable_layers = (quantizeml.layers.QDropout, quantizeml.layers.QuantizedFlatten,
                        quantizeml.layers.QuantizedReshape, quantizeml.layers.QuantizedRescaling,
                        quantizeml.layers.QuantizedReLU)

    # Get inbound layers names
    in_node = k_layer._inbound_nodes[0]
    inbound_layers = in_node.inbound_layers
    if not isinstance(inbound_layers, list):
        inbound_layers = [inbound_layers]
    for layer in inbound_layers:
        if type(layer) in skippable_layers:
            inbound_layers = get_inbound_layers(ak_model, layer)
    return [ak_model.get_layer(ly.name) for ly in inbound_layers]


def parse_non_neural_layers(layers, neural_params):
    """Parse no neural layers into the parameters of one.

    We are able to manage this sequence of layers:

    - QuantizedMaxPooling2D,
    - QuantizedRelU.

    Args:
        layers (list(:obj:`tf.keras.Layer`)): the block layers.
        neural_params (dict): initial neural parse parameters.

    Returns:
        list(:obj:`tf.keras.Layer`): no neural layers found in process.
    """
    # Identify the next layers
    next_layers = []
    layer_types = [QuantizedMaxPool2D, QuantizedReLU]
    index = 1
    while index < len(layers) and layer_types:
        layer_type = layer_types.pop(0)
        layer = layers[index]
        if isinstance(layer, layer_type):
            next_layers.append(layer)
            index += 1

    # Evaluate the neural layer parameters
    neural_name = layers[0].name
    for layer in next_layers:
        if isinstance(layer, QuantizedMaxPool2D):
            pool_params = parse_max_pooling(layer)
            if pool_params["padding"] != neural_params["padding"]:
                raise ValueError(f"{layer.name} must have the same padding as {neural_name}.")
            neural_params.update(pool_params)
        if isinstance(layer, QuantizedReLU):
            act_params = parse_relu(layer)
            neural_params.update(act_params)

    return next_layers
