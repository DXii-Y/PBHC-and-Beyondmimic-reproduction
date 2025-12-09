# gvhmr_demo_helper.py
import os

def demo_google_drive_video(url: str, static_camera: bool):
    ''' URL should be like https://drive.google.com/file/d/xxxxxxxx/view?usp=drive_link '''
    proj_root = os.getcwd()
    print(f"[1/3] 📥 Downloading video...")
    gdid = url.split('/')[5]
    video_name = f'custom_{gdid}'
    download_url = f'https://drive.google.com/uc?id={gdid}&export=download&confirm=t'
    os.system(f"mkdir -p inputs/demo")
    os.system(f"gdown {download_url} -O inputs/demo/{video_name}.mp4")

    print(f"[2/3] 💃 Start running GVHMR...")
    flag = '-s' if static_camera else ''
    os.system(f"python {proj_root}/tools/demo/demo.py --video=inputs/demo/{video_name}.mp4 {flag}")

    print(f"[3/3] 📺 Displaying result...")
    output_path = f"outputs/demo/{video_name}/{video_name}_3_incam_global_horiz.mp4"
    print(f"✅ Done! Output video saved at:\n{output_path}")
