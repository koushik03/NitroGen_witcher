Project: Scaling Generalist Gaming Agents via Inverse Dynamics on Walkthroughs
Overview
This project aims to significantly expand the training data available for generalist gaming agents by moving beyond videos with explicit "input overlays." Building upon the NitroGen foundation model, which correlates video frames with ground-truth actions extracted from controller overlays, this project utilizes the NitroGen dataset to train an Inverse Dynamics Model (IDM).
This IDM is subsequently used to "pseudo-label" the vast quantity of unlabeled internet gameplay videos (e.g., "Let's Plays" and Walkthroughs), allowing the agent to learn from a virtually unlimited source of data and improve generalization across unseen games and genres.
Motivation
Current state-of-the-art models like NitroGen rely on extracting actions from specific videos where content creators have overlaid a visualization of their controller,. While this yields high-quality data (40,000 hours across 1,000+ games), it represents only a fraction of available gaming content.
By learning to infer actions from visual state transitions alone (Inverse Dynamics), we can unlock the millions of hours of standard gameplay videos available online, effectively enabling the model to "self-learn" action mappings from observation.
Methodology
1. Train Inverse Dynamics Model (IDM)
Using the NitroGen Dataset (which pairs raw frames with extracted gamepad actions), we train a supervised IDM.
• Input: Two consecutive frames (frame 
t
​
 , frame 
t+1
​
 ).
• Output: The action (action 
t
​
 ) that caused the transition.
• Data Source: NitroGen Dataset (v1.0), comprising ~15 billion annotated frames.
2. Internet-Scale Pseudo-Labeling
The trained IDM is run for inference on a curated dataset of raw game walkthroughs (videos without overlays). This process generates estimated action labels for every frame of the previously unusable video data.
• Filtering: Low-confidence predictions and idle segments are filtered out to maintain data quality, similar to the NitroGen processing pipeline.
3. Foundation Model Training
We combine the original ground-truth NitroGen data with the new pseudo-labeled walkthrough data to train a larger Vision-Action Policy.
• Architecture: Following the NitroGen architecture, we utilize a SigLIP 2 vision encoder and a Diffusion Transformer (DiT) for action generation.
• Objective: Flow-matching objective to predict action chunks from visual context.
Future Work: World Models & Latent Actions
In addition to IDMs, this repository explores using the dataset to train World Models (Actions → Video). By learning the physics and transition dynamics of the game environments, the model can infer latent actions in scenarios where specific button mappings are unknown or ambiguous.
References & Inspiration
This project is directly inspired by the following foundational papers:
• NitroGen (Base Model & Dataset):
    ◦ Magne, L., et al. (2025). NitroGen: An Open Foundation Model for Generalist Gaming Agents. See Paper
    ◦ Source of the labeled overlay dataset and base policy architecture.
• VPT (Inverse Dynamics Inspiration):
    ◦ Baker, B., et al. (2022). Video PreTraining (VPT): Learning to Act by Watching Unlabeled Online Videos. NeurIPS.
    ◦ Proposed the method of training an IDM on a small labeled dataset to label a massive internet dataset (Minecraft).
• Genie (Latent Actions):
    ◦ Bruce, J., et al. (2024). Genie: Generative Interactive Environments. ICML.
    ◦ Inspiration for learning latent policies and world models from video only.
