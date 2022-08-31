import glob
from PIL import Image
def make_gif(frame_folder):
    frames = [Image.open(image).convert('P') for image in glob.glob(f"{frame_folder}/*.jpg")]
    frame_one = frames[0]
    frame_one.save("Background.gif", format="GIF", append_images=frames[1:],
               save_all=True, duration=200, loop=0)
    
if __name__ == "__main__":
    make_gif("./frames")