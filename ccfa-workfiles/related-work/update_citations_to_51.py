from pathlib import Path
import re

root = Path(r"D:\论文\9.27论文")
main_bib = root / "author-kit-main" / "main.bib"
zh_bib = root / "中文论文" / "references.bib"
refs_tex = root / "author-kit-main" / "references.tex"
zh_refs = root / "中文论文" / "参考文献.md"

bib_entries = r"""

% ===== Additional references R29--R51 (verified 2026-10-20) =====
@InProceedings{R29,
  author    = {Wang, Feng and Mei, Jieru and Yuille, Alan},
  title     = {{SCLIP}: Rethinking Self-Attention for Dense Vision-Language Inference},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2024},
  pages     = {315--332},
  doi       = {10.1007/978-3-031-72664-4_18}
}

@InProceedings{R30,
  author    = {Lan, Mengcheng and Chen, Chaofeng and Ke, Yiping and Wang, Xinjiang and Feng, Litong and Zhang, Wayne},
  title     = {{ClearCLIP}: Decomposing {CLIP} Representations for Dense Vision-Language Inference},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2024},
  pages     = {143--160},
  doi       = {10.1007/978-3-031-72970-6_9}
}

@InProceedings{R31,
  author    = {Lan, Mengcheng and Chen, Chaofeng and Ke, Yiping and Wang, Xinjiang and Feng, Litong and Zhang, Wayne},
  title     = {{ProxyCLIP}: Proxy Attention Improves {CLIP} for Open-Vocabulary Segmentation},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2024},
  pages     = {70--88},
  doi       = {10.1007/978-3-031-73113-6_5}
}

@InProceedings{R32,
  author    = {Zhu, Hao and Jin, Shuo and Liao, Wenbin and Xiao, Jiayu and Zhu, Yan and Yu, Siyue and Dai, Feng},
  title     = {{VIP}: Visual-guided Prompt Evolution for Efficient Dense Vision-Language Inference},
  booktitle = {Proceedings of the International Conference on Machine Learning (ICML)},
  year      = {2026},
  url       = {https://arxiv.org/abs/2605.12325}
}

@Article{R33,
  author  = {Wang, Shanwen and Sun, Xin and Han, Jungong and Zhu, Xiao Xiang},
  title   = {{RSCLIP} for Training-Free Open-Vocabulary Remote Sensing Image Semantic Segmentation},
  journal = {IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing},
  year    = {2026},
  volume  = {19},
  pages   = {15626--15639},
  doi     = {10.1109/JSTARS.2026.3688939}
}

@InProceedings{R34,
  author    = {Zhang, Dengke and Liu, Fagui and Tang, Quan},
  title     = {{CorrCLIP}: Reconstructing Patch Correlations in {CLIP} for Open-Vocabulary Semantic Segmentation},
  booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  year      = {2025},
  pages     = {24677--24687},
  doi       = {10.1109/ICCV51701.2025.02288}
}

@Article{R35,
  author  = {Tien, Tran Dinh and Shen, Zhiqiang},
  title   = {{ActiveSAM}: Fast and Accurate Open-Vocabulary Semantic Segmentation with Frozen {SAM} 3},
  journal = {arXiv preprint arXiv:2606.16996},
  year    = {2026},
  url     = {https://arxiv.org/abs/2606.16996}
}

@InProceedings{R36,
  author    = {Wang, Junjue and Zheng, Zhuo and Ma, Ailong and Lu, Xiaoyan and Zhong, Yanfei},
  title     = {{LoveDA}: A Remote Sensing Land-Cover Dataset for Domain Adaptive Semantic Segmentation},
  booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks},
  year      = {2021},
  volume    = {1},
  url       = {https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/4e732ced3463d06de0ca9a15b6153677-Paper-round2.pdf}
}

@InProceedings{R37,
  author    = {Zamir, Syed Waqas and Arora, Aditya and Gupta, Akshita and Khan, Salman and Sun, Guolei and Khan, Fahad Shahbaz and Zhu, Fan and Shao, Ling and Xia, Gui-Song and Bai, Xiang},
  title     = {{iSAID}: A Large-Scale Dataset for Instance Segmentation in Aerial Images},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)},
  year      = {2019},
  url       = {https://arxiv.org/abs/1905.12886}
}

@InProceedings{R38,
  author    = {Xia, Junshi and Yokoya, Naoto and Adriano, Bruno and Broni-Bediako, Clifford},
  title     = {{OpenEarthMap}: A Benchmark Dataset for Global High-Resolution Land Cover Mapping},
  booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
  year      = {2023},
  pages     = {6243--6253},
  doi       = {10.1109/WACV56688.2023.00619}
}

@Article{R39,
  author  = {Lyu, Ye and Vosselman, George and Xia, Gui-Song and Yilmaz, Alper and Yang, Michael Ying},
  title   = {{UAVid}: A Semantic Segmentation Dataset for {UAV} Imagery},
  journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
  year    = {2020},
  volume  = {165},
  pages   = {108--119},
  doi     = {10.1016/j.isprsjprs.2020.05.009}
}

@InProceedings{R40,
  author    = {Chen, Yu and Wang, Yao and Lu, Peng and Chen, Yisong and Wang, Guoping},
  title     = {Large-Scale Structure from Motion with Semantic Constraints of Aerial Images},
  booktitle = {Pattern Recognition and Computer Vision (PRCV)},
  year      = {2018},
  pages     = {347--359},
  doi       = {10.1007/978-3-030-03398-9_30}
}

@Article{R41,
  author  = {Cai, Wenxiao and Jin, Ke and Hou, Jinyan and Guo, Cong and Wu, Letian and Yang, Wankou},
  title   = {{VDD}: Varied Drone Dataset for Semantic Segmentation},
  journal = {Journal of Visual Communication and Image Representation},
  year    = {2025},
  volume  = {109},
  pages   = {104429},
  doi     = {10.1016/j.jvcir.2025.104429}
}

@Misc{R42,
  title        = {{ISPRS} 2D Semantic Labeling Benchmark: Potsdam and Vaihingen},
  howpublished = {International Society for Photogrammetry and Remote Sensing},
  url          = {https://www.isprs.org/education/benchmarks/UrbanSemLab/}
}

@InProceedings{R43,
  author    = {Cordts, Marius and Omran, Mohamed and Ramos, Sebastian and Rehfeld, Timo and Enzweiler, Markus and Benenson, Rodrigo and Franke, Uwe and Roth, Stefan and Schiele, Bernt},
  title     = {The {Cityscapes} Dataset for Semantic Urban Scene Understanding},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016},
  pages     = {3213--3223},
  doi       = {10.1109/CVPR.2016.350}
}

@Article{R44,
  author  = {Everingham, Mark and Van Gool, Luc and Williams, Christopher K. I. and Winn, John and Zisserman, Andrew},
  title   = {The {PASCAL} Visual Object Classes ({VOC}) Challenge},
  journal = {International Journal of Computer Vision},
  year    = {2010},
  volume  = {88},
  number  = {2},
  pages   = {303--338},
  doi     = {10.1007/s11263-009-0275-4}
}

@InProceedings{R45,
  author    = {Xu, Jiarui and De Mello, Shalini and Liu, Sifei and Byeon, Wonmin and Breuel, Thomas and Kautz, Jan and Wang, Xiaolong},
  title     = {{GroupViT}: Semantic Segmentation Emerges from Text Supervision},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2022},
  pages     = {18113--18123},
  doi       = {10.1109/CVPR52688.2022.01760}
}

@InProceedings{R46,
  author    = {Liang, Feng and Wu, Bichen and Dai, Xiaoliang and Li, Kunpeng and Zhao, Yinan and Zhang, Hang and Zhang, Peizhao and Vajda, Peter and Marculescu, Diana},
  title     = {Open-Vocabulary Semantic Segmentation with Mask-Adapted {CLIP}},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2023},
  pages     = {7061--7070},
  doi       = {10.1109/CVPR52729.2023.00682}
}

@InProceedings{R47,
  author    = {Yang, Yuhang and Deng, Jinhong and Li, Wen and Duan, Lixin},
  title     = {{ResCLIP}: Residual Attention for Training-Free Dense Vision-Language Inference},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2025},
  pages     = {29968--29978},
  doi       = {10.1109/CVPR52734.2025.02789}
}

@InProceedings{R48,
  author    = {Cho, Seokju and Shin, Heeseong and Hong, Sunghwan and Arnab, Anurag and Seo, Paul Hongsuck and Kim, Seungryong},
  title     = {{CAT-Seg}: Cost Aggregation for Open-Vocabulary Semantic Segmentation},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2024},
  pages     = {4113--4123},
  doi       = {10.1109/CVPR52733.2024.00394}
}

@InProceedings{R49,
  author    = {Xie, Bin and Cao, Jiale and Xie, Jin and Khan, Fahad Shahbaz and Pang, Yanwei},
  title     = {{SED}: A Simple Encoder-Decoder for Open-Vocabulary Semantic Segmentation},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2024},
  pages     = {3426--3436},
  doi       = {10.1109/CVPR52733.2024.00329}
}

@InProceedings{R50,
  author    = {Hu, Yu and Gu, Jianyang and Liu, Hao and Cao, Yue and Hamari, Jozsef and Liu, Zheng and Zardadi, Mohsen},
  title     = {{AVION}: Aerial Vision-Language Instruction from Offline Teacher to Prompt-Tuned Network},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2026},
  url       = {https://openaccess.thecvf.com/content/CVPR2026/html/Hu_AVION_Aerial_Vision-Language_Instruction_from_Offline_Teacher_to_Prompt-Tuned_Network_CVPR_2026_paper.html}
}

@InProceedings{R51,
  author    = {Zhang, Bingfeng and Yu, Siyue and Li, Hui and Lin, Jiahua and Wang, Wenwu and Xiao, Jimin},
  title     = {The Power of Prior: Training-Free Open-Vocabulary Semantic Segmentation with {LLaVA}},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2026},
  url       = {https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_The_Power_of_Prior_Training-Free_Open-Vocabulary_Semantic_Segmentation_with_LLaVA_CVPR_2026_paper.html}
}
"""

tex_entries = r"""
\bibitem{R29}
Feng Wang, Jieru Mei, and Alan Yuille.
\newblock {SCLIP}: Rethinking self-attention for dense vision-language inference.
\newblock In \emph{European Conference on Computer Vision (ECCV)}, pages
  315--332, 2024.
\newblock \doi{10.1007/978-3-031-72664-4_18}

\bibitem{R30}
Mengcheng Lan, Chaofeng Chen, Yiping Ke, Xinjiang Wang, Litong Feng, and
  Wayne Zhang.
\newblock {ClearCLIP}: Decomposing {CLIP} representations for dense
  vision-language inference.
\newblock In \emph{European Conference on Computer Vision (ECCV)}, pages
  143--160, 2024.
\newblock \doi{10.1007/978-3-031-72970-6_9}

\bibitem{R31}
Mengcheng Lan, Chaofeng Chen, Yiping Ke, Xinjiang Wang, Litong Feng, and
  Wayne Zhang.
\newblock {ProxyCLIP}: Proxy attention improves {CLIP} for open-vocabulary
  segmentation.
\newblock In \emph{European Conference on Computer Vision (ECCV)}, pages
  70--88, 2024.
\newblock \doi{10.1007/978-3-031-73113-6_5}

\bibitem{R32}
Hao Zhu, Shuo Jin, Wenbin Liao, Jiayu Xiao, Yan Zhu, Siyue Yu, and Feng Dai.
\newblock {VIP}: Visual-guided prompt evolution for efficient dense
  vision-language inference.
\newblock In \emph{Proceedings of the International Conference on Machine
  Learning (ICML)}, 2026.

\bibitem{R33}
Shanwen Wang, Xin Sun, Jungong Han, and Xiao~Xiang Zhu.
\newblock {RSCLIP} for training-free open-vocabulary remote sensing image
  semantic segmentation.
\newblock \emph{IEEE Journal of Selected Topics in Applied Earth Observations
  and Remote Sensing}, 19:15626--15639, 2026.
\newblock \doi{10.1109/JSTARS.2026.3688939}

\bibitem{R34}
Dengke Zhang, Fagui Liu, and Quan Tang.
\newblock {CorrCLIP}: Reconstructing patch correlations in {CLIP} for
  open-vocabulary semantic segmentation.
\newblock In \emph{Proceedings of the IEEE/CVF International Conference on
  Computer Vision (ICCV)}, pages 24677--24687, 2025.
\newblock \doi{10.1109/ICCV51701.2025.02288}

\bibitem{R35}
Tran~Dinh Tien and Zhiqiang Shen.
\newblock {ActiveSAM}: Fast and accurate open-vocabulary semantic
  segmentation with frozen {SAM}~3.
\newblock \emph{arXiv preprint arXiv:2606.16996}, 2026.

\bibitem{R36}
Junjue Wang, Zhuo Zheng, Ailong Ma, Xiaoyan Lu, and Yanfei Zhong.
\newblock {LoveDA}: A remote sensing land-cover dataset for domain adaptive
  semantic segmentation.
\newblock In \emph{Proceedings of the Neural Information Processing Systems
  Track on Datasets and Benchmarks}, volume~1, 2021.

\bibitem{R37}
Syed~Waqas Zamir, Aditya Arora, Akshita Gupta, Salman Khan, Guolei Sun,
  Fahad~Shahbaz Khan, Fan Zhu, Ling Shao, Gui-Song Xia, and Xiang Bai.
\newblock {iSAID}: A large-scale dataset for instance segmentation in aerial
  images.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition Workshops (CVPRW)}, 2019.

\bibitem{R38}
Junshi Xia, Naoto Yokoya, Bruno Adriano, and Clifford Broni-Bediako.
\newblock {OpenEarthMap}: A benchmark dataset for global high-resolution land
  cover mapping.
\newblock In \emph{Proceedings of the IEEE/CVF Winter Conference on
  Applications of Computer Vision (WACV)}, pages 6243--6253, 2023.
\newblock \doi{10.1109/WACV56688.2023.00619}

\bibitem{R39}
Ye Lyu, George Vosselman, Gui-Song Xia, Alper Yilmaz, and Michael~Ying Yang.
\newblock {UAVid}: A semantic segmentation dataset for {UAV} imagery.
\newblock \emph{ISPRS Journal of Photogrammetry and Remote Sensing},
  165:108--119, 2020.
\newblock \doi{10.1016/j.isprsjprs.2020.05.009}

\bibitem{R40}
Yu Chen, Yao Wang, Peng Lu, Yisong Chen, and Guoping Wang.
\newblock Large-scale structure from motion with semantic constraints of aerial
  images.
\newblock In \emph{Pattern Recognition and Computer Vision (PRCV)}, pages
  347--359, 2018.
\newblock \doi{10.1007/978-3-030-03398-9_30}

\bibitem{R41}
Wenxiao Cai, Ke Jin, Jinyan Hou, Cong Guo, Letian Wu, and Wankou Yang.
\newblock {VDD}: Varied drone dataset for semantic segmentation.
\newblock \emph{Journal of Visual Communication and Image Representation},
  109:104429, 2025.
\newblock \doi{10.1016/j.jvcir.2025.104429}

\bibitem{R42}
\newblock {ISPRS} 2D semantic labeling benchmark: Potsdam and Vaihingen.
\newblock International Society for Photogrammetry and Remote Sensing.
\newblock \url{https://www.isprs.org/education/benchmarks/UrbanSemLab/}

\bibitem{R43}
Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus
  Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele.
\newblock The {Cityscapes} dataset for semantic urban scene understanding.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 3213--3223, 2016.
\newblock \doi{10.1109/CVPR.2016.350}

\bibitem{R44}
Mark Everingham, Luc Van~Gool, Christopher~K.~I. Williams, John Winn, and
  Andrew Zisserman.
\newblock The {PASCAL} visual object classes ({VOC}) challenge.
\newblock \emph{International Journal of Computer Vision}, 88(2):303--338,
  2010.
\newblock \doi{10.1007/s11263-009-0275-4}

\bibitem{R45}
Jiarui Xu, Shalini De~Mello, Sifei Liu, Wonmin Byeon, Thomas Breuel, Jan
  Kautz, and Xiaolong Wang.
\newblock {GroupViT}: Semantic segmentation emerges from text supervision.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 18113--18123, 2022.
\newblock \doi{10.1109/CVPR52688.2022.01760}

\bibitem{R46}
Feng Liang, Bichen Wu, Xiaoliang Dai, Kunpeng Li, Yinan Zhao, Hang Zhang,
  Peizhao Zhang, Peter Vajda, and Diana Marculescu.
\newblock Open-vocabulary semantic segmentation with mask-adapted {CLIP}.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 7061--7070, 2023.
\newblock \doi{10.1109/CVPR52729.2023.00682}

\bibitem{R47}
Yuhang Yang, Jinhong Deng, Wen Li, and Lixin Duan.
\newblock {ResCLIP}: Residual attention for training-free dense
  vision-language inference.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 29968--29978, 2025.
\newblock \doi{10.1109/CVPR52734.2025.02789}

\bibitem{R48}
Seokju Cho, Heeseong Shin, Sunghwan Hong, Anurag Arnab, Paul~Hongsuck Seo,
  and Seungryong Kim.
\newblock {CAT-Seg}: Cost aggregation for open-vocabulary semantic
  segmentation.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 4113--4123, 2024.
\newblock \doi{10.1109/CVPR52733.2024.00394}

\bibitem{R49}
Bin Xie, Jiale Cao, Jin Xie, Fahad~Shahbaz Khan, and Yanwei Pang.
\newblock {SED}: A simple encoder-decoder for open-vocabulary semantic
  segmentation.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, pages 3426--3436, 2024.
\newblock \doi{10.1109/CVPR52733.2024.00329}

\bibitem{R50}
Yu Hu, Jianyang Gu, Hao Liu, Yue Cao, Jozsef Hamari, Zheng Liu, and Mohsen
  Zardadi.
\newblock {AVION}: Aerial vision-language instruction from offline teacher to
  prompt-tuned network.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, 2026.

\bibitem{R51}
Bingfeng Zhang, Siyue Yu, Hui Li, Jiahua Lin, Wenwu Wang, and Jimin Xiao.
\newblock The power of prior: Training-free open-vocabulary semantic
  segmentation with {LLaVA}.
\newblock In \emph{Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition (CVPR)}, 2026.
"""

md_entries = r"""

<a id="r29"></a>

[29] Wang, Feng and Mei, Jieru and Yuille, Alan. [SCLIP: Rethinking Self-Attention for Dense Vision-Language Inference](https://doi.org/10.1007/978-3-031-72664-4_18). European Conference on Computer Vision (ECCV), 2024.

<a id="r30"></a>

[30] Lan, Mengcheng and Chen, Chaofeng and Ke, Yiping and Wang, Xinjiang and Feng, Litong and Zhang, Wayne. [ClearCLIP: Decomposing CLIP Representations for Dense Vision-Language Inference](https://doi.org/10.1007/978-3-031-72970-6_9). European Conference on Computer Vision (ECCV), 2024.

<a id="r31"></a>

[31] Lan, Mengcheng and Chen, Chaofeng and Ke, Yiping and Wang, Xinjiang and Feng, Litong and Zhang, Wayne. [ProxyCLIP: Proxy Attention Improves CLIP for Open-Vocabulary Segmentation](https://doi.org/10.1007/978-3-031-73113-6_5). European Conference on Computer Vision (ECCV), 2024.

<a id="r32"></a>

[32] Zhu, Hao and Jin, Shuo and Liao, Wenbin and Xiao, Jiayu and Zhu, Yan and Yu, Siyue and Dai, Feng. [VIP: Visual-guided Prompt Evolution for Efficient Dense Vision-Language Inference](https://arxiv.org/abs/2605.12325). International Conference on Machine Learning (ICML), 2026.

<a id="r33"></a>

[33] Wang, Shanwen and Sun, Xin and Han, Jungong and Zhu, Xiao Xiang. [RSCLIP for Training-Free Open-Vocabulary Remote Sensing Image Semantic Segmentation](https://doi.org/10.1109/JSTARS.2026.3688939). IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 19:15626-15639, 2026.

<a id="r34"></a>

[34] Zhang, Dengke and Liu, Fagui and Tang, Quan. [CorrCLIP: Reconstructing Patch Correlations in CLIP for Open-Vocabulary Semantic Segmentation](https://doi.org/10.1109/ICCV51701.2025.02288). IEEE/CVF International Conference on Computer Vision (ICCV), 2025.

<a id="r35"></a>

[35] Tien, Tran Dinh and Shen, Zhiqiang. [ActiveSAM: Fast and Accurate Open-Vocabulary Semantic Segmentation with Frozen SAM 3](https://arxiv.org/abs/2606.16996). arXiv preprint arXiv:2606.16996, 2026.

<a id="r36"></a>

[36] Wang, Junjue and Zheng, Zhuo and Ma, Ailong and Lu, Xiaoyan and Zhong, Yanfei. [LoveDA: A Remote Sensing Land-Cover Dataset for Domain Adaptive Semantic Segmentation](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/4e732ced3463d06de0ca9a15b6153677-Paper-round2.pdf). NeurIPS Datasets and Benchmarks, 2021.

<a id="r37"></a>

[37] Zamir, Syed Waqas and Arora, Aditya and Gupta, Akshita and Khan, Salman and Sun, Guolei and Khan, Fahad Shahbaz and Zhu, Fan and Shao, Ling and Xia, Gui-Song and Bai, Xiang. [iSAID: A Large-Scale Dataset for Instance Segmentation in Aerial Images](https://arxiv.org/abs/1905.12886). IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2019.

<a id="r38"></a>

[38] Xia, Junshi and Yokoya, Naoto and Adriano, Bruno and Broni-Bediako, Clifford. [OpenEarthMap: A Benchmark Dataset for Global High-Resolution Land Cover Mapping](https://doi.org/10.1109/WACV56688.2023.00619). IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2023.

<a id="r39"></a>

[39] Lyu, Ye and Vosselman, George and Xia, Gui-Song and Yilmaz, Alper and Yang, Michael Ying. [UAVid: A Semantic Segmentation Dataset for UAV Imagery](https://doi.org/10.1016/j.isprsjprs.2020.05.009). ISPRS Journal of Photogrammetry and Remote Sensing, 2020.

<a id="r40"></a>

[40] Chen, Yu and Wang, Yao and Lu, Peng and Chen, Yisong and Wang, Guoping. [Large-Scale Structure from Motion with Semantic Constraints of Aerial Images](https://doi.org/10.1007/978-3-030-03398-9_30). Pattern Recognition and Computer Vision (PRCV), 2018.

<a id="r41"></a>

[41] Cai, Wenxiao and Jin, Ke and Hou, Jinyan and Guo, Cong and Wu, Letian and Yang, Wankou. [VDD: Varied Drone Dataset for Semantic Segmentation](https://doi.org/10.1016/j.jvcir.2025.104429). Journal of Visual Communication and Image Representation, 2025.

<a id="r42"></a>

[42] [ISPRS 2D Semantic Labeling Benchmark: Potsdam and Vaihingen](https://www.isprs.org/education/benchmarks/UrbanSemLab/). International Society for Photogrammetry and Remote Sensing.

<a id="r43"></a>

[43] Cordts, Marius and Omran, Mohamed and Ramos, Sebastian and Rehfeld, Timo and Enzweiler, Markus and Benenson, Rodrigo and Franke, Uwe and Roth, Stefan and Schiele, Bernt. [The Cityscapes Dataset for Semantic Urban Scene Understanding](https://doi.org/10.1109/CVPR.2016.350). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2016.

<a id="r44"></a>

[44] Everingham, Mark and Van Gool, Luc and Williams, Christopher K. I. and Winn, John and Zisserman, Andrew. [The PASCAL Visual Object Classes (VOC) Challenge](https://doi.org/10.1007/s11263-009-0275-4). International Journal of Computer Vision, 88(2):303-338, 2010.

<a id="r45"></a>

[45] Xu, Jiarui and De Mello, Shalini and Liu, Sifei and Byeon, Wonmin and Breuel, Thomas and Kautz, Jan and Wang, Xiaolong. [GroupViT: Semantic Segmentation Emerges from Text Supervision](https://doi.org/10.1109/CVPR52688.2022.01760). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022.

<a id="r46"></a>

[46] Liang, Feng and Wu, Bichen and Dai, Xiaoliang and Li, Kunpeng and Zhao, Yinan and Zhang, Hang and Zhang, Peizhao and Vajda, Peter and Marculescu, Diana. [Open-Vocabulary Semantic Segmentation with Mask-Adapted CLIP](https://doi.org/10.1109/CVPR52729.2023.00682). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023.

<a id="r47"></a>

[47] Yang, Yuhang and Deng, Jinhong and Li, Wen and Duan, Lixin. [ResCLIP: Residual Attention for Training-Free Dense Vision-Language Inference](https://doi.org/10.1109/CVPR52734.2025.02789). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025.

<a id="r48"></a>

[48] Cho, Seokju and Shin, Heeseong and Hong, Sunghwan and Arnab, Anurag and Seo, Paul Hongsuck and Kim, Seungryong. [CAT-Seg: Cost Aggregation for Open-Vocabulary Semantic Segmentation](https://doi.org/10.1109/CVPR52733.2024.00394). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024.

<a id="r49"></a>

[49] Xie, Bin and Cao, Jiale and Xie, Jin and Khan, Fahad Shahbaz and Pang, Yanwei. [SED: A Simple Encoder-Decoder for Open-Vocabulary Semantic Segmentation](https://doi.org/10.1109/CVPR52733.2024.00329). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024.

<a id="r50"></a>

[50] Hu, Yu and Gu, Jianyang and Liu, Hao and Cao, Yue and Hamari, Jozsef and Liu, Zheng and Zardadi, Mohsen. [AVION: Aerial Vision-Language Instruction from Offline Teacher to Prompt-Tuned Network](https://openaccess.thecvf.com/content/CVPR2026/html/Hu_AVION_Aerial_Vision-Language_Instruction_from_Offline_Teacher_to_Prompt-Tuned_Network_CVPR_2026_paper.html). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2026.

<a id="r51"></a>

[51] Zhang, Bingfeng and Yu, Siyue and Li, Hui and Lin, Jiahua and Wang, Wenwu and Xiao, Jimin. [The Power of Prior: Training-Free Open-Vocabulary Semantic Segmentation with LLaVA](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_The_Power_of_Prior_Training-Free_Open-Vocabulary_Semantic_Segmentation_with_LLaVA_CVPR_2026_paper.html). IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2026.
"""

text = main_bib.read_text(encoding="utf-8")
if "@InProceedings{R29," not in text and "@Article{R33," not in text:
    text = text.rstrip() + bib_entries
main_bib.write_text(text.rstrip() + "\n", encoding="utf-8")
zh_bib.write_text(text.rstrip() + "\n", encoding="utf-8")

tex = refs_tex.read_text(encoding="utf-8")
tex = re.sub(r"\\begin\{thebibliography\}\{[^}]+\}", r"\\begin{thebibliography}{51}", tex, count=1)
if r"\bibitem{R29}" not in tex:
    idx = tex.rfind(r"\end{thebibliography}")
    if idx < 0:
        raise RuntimeError("references.tex lacks end{thebibliography}")
    tex = tex[:idx].rstrip() + "\n" + tex_entries + "\n" + tex[idx:]
refs_tex.write_text(tex, encoding="utf-8")

md = zh_refs.read_text(encoding="utf-8")
md = md.replace("BibTeX key 为 R01–R23", "BibTeX key 为 R01–R51")
md = md.replace("BibTeX key 为 R01–R28", "BibTeX key 为 R01–R51")
if '<a id="r29"></a>' not in md:
    md = md.rstrip() + md_entries
zh_refs.write_text(md.rstrip() + "\n", encoding="utf-8")

print("main.bib entries:", len(re.findall(r"^@", main_bib.read_text(encoding='utf-8'), flags=re.M)))
print("references.tex bibitems:", len(re.findall(r"^\\bibitem", refs_tex.read_text(encoding='utf-8'), flags=re.M)))
print("Chinese reference anchors:", len(re.findall(r'<a id="r\d+"></a>', zh_refs.read_text(encoding='utf-8'))))
