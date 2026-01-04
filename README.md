# Scaling Generalist Gaming Agents via Inverse Dynamics on Walkthroughs

This project aims to significantly expand the training data available for generalist gaming agents by moving beyond videos with explicit "input overlays." By leveraging an **Inverse Dynamics Model (IDM)** trained on the [NitroGen](https://nitrogen-project.github.io/) foundation model dataset, we "pseudo-label" vast quantities of unlabelled internet gameplay videos (e.g., "Let's Plays" and walkthroughs). 

This approach allows agents to learn from a virtually unlimited source of data, drastically improving generalization across unseen games and genres.

---

## 💡 Motivation

Current state-of-the-art models like **NitroGen** rely on extracting actions from specific videos where creators have overlaid a visualization of their controller. While high-quality, this represents only a small fraction of available gaming content. 

By learning to infer actions from visual state transitions alone, we can unlock millions of hours of standard gameplay videos. This enables the model to "self-learn" action mappings from pure observation, following the precedent set by models like OpenAI's VPT.

---

## 🛠 Methodology

The pipeline consists of three core stages:

### 1. Train Inverse Dynamics Model (IDM)
We use the **NitroGen Dataset (v1.0)**, comprising ~15 billion annotated frames, to train a supervised IDM.
* **Input:** Two consecutive frames ($frame_t, frame_{t+1}$).
* **Output:** The predicted action ($action_t$) that caused the transition.
* **Goal:** Learn the mapping $f(s_t, s_{t+1}) \rightarrow a_t$.

### 2. Internet-Scale Pseudo-Labeling
The trained IDM is run for inference on a curated dataset of raw game walkthroughs.
* **Processing:** Raw pixels are converted into action sequences.
* **Filtering:** Low-confidence predictions and idle segments (e.g., loading screens, menus) are filtered out to maintain data quality.

### 3. Foundation Model Training
We combine the original ground-truth NitroGen data with the new pseudo-labeled walkthrough data to train a massive **Vision-Action Policy**.
* **Architecture:** SigLIP 2 vision encoder + Diffusion Transformer (DiT).
* **Objective:** A flow-matching objective to predict action chunks from visual context.



---

## 🚀 Future Work: World Models & Latent Actions

Beyond IDMs, this repository explores training **World Models** (Actions → Video). By learning the physics and transition dynamics of game environments, the model can:
1.  Predict future states: $P(s_{t+1} | s_t, a_t)$.
2.  Infer **Latent Actions** in scenarios where specific button mappings are unknown or ambiguous, similar to the **Genie** architecture.

---

## 📚 References

If you use this code or approach in your research, please cite the following foundational works:

```bibtex
@article{magne2025nitrogen,
  title={NitroGen: An Open Foundation Model for Generalist Gaming Agents},
  author={Magne, L. and Awadalla, A. and Wang, G. and Xu, Y. and Belofsky, J. and Hu, F. and Kim, J. and Schmidt, L. and Gkioxari, G. and Kautz, J. and Yue, Y. and Choi, Y. and Zhu, Y. and Fan, L.},
  journal={arXiv preprint},
  year={2025}
}

@inproceedings{baker2022vpt,
  title={Video PreTraining (VPT): Learning to act by watching unlabeled online videos},
  author={Baker, Bowen and Akkaya, Ilge and Zhokov, Peter and Huizinga, Joost and Tang, Jie and Ecoffet, Adrien and Houghton, Brandon and Sampedro, Raul and Clune, Jeff},
  booktitle={Advances in Neural Information Processing Systems},
  volume={35},
  pages={24639--24654},
  year={2022}
}

@article{ye2024latent,
  title={Latent action pretraining from videos},
  author={Ye, Siyuan and Jang, Joel and Jeon, Ben and Joo, Seohyun and Yang, Jiankai and Peng, Bo and Mandlekar, Ajay and Tan, Rick and Chao, Yu-Wei and Lin, Bill Yuchen and others},
  journal={arXiv preprint arXiv:2410.11758},
  year={2024}
}
```

## ⚖️ License & Disclaimers

### Open Source License
The code in this repository is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full text.

### Upstream Restrictions & Non-Commercial Use
This project is a derivative of the **NVIDIA NitroGen** model and dataset. Consequently, the following usage terms apply:
* **Non-Commercial Research:** This model and the resulting pseudo-labeled data are restricted to **non-commercial research purposes** only.
* **Prohibited Uses:** Use for military, surveillance, or commercial profit is strictly prohibited per the upstream NitroGen license.
* **Inherited Notice:** Users must retain the [NOTICE](NOTICE) file when redistributing this work to maintain proper attribution to the NitroGen and VPT frameworks.

### Data Disclaimer (Walkthroughs)
* **Fair Use:** This project utilizes publicly available gameplay walkthroughs for the purpose of research and education under the principles of "Fair Use."
* **Content Ownership:** All rights to the original gameplay footage belong to the respective content creators. We do not host or distribute raw video files.
* **Takedown Requests:** If you are a content creator and wish to have your content removed from our indexing, please open a GitHub Issue.
