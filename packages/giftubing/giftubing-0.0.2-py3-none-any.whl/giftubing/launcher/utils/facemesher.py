from math import dist
import cv2
import numpy as np

lipsUpperOuter = [185, 40, 39, 37, 0, 267, 269, 270, 409] # 11 elements #! - [61, - 291], 
lipsUpperInner = [191, 80, 81, 82, 13, 312, 311, 310, 415] # 11 elements #! - [78, - 308], 
lipsLowerInner = [95, 88, 178, 87, 14, 317, 402, 318, 324] # 11 elements #! - [78, - 308], 
lipsLowerOuter = [146, 91, 181, 84, 17, 314, 405, 321, 375] # 10 elements #! - , 291], 

rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173] # 7 elements
rightEyeLower0 = [7, 163, 144, 145, 153, 154, 155]  # 7 elements #! - [33, - 133], 
rightEyeIris = [468, 469, 470, 471, 472] # 5 elements #! first is center

leftEyeUpper0 = [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
leftEyeIris = [473, 474, 475, 476, 477]  #! first is center

def coord2relative(coords, image_shape):
    """returns (x, y) tuple in pixels from percentage"""
    return (int(coords[0] * image_shape[1]), int(coords[1] * image_shape[0]))

class Facemesher():
    """
    
    """
    def __init__(self, mp_face_mesh):
        #init values
        CUTOFF_VALUE_FOR_GAUSSIAN_EYE_STATUS = 75
        CUTOFF_VALUE_FOR_MOUTH_OPEN = 4*1e-5
        CUTOFF_VALUE_FOR_MOUTH_WIDE_OPEN = 3*1e-4

        self.eye_cutoff = CUTOFF_VALUE_FOR_GAUSSIAN_EYE_STATUS
        self.mouth_open_cutoff = CUTOFF_VALUE_FOR_MOUTH_OPEN
        self.mouth_wide_open_cutoff = CUTOFF_VALUE_FOR_MOUTH_WIDE_OPEN
        if self.mouth_wide_open_cutoff < self.mouth_open_cutoff:
            raise ValueError(f"Invalid value: CUTOFF_VALUE_FOR_MOUTH_OPEN must be less than CUTOFF_VALUE_FOR_MOUTH_WIDE_OPEN")
        self.is_mouth_open = False
        self.is_mouth_wide = False
        self.is_right_eye_open = True
        self.is_left_eye_open = True
        self.mp_face_mesh = mp_face_mesh

    def get_eye_status(self, image: np.array, landmarks, which: str):
        """
        Input: image of face, landmarks from facemesh, and
        whether it's the left or right eye.
        """
        if which == "left":
            eye_landmarks = (441, 261)
        elif which == "right":
            eye_landmarks = (225, 232)
        else:
            raise ValueError("for get_eye_status, which must be 'left' or 'right'")        

        list_eye_landmarks = [coord2relative((land.x, land.y), image.shape) for land in (landmarks[x] for x in eye_landmarks)]

        # Crop the eye from image:
        eye_img = image[
            list_eye_landmarks[0][1]:list_eye_landmarks[1][1], # slicing ymin ymax
            list_eye_landmarks[0][0]:list_eye_landmarks[1][0], # slicing xmin xmax
            : # R G B
        ]

        if 0 not in eye_img.shape: # image validity check
            # Difference of gaussians to get shapes info:
            gray_l = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)
            low_sigma = cv2.GaussianBlur(gray_l,(3,3),0)
            high_sigma = cv2.GaussianBlur(gray_l,(5,5),0)
            gray_l = low_sigma - high_sigma

            # Open eye has more edges than closed:
            if np.mean(gray_l) < self.eye_cutoff:
                if which == "left":
                    self.is_left_eye_open = False
                else:
                    self.is_right_eye_open = False
            else:
                if which == "left":
                    self.is_left_eye_open = True
                else:
                    self.is_right_eye_open = True

    def run(self, image):
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
            # Get landmarks:
            face_results = face_mesh.process(image)
            if face_results.multi_face_landmarks:
                # only first face taken in account
                landmarks = face_results.multi_face_landmarks[0].landmark

                # Get mouth info:
                lip_up = landmarks[13] # middle of inner upper lip
                lip_down = landmarks[14] # middle of inner lower lip
                mouth_openness_val = dist((lip_up.x, lip_up.y), (lip_down.x, lip_down.y)) / image.shape[1] #, lip_up.z #, lip_down.z # Divide by height
                
                if mouth_openness_val > self.mouth_open_cutoff:
                    self.is_mouth_open = True
                    if mouth_openness_val > self.mouth_wide_open_cutoff:
                        self.is_mouth_wide = True
                    else:
                        self.is_mouth_wide = False
                else:
                    self.is_mouth_open = False

                # Get eyes info:
                self.get_eye_status(image, landmarks, "left")
                self.get_eye_status(image, landmarks, "right")


if __name__ == "__main__":
    from PIL import Image
    from torch import cuda
    from facenet_pytorch import MTCNN
    import mediapipe as mp

    from get_face import Face_boundary

    use_cuda = cuda.is_available()
    device = 'cuda' if use_cuda else 'cpu'
    if device == "cuda":
        print("Using GPU")
    else:
        print("Using CPU")

    TEST_IMAGE_PATH = ""
    PATH_TO_CREATED_RESULT_IMAGE = ""

    mtcnn = MTCNN(keep_all=False, post_process=False, min_face_size=40, device=device)
    image = np.array(Image.open(TEST_IMAGE_PATH))
    th = Face_boundary(mtcnn)
    th.run(image)
    im = th.face_image
    mp_face_mesh = mp.solutions.face_mesh
    f = Facemesher(im, mp_face_mesh)
    Image.fromarray(im).save(f"{PATH_TO_CREATED_RESULT_IMAGE}_.png")

