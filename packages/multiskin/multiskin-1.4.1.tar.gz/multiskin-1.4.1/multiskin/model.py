# from enum import Enum
from time import strftime
from os import mkdir, path, getcwd, environ
from PIL import Image
from typing import List
from dataclasses import dataclass
from huggingface_hub import login
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from profanity_check import predict as profanity_predict
import traceback
from multiskin.clean.clean_skin import clean_skin

# class CreationType(Enum):
#     SKIN = 1
#     CAPE = 2

@dataclass
class InferConfig:
    prompts: List[str]
    num_inference_steps: int = 50
    width: int = 512
    height: int = 512
    creation_type: str = "SKIN"

def dummy(images, **kwargs):
            return images, False

class ProfanityError(Exception):
    pass

class Model:
    '''
    Python class that wraps the real model (weights, etc) hosted on HF under model_path.
    Uses HuggingFace libs to download the model, configure it for CUDA.
    infer() function
    '''
    model_path: str = None
    skin_output_folder: str = "generated_images"
    cape_output_folder = "generated_capes" # change cape.py if changing this

    def __init__(self, hf_token: str = "", mac: bool = False, model_path: str ="joshelgar/premesh-mc-skin-2k"):
        self.model_path = model_path
        login(environ.get("HUGGING_FACE_TOKEN", hf_token))
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_path)
        if mac:
            self.pipe = self.pipe.to("mps")
            self.pipe.enable_attention_slicing() # Recommended if your computer has < 64 GB of RAM
        else:
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
            self.pipe = self.pipe.to("cuda")
        
        self.pipe.safety_checker = dummy
        self.make_output_folders()
        if mac:
            self.warmup_pass()

    def warmup_pass(self):
        _ = self.pipe("nothing", num_inference_steps=1) # warmup to fix first-inference bug

    def make_output_folders(self):
        output_folders = [
            path.join(getcwd(), f'./{self.skin_output_folder}'),
            path.join(getcwd(), f'./{self.cape_output_folder}')
        ]
        print(f"Creating {len(output_folders)} output folders")
        for folder in output_folders:
            if not path.isdir(folder):
                mkdir(folder)

    def pipeline_args(self, infer_config: InferConfig):
        args = {
            "num_inference_steps": infer_config.num_inference_steps,
            "height": infer_config.height,
            "width": infer_config.width
        }
        return args

    def create_filename(self, prompt: str):
        # Clean and add current time
        print(f"Creating filename from prompt: {prompt}")
        keepcharacters = (' ', '_')
        shortened_prompt = prompt[:32]  # cap at about 32 chars + currtime string length
        cleaned_prompt = "".join(c for c in shortened_prompt if c.isalnum() or c in keepcharacters).rstrip()
        prompt_as_list = cleaned_prompt.split()
        currtime = strftime("%Y%m%d-%H%M%S")
        currtime_list = [currtime]
        currtime_list.extend(prompt_as_list)
        filename = "_".join(currtime_list)
        return filename


    def infer(self, infer_config: InferConfig) -> List[str]:
        '''
        Runs the model based on a supplied RunConfig (prompts, inf steps, resolution etc.)
        Returns -> List of filenames of resized images
        '''
        prompts = infer_config.prompts
        generated_filenames = []
        try:
            print(f"Inference config: {infer_config}")
            if any(profanity_predict(prompts)):
                raise ProfanityError
            for idx, prompt in enumerate(prompts):
                print(f"Generating prompt [{idx}/{len(prompts)}]: [{prompt}]...")
                tokened_prompt = f"{prompt} mc" if infer_config.creation_type is "SKIN" else f"{prompt}, sjh style"
                images: List[Image.Image] = self.pipe(tokened_prompt, **self.pipeline_args(infer_config=infer_config)).images
                filename = self.create_filename(prompt=prompt)
                print(f"Generated images: {images}")
                if infer_config.creation_type == "SKIN":
                    for image in images:
                        resized = image.resize((64, 64), resample=Image.Resampling.NEAREST)
                        cleaned = clean_skin(resized)
                        final_filename = f"./{self.skin_output_folder}/{filename}_resized.png"
                        cleaned.save(final_filename)
                        generated_filenames.append(final_filename)
                elif infer_config.creation_type == "CAPE":
                    print(f"Making a cape")
                    for image in images:
                        final_filename = f"./{self.cape_output_folder}/{filename}.png"
                        print(f"final_filename: {final_filename}")
                        image.save(final_filename)
                        generated_filenames.append(final_filename)
                        print(f"generated_filenames: {generated_filenames}")
                        
            return generated_filenames
        except Exception as e:
            print(traceback.format_exc())
            raise e