from cv2 import cvtColor, COLOR_BGR2RGB

class Face_boundary():
    """
    Uses mtcnn to detect face bounding box from frame,
    then outputs cropped result to self.face_image 
    or sets it to None.
    """
    def __init__(self, mtcnn):
        self.face_image = None
        self.left_border = None
        self.upper_border = None
        self.right_border = None
        self.lower_border = None
        self.mtcnn = mtcnn

    def run(self, image):
        frame = cvtColor(image, COLOR_BGR2RGB)
        bounding_boxes, probs = self.mtcnn.detect(frame, landmarks=False)
        if bounding_boxes is not None:
            bounding_boxes=bounding_boxes[probs>0.9]
            if len(bounding_boxes) > 0:
                # if any negative value, facemesh crashes so let's not:
                if any((x < 0 for x in bounding_boxes[0])):
                    self.face_image = None
                    return
                # Get bounding box values and crop image:
                self.left_border, self.upper_border, self.right_border, \
                    self.lower_border  = [int(x) for x in bounding_boxes[0]]
                self.face_image = image[self.upper_border:self.lower_border, 
                                        self.left_border:self.right_border,
                                        :]
            else:
                self.face_image = None
        else:
            self.face_image = None

if __name__ == "__main__":
    from PIL import Image
    from torch import cuda
    from facenet_pytorch import MTCNN
    import numpy as np

    PATH_TO_EXISTING_TEST_IMAGE = ""
    PATH_TO_CREATED_RESULT_IMAGE = ""

    use_cuda = cuda.is_available()
    device = 'cuda' if use_cuda else 'cpu'
    if device == "cuda":
        print("Using GPU")
    else:
        print("Using CPU")
    mtcnn = MTCNN(keep_all=False, post_process=False, min_face_size=40, device=device)
    image = np.array(Image.open(PATH_TO_EXISTING_TEST_IMAGE))
    th = Face_boundary(mtcnn).run(image)
    im = Image.fromarray(th.face_image)
    im.save(f"{PATH_TO_CREATED_RESULT_IMAGE}_.png")

