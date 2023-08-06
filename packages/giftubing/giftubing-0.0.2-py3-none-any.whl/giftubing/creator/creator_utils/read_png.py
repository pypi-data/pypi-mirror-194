import os

from PIL import Image

from .resize_choice import get_resize_input

def get_imgs_dict_from_img(dict_image_source):
    """
    This file reads the contents of source folder and output a dictonary (keys emotions)
    for each emotion a dict of {layername: layer_image}
    """
    print("BEGIN LOADING AVATAR DATA")
    list_emotions = ['Anger','Fear', 'Happiness','Neutral',
                    'Sadness','Surprise'] #,'Contempt', 'Disgust' 
    #! make auto removal at end of func if emotion not present in file
    # Empty dict for layer images: keys are emotions
    dict_imgs = {k: None for k in list_emotions}

    # get image shape from first image:
    first_im = Image.open(list(dict_image_source.values())[0][0])
    img_shape = (first_im.width, first_im.height)
    
    # Get user input regarding chosen resize:
    newsize = get_resize_input(img_shape)
    print(f"newsize: {newsize}")

    for emotion in list_emotions:
        if emotion not in dict_image_source.keys():
            # Skip emotions without source
            continue
        print(f"Loading layer {emotion}")
        for impath in dict_image_source[emotion]:
            if dict_imgs[emotion] is None:
                # initialize dict for emotion group
                dict_imgs[emotion] = {}
            if newsize is not None:
                dict_imgs[emotion][os.path.basename(impath)] = Image.open(impath).resize(newsize)
            else:
                dict_imgs[emotion][os.path.basename(impath)] = Image.open(impath)
    print("AVATAR DATA LOADED")
    if newsize is not None:
        img_shape = newsize
    return dict_imgs, img_shape


if __name__=="__main__":
    IMAGE_FOLDER_PATH = ""

    dict_results, shape = get_imgs_dict_from_img(IMAGE_FOLDER_PATH)
    print(dict_results)