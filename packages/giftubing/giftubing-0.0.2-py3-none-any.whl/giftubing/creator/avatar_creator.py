
import os
from itertools import product

from PIL import Image

from .creator_utils.read_xcf import get_imgs_dict_from_xcf
from .creator_utils.read_png import get_imgs_dict_from_img
from ..launcher.utils.parts import Mouth, Eyes

def get_layer_order(dict_layers):
    """
    Create and returns a dict ordering layer stack order by their name:
    {0: ['body_layername']} is first, then 1: ['mouth_closed_layername', 'mouth_open_layername'], 
            finally 2&3: 'eyes_layernames'}
    keys represent layer stack order
    """
    # create empty dict with key layer priority (int) and value empty list
    dict_results = dict(zip(range(4), ([] for i in range(4))))
    for layername in dict_layers.keys():
        if "body" in layername:
            dict_results[0].append(layername)
        elif "mouth" in layername:
            dict_results[1].append(layername)
        elif "eye" in layername:
            if "left" in layername:
                dict_results[2].append(layername)
            elif "right" in layername:
                dict_results[3].append(layername)
            else:
                raise ValueError(f"Layer name: {layername} has 'eye' but no 'left' and no 'right'")
        else:
            print(f"Layer name {layername} not supported yet ('body', 'mouth' or 'eye' only for now")
    # sort dictionary by keys to be sure that stack is in correct order
    dict_results = dict(sorted(dict_results.items()))
    # Check:
    for k, v in dict_results.items():
        if len(v) == 0:
            d = {0: "body", 1: "mouth", 2: "left_eye", 3: "right_eye"}
            raise ValueError(f"No layer found for '{d[k]}', it must be found in the layer name")
    return dict_results

def get_frame(dict_avatar, 
                avatar_shape,
                emotion,
                is_mouth_open,
                is_mouth_wide,
                is_left_eye_open,
                is_right_eye_open
            ):
    """
    Creates a frame from the different layers, given an emotion and
    the boolean info.
    Works by creating an empty frame of size avatar_shape, then
    iterating on layer stack order, pasting the correct combination of layers
    on top of the formerly empty frame and returning the result.
    """
    # create empty image of correct size:
    frame = Image.new('RGBA', avatar_shape, (0, 0, 0, 0))

    # get dict of layers for chosen emotion:
    dict_layers = dict_avatar[emotion]

    # Create objects from boolean infos:
    curmouth = Mouth(is_mouth_open, is_mouth_wide)
    cureyes = Eyes(is_left_eye_open, is_right_eye_open)

    # Get {int(layer order): ['layername1', 'layername2', ...], }:
    dict_layernames = get_layer_order(dict_layers)

    # Iterate over all 4 layer levels, paste the correct one to returned frame
    for i, list_layer_names in dict_layernames.items():
        if i == 0:
            # body
            if len(list_layer_names) != 1:
                raise ValueError(f"Exactly one layer per emotion should have 'body': {list_layer_names}")
            # Paste body
            frame.paste(dict_layers[list_layer_names[0]], (0, 0), dict_layers[list_layer_names[0]])
            continue
        if i == 1:
            # mouth
            idx = 0
            while True:
                try:
                    layername = list_layer_names[idx]
                    idx += 1
                except IndexError:
                    raise Exception(f"No layer with {curmouth.status} found in {list_layer_names}")
                if curmouth.status in layername:
                    # Paste correct mouth
                    frame.paste(dict_layers[layername], (0, 0), dict_layers[layername])
                    break
        if i == 2:
            # left eye
            idx = 0
            while True:
                try:
                    layername = list_layer_names[idx]
                    idx += 1
                except IndexError:
                    raise Exception(f"No layer with {cureyes.left} found in {list_layer_names}")
                if cureyes.left in layername:
                    # Paste correct eye
                    frame.paste(dict_layers[layername], (0, 0), dict_layers[layername])
                    break
        if i == 3:
            # right eye
            idx = 0
            while True:
                try:
                    layername = list_layer_names[idx]
                    idx += 1
                except IndexError:
                    raise Exception(f"No layer with {cureyes.right} found in {list_layer_names}")
                if cureyes.right in layername:
                    # Paste correct eye
                    frame.paste(dict_layers[layername], (0, 0), dict_layers[layername])
                    break
    # Frame created!
    return frame

def generate_images(dictlayers: dict, shape: tuple, avatars_dir_path: str):
    """
    For all emotions and combinations of boolean values of eyes and mouth info,
    creates and save the corresponding image file.
    """
    # init lists
    list_emotions = ['Anger','Fear', 'Happiness','Neutral',
                    'Sadness','Surprise'] #,'Contempt', 'Disgust' #! make auto removal at end of func
    # start image generation
    for emotion in list_emotions:
        if dictlayers[emotion] is None:
            continue
        # create emotion folder
        list_infos = list(product([True,False], repeat=4))
        for info in list_infos:
            if (info[0] is False) and (info[1] is True):
                #print("mouth cannot be closed and open simultaneously")
                filename = os.path.join(avatars_dir_path, "empty.png")
                empty_image = Image.new('RGBA', shape, (0, 0, 0, 0))
                empty_image.save(filename)
                continue
            # create frame from layers and info:
            image = get_frame(dictlayers, 
                                    shape,
                                    emotion,
                                    info[0], #is_mouth_open, 
                                    info[1], #is_mouth_wide,
                                    info[2], #is_left_eye_open 
                                    info[3] #is_right_eye_open, 
                                    )
            mouth = Mouth(info[0], info[1])
            eyes = Eyes(info[2], info[3])
            # name image:
            filename = os.path.join(avatars_dir_path, emotion + mouth.name + eyes.name + ".png")
            # save image:
            image.save(filename)
    print(f"Avatar {os.path.basename(avatars_dir_path)} created!")
    print(f"Full path: {os.path.abspath(avatars_dir_path)}")

def create_avatar(dir_path):
    """
    Creates two folders inside dir_path:
        - giftubing_sources needs to contain folder of images for avatar creation
        - giftubing_avatars will contain generated avatars for use by launcher
    Fills two dictionaries with available avatars for creation, from images
        and from gimp project files (.xcf):
        - dict_xcf_avatars = {'avatar_name':'file_path_of_.xcf'}
        - dict_png_avatars = {'avatar_name':{'emotion':['body.png', 'right eye.png', ...]}}
    Remove avatars already created before getting user input of which source to use
        to create the avatar
    Gets a dictionary of images for generation.
    Generates avatar.
    """
    print('\n\n\n\n')
    list_emotions = ['Anger','Fear', 'Happiness','Neutral',
                    'Sadness','Surprise']
    source_dir_path = os.path.join(dir_path,"giftubing_sources")
    avatars_dir_path = os.path.join(dir_path,"giftubing_avatars")

    if not os.path.isdir(avatars_dir_path):
        os.mkdir(avatars_dir_path)
        print(f"Folder giftubing_avatars created! avatars will be created here:\n {os.path.abspath(avatars_dir_path)}")

    must_place_files = False
    if not os.path.isdir(source_dir_path):
        os.mkdir(source_dir_path)
        print(f"Folder giftubing_sources created! Place sources folders here:\n {os.path.abspath(source_dir_path)}")
        must_place_files = True

    if must_place_files:
        while True:
            val = input("Copy your avatar to giftubing_sources folder, then press ENTER key\n")
            if val == "":
                break

    # Get all avatars information
    dict_xcf_avatars = {} # {'avatar_name':'file_path_of_.xcf'}
    dict_png_avatars = {} # {'avatar_name':{'emotion':['body.png', 'right eye.png', ...]}}
    for elem in os.listdir(source_dir_path):
        elem_fullpath = os.path.join(source_dir_path,elem)
        if os.path.isfile(elem_fullpath):
            # file in main dir, if .xcf then it's an avatar from gimp
            if elem_fullpath[-4:] == ".xcf":
                dict_xcf_avatars[elem[:-4]] = elem_fullpath # {'avatar_name':'file_path_of_.xcf'}
            continue

        if all([os.path.isfile(os.path.join(elem_fullpath,x)) for x in os.listdir(elem_fullpath)]):
            # One folder, containing files only (images)
            # Single emotion avatar
            dict_png_avatars[elem] = {"Neutral":[os.path.join(elem_fullpath, x) for x in os.listdir(elem_fullpath)]}
            continue

        # avatar from image, and consists of several subfolders for each emotion
        dict_png_avatars[elem] = {key: [] for key in list_emotions}
        for dir in os.listdir(elem_fullpath):
            if dir not in list_emotions:
                print(f"Name of folder {dir} inside folder {elem} is not among {list_emotions}")
                continue
            max_path = os.path.join(elem_fullpath, dir)
            dict_png_avatars[elem][dir] = [os.path.join(max_path, x) for x in os.listdir(max_path)]

        # remove empty lists (unused emotions)
        dict_png_avatars[elem] = {k:v for k, v in dict_png_avatars[elem].items() if len(v) > 0}

    # Remove already made avatars from list of offered avatars.
    list_already_made_avatars = os.listdir(avatars_dir_path)
    list_avatars_sources = [x for x in dict_xcf_avatars.keys()] + [x for x in dict_png_avatars.keys()]
    sources_to_skip = []
    for avatar_to_create in list_avatars_sources:
        if avatar_to_create in list_already_made_avatars:
            print(f"{avatar_to_create} already created in {avatars_dir_path}")
            sources_to_skip.append(avatar_to_create)
    list_avatars_sources = [x for x in list_avatars_sources if not x in sources_to_skip]
    
    # Get user input for avatar creation
    print("\n\n\n\nSelect which avatar to create from these sources:\n")
    for i, avatar_option in enumerate(list_avatars_sources):
        print(f"{i}: {avatar_option}")
    choice_is_valid = False
    while not choice_is_valid:
        choice = input("\nEnter avatar number:")
        try:
            avatar_choice = int(choice)
        except ValueError:
            print(f"Input must be an integer: {choice} is not valid")
        if avatar_choice < 0:
            print(f"{choice} must be greater than or equal to zero")
        elif avatar_choice < len(list_avatars_sources):
            avatar_to_create = list_avatars_sources[avatar_choice]
            choice_is_valid = True
        else:
            print(f"{avatar_choice} is not valid; {[x for x in range(len(list_avatars_sources))]} are valid options")

    # Find chosen avatar, and get its dicts of images for generation
    if avatar_to_create in dict_xcf_avatars.keys():
        avatar_path = dict_xcf_avatars[avatar_to_create]
        dict_imgs, img_shape = get_imgs_dict_from_xcf(avatar_path)

    if avatar_to_create in dict_png_avatars.keys():
        images_paths = dict_png_avatars[avatar_to_create]
        dict_imgs, img_shape = get_imgs_dict_from_img(images_paths)

    # create avatar folder:
    avatar_folder = os.path.join(avatars_dir_path, avatar_to_create)
    os.mkdir(avatar_folder)

    # generate avatar:
    generate_images(dict_imgs, img_shape, avatar_folder)

if __name__=="__main__":
    create_avatar()