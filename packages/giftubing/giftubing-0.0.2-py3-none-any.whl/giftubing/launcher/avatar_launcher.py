import os
import sys
#from time import perf_counter
from itertools import product

import keyboard
from torch import cuda
from facenet_pytorch import MTCNN
import cv2
from hsemotion.facial_emotions import HSEmotionRecognizer
import mediapipe as mp
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QImageReader, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow

from .utils.get_face import Face_boundary
from .utils.parts import get_filename, Mouth, Eyes
from .utils.facemesher import Facemesher


class emotion_filter():
    """
    Controls whether displayed 
    emotion is automatic through face emotion detection,
    or is toggled through key input.
    Also makes sure that missing emotions do not impact usage.
    """
    toggle_fixed_emotion = False
    fixed_num = "1"

    def __init__(self, list_emotions, list_unused_emotions) -> None:
        self.list_unused_emotions = list_unused_emotions
        self.dict_fixed = {str(k+1):v for k, v in enumerate([x for x in list_emotions if x not in list_unused_emotions])}
        keyboard.add_hotkey(str(0), self.toggle_autoemotions)

        print("\n\nPress '0' key to toggle automatic or manual emotion. Currently auto.")
        for key, value in self.dict_fixed.items():
            keyboard.add_hotkey(str(key), self.change_key, args=(str(key),))
            print(f"Press key '{key}' to display emotion {value}")


    def __getitem__(self, value):
        if self.toggle_fixed_emotion:
            return self.dict_fixed[self.fixed_num]
        if value in self.list_unused_emotions:
            return "Neutral"
        return value

    def change_key(self, new_value):
        self.fixed_num = new_value

    def toggle_autoemotions(self):
        print('toggling')
        if self.toggle_fixed_emotion:
            self.toggle_fixed_emotion = False
        else:
            self.toggle_fixed_emotion = True


class Giftube(QWidget): 
    """
    Widget displaying avatar frames in a QLabel,
    contains the main loop.
    """
    def __init__(self, parent=None, avatar_path=None): 
        QWidget.__init__(self, parent)

        # load all frames:
        self.load_frames(avatar_path)

        # init avatar values:
        EMOTION_INERTIA_VAL = 5

        self.list_emotion = ["Neutral" for x in range(EMOTION_INERTIA_VAL)]
        self.current_emotion = "Neutral"
        self.is_mouth_open = True
        self.is_mouth_wide = False
        self.is_right_eye_open = True
        self.is_left_eye_open = True

        # Label for displaying image:
        self.label = QLabel()

        # layout:
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.label)
        self.setLayout(main_layout) 

        # Init first frame:
        first_frame_path = get_filename(
                                "Neutral",
                                self.is_mouth_open, 
                                self.is_mouth_wide, 
                                self.is_left_eye_open,
                                self.is_right_eye_open 
                            )
        reader = QImageReader(first_frame_path)
        image = reader.read().copy() #.copy(*self.cropvals)
        self.curframe = QPixmap().fromImage(image)
        self.label.setPixmap(self.curframe)
        self.show()

        print("initializing webcam")
        self.cap = cv2.VideoCapture(0)
        W, H = 720, 480 # 1280, 720 # 1920, 1080
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

        print('loading neural networks')
        self.device = 'cuda' if cuda.is_available() else 'cpu'
        self.fer=HSEmotionRecognizer(model_name='enet_b0_8_best_afew',device=self.device)
        #list_fer_models = ['mobilenet_7.h5', 
        #                'enet_b0_8_best_afew.pt', # 8 classes, ~60ms inference time
        #                'enet_b0_8_best_vgaf.pt',
        #                'enet_b0_8_va_mtl.pt',
        #                'enet_b0_7.pt',
        #                'enet_b2_7.pt',
        #                'enet_b2_8.pt',
        #                'enet_b2_8_best.pt']
        self.mtcnn = MTCNN(keep_all=False, 
                            post_process=False, 
                            min_face_size=40, 
                            device="cpu") #! For some reason cpu is faster than gpu for mtcnn on my computer. wut.
                            #image_size=224) #default size for HSEmotionRecognizer
        self.mp_face_mesh = mp.solutions.face_mesh

        print("loading utils")
        self.process_face = Face_boundary(self.mtcnn)
        self.process_infos = Facemesher(self.mp_face_mesh)

        while not self.cap.isOpened():
            print("waiting cam")

        # define variables for giftubing loop:
        COMPUTE_EMOTION_LOOP_VAL = 10

        self.cnt_limit = COMPUTE_EMOTION_LOOP_VAL
        self.stop_app = False
        self.cropped_face = None
        self.cnt = 0
        self.is_visible = True

        # Define hotkeys:
        keyboard.add_hotkey('alt+t', self.toggleVisibility)
        keyboard.add_hotkey('alt+q', self.quit_app)

        print("Starting")
        QTimer.singleShot(10, self.giftubing)

    def toggleVisibility(self):
        """
        Toggles label visibility
        """
        if self.is_visible:
            print("Invisible")
            self.is_visible = False
        else:
            print("Visible")
            self.is_visible = True

    def load_frames(self, avatardir_path):
        """
        Loads all frames in self.dict_frames for use in
        main loop.
        """
        print('begin loading frames')
        list_emotions = ['Anger','Fear', 'Happiness','Neutral',
                        'Sadness','Surprise']
        unused_emotions = []

        self.dict_frames = {}
        for emotion in list_emotions:
            # Generate all possibilities for finding files
            # See Mouth and Eyes objects for explanation
            list_infos = list(product([True,False], repeat=4))
            for info in list_infos:
                if (info[0] is False) and (info[1] is True):
                    #"mouth cannot be closed and open simultaneously
                    continue
                filename = get_filename(
                            emotion,
                            info[0], #is_mouth_open, 
                            info[1], #is_mouth_wide,
                            info[2], #is_left_eye_open 
                            info[3] #is_right_eye_open, 
                        )
                file_path = os.path.join(avatardir_path, filename)
                reader = QImageReader(file_path)
                image = reader.read().copy() #.copy(*self.cropvals)
                image = QPixmap().fromImage(image)
                if image.isNull():
                    unused_emotions.append(emotion)
                mouth = Mouth(info[0], info[1])
                eyes = Eyes(info[2], info[3])
                self.dict_frames[emotion + mouth.name + eyes.name] = image

        # Init of emotion filter:
        unused_emotions = list(set(unused_emotions))
        self.emofilter = emotion_filter(list_emotions, unused_emotions)
        
        # Set empty frame
        filename = os.path.join(avatardir_path, "empty.png")
        reader = QImageReader(filename)
        image = reader.read().copy() #.copy(*self.cropvals)
        self.invisible_frame = QPixmap().fromImage(image)

        print('frames loaded!')
        if len(unused_emotions) > 0:
            print(f"Unable to create {unused_emotions} emotions")

    def giftubing(self):
        """
        Main loop. Gets the frame, passes it to the neural
        networks to get info, changes the frame accordingly
        """
        #t1 = perf_counter()
        success, self.frame = self.cap.read() 
        self.cnt +=1
        if (success) and (self.is_visible):
            # Run Face_boundary from utils, get frame cropped to bounding box of face
            self.process_face.run(self.frame)
            if self.process_face.face_image is not None:
                self.cropped_face = self.process_face.face_image

            if self.cropped_face is not None:
                # Run Facemesher to get infos for choosing which avatar frame to display
                self.process_infos.run(self.cropped_face)
                self.is_mouth_open, self.is_mouth_wide, self.is_right_eye_open,\
                    self.is_left_eye_open = self.process_infos.is_mouth_open, \
                        self.process_infos.is_mouth_wide, self.process_infos.is_right_eye_open, \
                            self.process_infos.is_left_eye_open

                # Every CNT_LIMIT frames, get emotion
                # Done this way to keep good overall display framerate
                if self.cnt > self.cnt_limit:
                    self.cnt = 0
                    frame_emotion, scores = self.fer.predict_emotions(self.cropped_face,logits=True)
                    # remove oldest emotion, add newest emotion to list:
                    self.list_emotion.pop(0)
                    self.list_emotion.append(frame_emotion)
                    # current emotion is most recurring in list:
                    self.current_emotion = max(set(self.list_emotion), key = self.list_emotion.count)
                    self.current_emotion = self.emofilter[self.current_emotion]
            # Display avatar frame from information:
            mouth = Mouth(self.is_mouth_open, self.is_mouth_wide)
            eyes = Eyes(self.is_left_eye_open, self.is_right_eye_open)
            self.curframe = self.dict_frames[self.current_emotion + mouth.name + eyes.name]
            self.label.setPixmap(self.curframe)
        elif (success) and not (self.is_visible):
            self.label.setPixmap(self.invisible_frame)
        else:
            print('missed frame from cam')
        #t2 = perf_counter()
        #print(f"Time: {(t2-t1)*10**3} ms") 
        self.show()
        if not self.stop_app:
            # Loop
            QTimer.singleShot(10,  self.giftubing) 
        else:
            sys.exit()

    def quit_app(self):
        # Stop the loop and exit
        self.stop_app = True
        sys.exit()
        #QCoreApplication.quit()

class WindowTube(QMainWindow):
    """
    Main window, has a Giftube object as mainwidget
    """
    def __init__(self, dir_path):
        super(WindowTube, self).__init__()
        
        print("Setting window attributes")
        self.setWindowTitle("Giftubing")
        #self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Find avatar folder:
        avatardir_path = os.path.join(dir_path,"giftubing_avatars" )
        if not os.path.isdir(avatardir_path):
            print(f"Unable to find folder giftubing_avatars inside folder:")
            print(f"{os.path.basename(os.path.abspath(dir_path))}")
            print(f"Full path: \n{dir_path}")
            try:
                print(f"Contains: {os.listdir(dir_path)}")
            except FileNotFoundError:
                print(f"No file in {dir_path}")
            self.destroy()
            sys.exit()

        # avatar choice from user input:
        print("\n\n\n\nSelect which avatar to use from these sources:\n")
        all_avatars = os.listdir(avatardir_path)
        for i, avatar_option in enumerate(all_avatars):
            print(f"{i}: {avatar_option}")
        choice_is_valid = False
        if len(all_avatars) == 1:
            avatar_to_use = all_avatars[0]
            choice_is_valid = True
            print(f"Using single available avatar: {avatar_to_use}")
        while not choice_is_valid:
            choice = input("\nEnter avatar number:")
            try:
                avatar_choice = int(choice)
            except ValueError:
                print(f"Input must be an integer: {choice} is not valid")
            if avatar_choice < 0:
                print(f"{choice} must be greater than or equal to zero")
            elif avatar_choice < len(all_avatars):
                avatar_to_use = all_avatars[avatar_choice]
                choice_is_valid = True
            else:
                print(f"{avatar_choice} is not valid; {[x for x in range(len(all_avatars))]} are valid options")

        # path of avatar to use:
        self.avatar_path = os.path.join(avatardir_path, avatar_to_use)
        # get avatar metrics from empty file:
        filename = os.path.join(self.avatar_path, "empty.png")
        reader = QImageReader(filename)
        image = reader.read().copy() #.copy(*self.cropvals)
        if image.isNull():
            print(f"\nCould not find {filename} file, unable to start.")
            quit()

        print("setting window shape, size, position")
        ws, hs = QApplication.instance().primaryScreen().size().toTuple()
        w, h = image.width(), image.height()
        x = ws - w
        y = hs - h
        self.setGeometry(x, y, w, h) # xmin, ymin, xmax, ymax from upper left corner

        # Start:
        self.setCentralWidget(Giftube(self, avatar_path=self.avatar_path))

def giftubing_main(folder_path):
    app = QApplication([]) #! -> SHORTCUTS HERE??!
    window = WindowTube(folder_path)
    window.show()
    ret = app.exec()
    sys.exit(ret)

if __name__ == "__main__":
    giftubing_main()











