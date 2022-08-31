import glob
from PIL import Image
def change_gif(image_folder):
    im = Image.open(f"{image_folder}")
    for frame in range(0,im.n_frames):
        im.seek(frame)
        image = im.convert('RGBA')
        newImage = []
        for item in image.getdata():
            if item[:3] == (242,229,226):
                newImage.append((255,255,255,0))
            else:
                newImage.append(item)
        image.putdata(newImage)
        image.show()
    
    exit()
    frames = [Image.open(image).convert('P') for image in glob.glob(f"{frame_folder}/*.jpg")]
    frame_one = frames[0]
    frame_one.save("Background.gif", format="GIF", append_images=frames[1:],
               save_all=True, duration=250, loop=0)
    
if __name__ == "__main__":
    change_gif("./robot.gif")