# Omnidirectional Sky Synthesis in StyleCity

![example](https://www.chenyingshu.com/stylecity3d/img/pipeline_sky.jpg)


# Quick Start
Our code is tested with Python 3.9, CUDA 11.3 and Pytorch 1.12.1 in GeForce RTX 3090.

## Installation
Install essential packages into an existing environment:
- diffusers
- transformers
- lpips

or run
```
pip install -r requirements.txt
```

## Sky Synthesis
You can also generate a sky panorama with text prompt and style image reference by enabling augment `--omni` and setting style reference by `--pivot`:
```
python sample_syncdiffusion.py \
--prompt "a sky panorama, a watercolor painting, well-designed digital art, featured on dribbble, medibang, warm saturated palette, style of olidon redon, the artist has used bright, airbrush render, beautiful painting of a tall, by I Ketut Soki" \
--negative "low quality" \
--H 1024 \
--W 2048 \
--seed 20230108 \
--steps 50 \
--sync_weight 20.0 \
--sync_decay_rate 0.95 \
--sync_freq 1 \
--sync_thres 10 \
--sd_version "2.0" \
--save_dir results \
--stride 16 \
--pivot 0026_watercolor.png \
--omni
```


## Tips
Please make sure the aspect ratio of panoramic image is height:width = 1:2. 
<br>
To align with city style, please use same pair of text prompt and style reference image. 

<details>
<summary> Known issues: </summary>

- The top and bottom areas may not generate sufficient content with blurry emptiness.
- The model tends to generate complex textures with textual sematics in each patch, so it may fail to generate tedius textures such as a color patch.

</details>


# Code Details
The implementation is based on [SyncDiffusion](https://github.com/KAIST-Visual-AI-Group/SyncDiffusion), the key updates lie in:
- Omnidirectional sampling (`syncdiffusion/utils.py`)
- LPIPS applied on style reference image (`SyncDiffusionOmni` in `syncdiffusion/syncdiffusion_model.py`)

For more details, please refer to our [Paper Sec.3.4](https://www.chenyingshu.com/stylecity3d/assets/StyleCity_paper.pdf) and our [Supplementary Sec.2.1](https://www.chenyingshu.com/stylecity3d/assets/StyleCity_supp_doc.pdf).

# Acknowledgement
The code is based on the [official implementation](https://github.com/KAIST-Visual-AI-Group/SyncDiffusion) of [SyncDiffusion](https://syncdiffusion.github.io/).
