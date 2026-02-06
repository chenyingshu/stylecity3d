# StyleCity: Large-Scale 3D Urban Scenes Stylization (ECCV 2024)

<a href="https://www.chenyingshu.com/stylecity3d/"><img src="https://img.shields.io/badge/WEBSITE-Visit%20project%20page-blue?style=for-the-badge"></a>
<a href="https://arxiv.org/abs/2404.10681"><img src="https://img.shields.io/badge/arxiv-2404.10681-red?style=for-the-badge"></a>
<a href="https://github.com/chenyingshu/google_3dtile_collection"><img src="https://img.shields.io/badge/Data-Access Collecting Tool-green?style=for-the-badge"></a>

[Yingshu Chen](https://chenyingshu.github.io/),
[Huajian Huang](https://huajianup.github.io/)<sup>†</sup>,
[Tuan-Anh Vu](https://tuananh1007.github.io/),
[Ka-Chun Shum](https://scholar.google.com/citations?user=LAUhTjAAAAAJ&hl),
[Sai-Kit Yeung](https://www.saikit.org/) <br>
The Hong Kong University of Science and Technology <br>
<sup>†</sup>Corresponding author

> **Abstract:**
Creating large-scale virtual urban scenes with variant styles is inherently challenging. To facilitate prototypes of virtual production and bypass the need for complex materials and lighting setups, we introduce the first vision-and-text-driven texture stylization system for large-scale urban scenes, StyleCity. Taking an image and text as references, StyleCity stylizes a 3D textured mesh of a large-scale urban scene in a semantics-aware fashion and generates a harmonic omnidirectional sky background. To achieve that, we propose to stylize a neural texture field by transferring 2D vision-and-text priors to 3D globally and locally. During 3D stylization, we progressively scale the planned training views of the input 3D scene at different levels in order to preserve high-quality scene content. We then optimize the scene style globally by adapting the scale of the style image with the scale of the training views. Moreover, we enhance local semantics consistency by the semantics-aware style loss which is crucial for photo-realistic stylization. Besides texture stylization, we further adopt a generative diffusion model to synthesize a style-consistent omnidirectional sky image, which offers a more immersive atmosphere and assists the semantic stylization process. The stylized neural texture field can be baked into an arbitrary-resolution texture, enabling seamless integration into conventional rendering pipelines and significantly easing the virtual production prototyping process. Extensive experiments demonstrate our stylized scenes' superiority in qualitative and quantitative performance and user preferences.

## Updates:
- [ ] :hourglass_flowing_sand: Coming soon: StyleCity source code and samples
- [ ] :hourglass_flowing_sand: Coming soon: 2D-to-3D segmentation script
- [x] Omnidirectional sky synthesis source code
- [x] Segmentation model and 2D segmentation script: [city segmentation](https://github.com/chenyingshu/city_segmentation)
- [x] [Project page](https://www.chenyingshu.com/stylecity3d/) (Full materials: paper, poster, video, demo, etc.)
- [x] Data and data collector (Google Tiles API)

# More content is coming, stay tuned.

## Data
### Data Collector
We used Google 3D Tiles API to collect 3D city textured meshes.<br>
Please refer to [Google 3D Tiles Collection](https://github.com/chenyingshu/google_3dtile_collection) for details.

### Data Examples
Here are some data samples used in the paper: [[Dataset Link]](https://hkust-vgd.ust.hk/stylecity3d/datasets/)
```
datasets
├── model          # 3D model and 3D segmentation
├── segmentation   # 2D segmentation of style images
└── style          # style images
```

<details>

In folder `model`, each zip file contains a model data.<br>
Each sample contains (1) mesh and texture map, and (2) pre-processed 3D segmentation map (RGB & index).<br>
Data structure and description:<br>

```
model/SCENE_NAME.zip
├── SCENE_NAME.mtl          # dummpy material
├── SCENE_NAME.obj          # mesh, obj format
├── SCENE_NAME.png          # texture map
├── seg_texture.png         # segmentation RGB map (for visualization only)
├── seg_texture_index.png   # segmentation index map
├── cameras                 # planned pivot view camera pose
│   ├── R.npy               # camera rotations
│   └── T.npy               # camera translations
```


Folder `segmentation` contains pre-processed segmentation map (RGB & index) for some style images.<br>
Data structure and description:<br>
```
segmentation/style_segmentation
├── style1.png      # visualized segmentation
├── styleN.png      # visualized segmentation
├── index           # segmentation index map
│   ├── style1.png
│   └── styleN.png
```

</details>


## Get Started
### Requirements:
- Tested Python3.10+Pytorch1.13+Cuda11.6
  - used local cuda, conda cuda-toolkit encountered issue for tinycudann
- Tested Python3.9+Pytorch1.11/1.12+Cuda11.3
  - tested using conda cuda-toolkit

See more details in `requirements.txt`.

### Install Dependencies:

Here is an example of step-by-step environment setup based on conda. Suggest to install `pytorch3d` first then `tiny-cuda-nn`. Please install corresponding package versions based on your environment.

```
conda create stylecity_env python=3.9
conda activate stylecity_env

# install Pytorch 1.12.1 + CUDA 11.3
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch

# install Pytorch3D 0.7.5
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -c bottler nvidiacub
conda install pytorch3d=0.7.5 -c pytorch3d

pip install jupyter scikit-image matplotlib imageio plotly opencv-python chardet
pip install git+https://github.com/openai/CLIP.git

# install tiny-cuda-nn pytorch extension
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

pip install open3d # Optional, for camera visualization
```

### Checkpoints:
- Pretrained VGG model:<br>
Download pre-trained vgg normalized checkpoint `vgg_normalised.pth` [[here]](https://hkust-vgd.ust.hk/stylecity3d/checkpoints/vgg_normalised.pth) or [[here]](https://github.com/naoto0804/pytorch-AdaIN/releases/download/v0.0.0/vgg_normalised.pth) and put it under the folder `checkpoints/`.
- [Optional] Segmentation model: <br>
  - If you want to do 2D segmentation yourself, make sure [`city_segmentation`](https://github.com/chenyingshu/city_segmentation.git) repo is setup.
  - Download our pretrained segmentation [[here](https://hkust-vgd.ust.hk/stylecity3d/checkpoints/city_segmentation/model_final_v3.pth)] and put it under the folder `city_segmentation/checkpoint/`.

## Run Stylization

The whole process involves `preprocessing` and `3D style optimization`. After stylization, you can feel free to do `rendering`.

### Repo Setup
3D stylizatoin `StyleCity` repo and 2D segmentation `Mask2Former` repo:

```bash
# Main repository
git clone https://github.com/chenyingshu/stylecity3d.git

# Optional: set it up when you prepare your own data.
git clone https://github.com/chenyingshu/city_segmentation.git
cd city_segmentation
python setup.py . # please refer to `city_segmentation` for local installation
```

### Preprocessing
**Note:** If you use prepared [data sample](#data-examples), you can skip data preprocessing, and jump to Step [5. 3D Style Optimization](#5-3d-style-optimization).


#### **1. View planning and Rendering (coming soon)**

*View planning:* Plan training pivot cameras, taking as input a mesh and according information such as horizon level.


#### **2. 2D Segmentation**

Make sure [`city_segmentation`](https://github.com/chenyingshu/city_segmentation.git) repo is setup.

```bash
cd city_segmentation/demo
SCENE=SG_OrchardRd
RES=4096
python demo_split_merge.py \
--config-file ../configs/ade20k/semantic-segmentation/swin/anh_maskformer2_swin_large_IN21k_384_bs16_160k_res640.yaml \
--input ../../stylecity3d/outputs/planned_views/${SCENE}/images_${RES} \
--output ../../stylecity3d/dataset/segmentation/${SCENE} \
--opts MODEL.WEIGHTS ../checkpoint/model_final_v3.pth
```

If you need to segment your own style image, run the following script:
```bash
cd city_segmentation/demo
python demo.py \
--config-file ../configs/ade20k/semantic-segmentation/swin/anh_maskformer2_swin_large_IN21k_384_bs16_160k_res640.yaml \
--input style.jpg \
--output ../../stylecity3d/dataset/segmentation \
--opts MODEL.WEIGHTS ../checkpoint/model_final_v3.pth
```

#### **3. 3D Segmentation Mapping (coming soon)**


### Sky Synthesis

#### 4. Omnidirectional Sky Synthesis
**Note: proved by experiment, this step can be skipped and run 3D stylization directly with only perspective style reference image.**

You can read more details about sky synthesis in folder [`omni_sky/README.md`](./omni_sky/), here is an example of usage:

```bash
cd omni_sky
# recommend to create a new virtual environment
pip install -r requirements.txt
bash scripts.sh
```

### Stylization (coming soon)
#### **5. 3D Style Optimization (coming soon)**

This step includes neural texture intialization (non-stylization), and 3D stylization.

#### UV Distillation/Initialization

#### 3D Stylization

## Rendering (coming soon)
Optional neural rendering using neural texture, or conventional rendering using textured mesh.
### Export texture image

### Neural Rendering

### Conventional Rendering (Blender)
<!-- Import mesh.
Blender material setup. -->



## Citation
If you find our tool or work useful in your research, please consider citing:
```bibtex
@inproceedings{chen2024stylecity,
	title={StyleCity: Large-Scale 3D Urban Scenes Stylization},
	author={Chen, Yingshu and Huang, Huajian and Vu, Tuan-Anh and Shum, Ka Chun and Yeung, Sai-Kit},
	booktitle={Proceedings of the European Conference on Computer Vision},
	year={2024}
}
```

## Acknowledgements
We are very grateful for the source codes and outstanding contributions from [DPST](https://github.com/luanfujun/deep-photo-styletransfer), [SyncDiffusion](https://github.com/KAIST-Visual-AI-Group/SyncDiffusion), [Mask2Former](https://github.com/facebookresearch/Mask2Former), and [Pytorch3D](https://github.com/facebookresearch/pytorch3d).

