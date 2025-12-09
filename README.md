# PBHC-and-Beyondmimic-reproduction
This will permanently delete the DXii-Y/PBHC-and-Beyondmimic-reproduction repository, wiki, issues, comments, packages, secrets, workflow runs, and remove all collaborator associations.

## Environment
Ubuntu 22.04
RTX 3090

## 🚀Train a walking policy for G1
### Pipeline
walking skeleton extracted-> Retarget->Train Policy
And I use two methods for training PBHC and Beyondmimic

## 🤖PBHC
### 📦GVHMR:Skeleton extracted
Set up enviroment and follow [GVHMR](https://github.com/zju3dv/GVHMR) instructions setp by step 
#### 1. Update walk videos to GoogleDrive
#### 2. Extract your own videos
```python
python GVHMR/setup.py
```
### 📦Retarget
We use PBHC to retarget and train policy
#### 1. Install PBHC and Isaacgym
[PBHC](https://github.com/TeleHuman/PBHC/blob/main/INSTALL.md)
#### 2. PBHC Retarget
##### 🎮Data addressing
We use GVHMR to extract motions from videos. Replace GVHMR's demo.py with our demo.py to generate an SMPL-format .npz file in GVHMR's output directory.
##### 🎮Retarget
First bulid a folder and put .npz file under it
```python
motion_data/
├── dataset/
└── smpl.npz
```
And run:
```python
python phc_retarget/fit_smpl_motion.py robot=unitree_g1_29dof_anneal_23dof +motion=/home/ril/dxy/PBHC/smpl_retarget/motion_data +fit_all=True
```

#### 🧠3. Train policy for G1
##### Train
```python
python humanoidverse/train_agent.py +simulator=isaacgym +exp=motion_tracking +terrain=terrain_locomotion_plane project_name=MotionTracking num_envs=128 +obs=motion_tracking/main +robot=g1/g1_23dof_lock_wrist +domain_rand=main +rewards=motion_tracking/main experiment_name=debug robot.motion.motion_file="/home/ril/dxy/PBHC/smpl_retarget/retargeted_motion_data/phc/g1/0-smpl_origin.pkl" seed=1 +device=cuda:0
```
##### Evaluation
```python
python humanoidverse/eval_agent.py +device=cuda:0 +env.config.enforce_randomize_motion_start_eval=False +checkpoint=/home/ril/dxy/PBHC/logs/MotionTracking/20251125_010911-debug-motion_tracking-g1_23dof_lock_wrist/model_0.pt
```
## 🤖Beyondmimic
### 📦GVHMR:Skeleton extracted
Refer to PBHC, they are same
### 📦Retarget--GMR
Beyondmimic does not provide a redirect module, so used GMR
#### Install
install [GMR and IsaacLab](https://github.com/YanjieZe/GMR/blob/master/README.md)
#### Retaget
I modified output format form ```.pkl``` to ```.csv``` in ```gvhmr_to_robot.py```. For retarget, run:
```python
python scripts/csv_to_npz.py --input_file /home/ril/dxy/GMR/RetargetData/gvhmr/csv/my_test.csv --input_fps 30 --output_name my_test --headless
```
##### Evaluation
```python
python scripts/replay_npz.py --motion_file ./local_registry/motions/my_test.npz
```
#### 🧠Train Policy for G1
I modified code to train and visualize locally without use WandB
##### Trian
```python
python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 --motion_file ./local_registry/motions/my_test.npz --headless --logger tensorboard --run_name my_local_runb --max_iterations 8000 
```
##### Evaluation
```python
python scripts/rsl_rl/play.py \
    --task=Tracking-Flat-G1-v0 \
    --num_envs=1 \
    --motion_file=/home/ril/dxy/whole_body_tracking/local_registry/motions/my_test.npz \
    --checkpoint=/home/ril/dxy/whole_body_tracking/logs/rsl_rl/g1_flat/2025-11-26_12-17-19_my_local_runb/model_7999.pt
```
