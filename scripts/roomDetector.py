import modules.scripts as scripts
import gradio as gr

from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state
import modules.shared as shared
from PIL import PngImagePlugin,Image
from io import BytesIO
import base64

def decode_base64_to_image(encoding):
    print('checkpoint A')
    if encoding.startswith("data:image/"):
        encoding = encoding.split(";")[1].split(",")[1]
    print('checkpoint B')

    image = Image.open(BytesIO(base64.b64decode(encoding)))
    print('checkpoint C')
    return image


class Script(scripts.Script):

    def title(self):
        return "Room Detector"
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        img = gr.Image(type='pil', shape=(200, 200))
        return [img]
    
    def before_process_batch(self, p, img, prompts, api_img='', **kwargs):
        print('Running Room Detector')
        
        pil_img = img
        if isinstance(img, str): 
            pil_img = decode_base64_to_image(img)
        img_rgb = pil_img.convert('RGB')
        print('checkpoint 1')
        
        processed = shared.interrogator.interrogate(img_rgb)
        
        print('checkpoint 2')
        
        for i in range(len(prompts)):
            prompts[i] = prompts[i].replace('CLIP_REPLACEME', processed)
            print('checkpoint 3')
            print(prompts[i])
            
        print('checkpoint 4')
