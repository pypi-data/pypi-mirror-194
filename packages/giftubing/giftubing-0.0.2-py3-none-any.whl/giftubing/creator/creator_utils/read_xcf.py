from gimpformats.gimpXcfDocument import GimpDocument

from .resize_choice import get_resize_input

def get_imgs_dict_from_xcf(xcf_file_full_path: str):
    """
    This file reads a gimp xcf file and output a dictonary (keys emotions)
    for each emotion a dict of {layername: layer_image}
    """
    print("BEGIN LOADING AVATAR DATA")
    list_emotions = ['Anger','Fear', 'Happiness','Neutral',
                    'Sadness','Surprise'] #,'Contempt', 'Disgust' 
    # Empty dict for layer images: keys are emotions
    dict_imgs = {k: None for k in list_emotions}

    # Open gimp project .xcf file:
    project = GimpDocument(xcf_file_full_path)
    layers = project.layers
    
    # get image shape from first layer:
    img_shape = (layers[0].width, layers[0].height)
    
    # Get user input regarding chosen resize:
    newsize = get_resize_input(img_shape)
    print(f"newsize: {newsize}")

    # Iterate over layers to extract images:
    current_group = None
    for layer in layers:
        if layer.isGroup:
            # New emotion
            current_group = layer.name
            print(f"Loading layer {layer.name}")
            continue
        # Verify layer size:
        if layer.width != img_shape[0]:
            raise ValueError(f"{current_group}/{layer.name}'s width is not {img_shape[0]}")
        if layer.height != img_shape[1]:
            raise ValueError(f"{current_group}/{layer.name}'s height is not {img_shape[1]}")

        if dict_imgs[current_group] is None:
            # initialize dict for emotion group
            dict_imgs[current_group] = {}
        # keys are layer names, values are layer images
        if newsize is not None:
            dict_imgs[current_group][layer.name] = layer.image.resize(newsize)
        else:
            dict_imgs[current_group][layer.name] = layer.image
        continue
    print("AVATAR DATA LOADED")
    if newsize is not None:
        img_shape = newsize
    return dict_imgs, img_shape


if __name__=="__main__":
    XCF_FILE_PATH = ""

    dict_results, shape = get_imgs_dict_from_xcf(XCF_FILE_PATH)
    print(dict_results)