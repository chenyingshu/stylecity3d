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
- [x] Segmentation model and 2D segmentation script: [city segmentation](https://github.com/chenyingshu/city_segmentation)
- [ ] :hourglass_flowing_sand: Coming soon: 2D-to-3D segmentation script
- [ ] :hourglass_flowing_sand: Coming soon: Omnidirectional sky synthesis source code
- [x] [Project page](https://www.chenyingshu.com/stylecity3d/) (Full materials: paper, poster, video, demo, etc.)
- [x] Data collector (Google Tiles API)

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

