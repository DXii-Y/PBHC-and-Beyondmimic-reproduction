# run_demo.py
from gvhmr_demo_helper import demo_google_drive_video

if __name__ == "__main__":
    demo_google_drive_video(
        "https://drive.google.com/file/d/17c6GD0RMQkaWZRlLW5LCRPtOTOS_utnI/view?usp=drive_link",
        static_camera=True
    )
