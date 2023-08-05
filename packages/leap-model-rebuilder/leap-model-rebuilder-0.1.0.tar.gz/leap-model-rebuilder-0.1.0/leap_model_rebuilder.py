import tensorflow as tf

def get_relevant_nodes(layer, _model):
    relevant_model_nodes = []
    for v in _model._nodes_by_depth.values():
      relevant_model_nodes += v

    relevant_nodes = []
    for node in layer._inbound_nodes:
        if relevant_model_nodes and node not in relevant_model_nodes:
            # node is not part of the current network
            continue
        relevant_nodes.append(node)
    return relevant_nodes

def rebuild_model(_model, layers_to_remove=[], layers_to_replace={}, inject_after={}):
    tensors = {}
    input_tensors = {}

    print('Scanning for input...')
    for layer in _model.layers:
        if layer.__class__.__name__ == 'InputLayer':
            print(f'Processing: {layer.name} ({layer.__class__.__name__})')
            shape = layer.input_shape[0][1:]
            input_tensor = layer.call(tf.keras.Input(shape=shape, name=layer.name))
            tensors[layer.name] = input_tensor
            input_tensors[layer.name] = input_tensor

    for idx, layer in enumerate(_model.layers):
        if layer.__class__.__name__ == 'InputLayer':
            continue

        relevant_nodes = get_relevant_nodes(layer, _model)

        print(f'Processing: {layer.name} ({layer.__class__.__name__})')

        # Layers to remove handler
        if layer.name in layers_to_remove:
            tensor = tensors[relevant_nodes[0].input_tensors.name.split('/')[0]]
            tensors[layer.name] = tensor
            continue

        # Layers to replace handler
        if layer.name in layers_to_replace.keys():
            replace_with = layers_to_replace[layer.name]
            if not isinstance(replace_with, list):
                replace_with = [replace_with]
            tensor = tensors[relevant_nodes[0].input_tensors.name.split('/')[0]]
            tensors[layer.name] = tensor
            for replace_with_layer in replace_with:
                tensors[layer.name] = replace_with_layer(tensors[layer.name])
            continue


        if isinstance(layer.input, list):
            inputs = []
            for tensor in relevant_nodes[0].input_tensors:
                layer_input_name = tensor.name.split('/')[0]
                tensor = tensors[layer_input_name]
                if isinstance(tensor, list) and len(tensor) == 1:
                    tensor = tensor[0]
                inputs.append(tensor)
            tensors[layer.name] = layer(inputs)

        else:
            tensor = tensors[relevant_nodes[0].input_tensors.name.split('/')[0]]
            if isinstance(tensor, list) and len(tensor) == 1:
                tensor = tensor[0]
            tensors[layer.name] = layer(tensor)

        # Inject after handler
        if layer.name in inject_after.keys():
            injected_layers = inject_after[layer.name]
            if not isinstance(injected_layers, list):
                injected_layers = [injected_layers]
            for injected_layer in injected_layers:
                tensors[layer.name] = injected_layer(tensors[layer.name])
            continue

    orig_model_output_name = _model.output.name.split('/')[0]
    rebuilt_model = tf.keras.Model(inputs=list(input_tensors.values()), outputs=tensors[orig_model_output_name])

    return rebuilt_model
