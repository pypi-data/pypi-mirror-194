class Mouth():
    """
    Relates boolean mouth status values to strings.
    Status for parsing image in giftubing_sources folder from creator,
    name for generating and reading image file in launcher.
    """
    def __init__(self, is_mouth_open, is_mouth_wide):
        if not is_mouth_open:
            self.name = "_mouthclosed_"
            self.status = "closed"
        else:
            if is_mouth_wide:
                self.name = "_mouthwide_"
                self.status = "wide"
            else:
                self.name = "_mouthopen_"
                self.status = "open"

class Eyes():
    """
    Relates boolean eye status values to strings.
    left and right for parsing image in giftubing_sources folder from creator,
    name for generating and reading image file in launcher.
    """
    def __init__(self, is_left_eye_open, is_right_eye_open) -> None:
        if is_left_eye_open:
            self.name = "lefteyeopen_"
            self.left = "open"
        else:
            self.name = "lefteyeclosed_"
            self.left = "closed"
        if is_right_eye_open:
            self.name = self.name + "righteyeopen_"
            self.right = "open"
        else:
            self.name = self.name + "righteyeclosed_"
            self.right = "closed"

def get_filename(emotion, is_mouth_open, is_mouth_wide, is_left_eye_open, is_right_eye_open):
    mouth = Mouth(is_mouth_open, is_mouth_wide)
    eyes = Eyes(is_left_eye_open, is_right_eye_open)
    filename = emotion + mouth.name + eyes.name + ".png"
    return filename

if __name__=="__main__":
    print(get_filename("Neutral", True, False, True, True))