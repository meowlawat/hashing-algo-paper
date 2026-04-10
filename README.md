# Empirical Reductions in Effective Password Search Spaces

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-MPS%20%7C%20CUDA-ee4c2c.svg)](https://pytorch.org/)

> [cite_start]**A Neural Approach to Bypassing Memory-Hard Key Derivation Functions** 

## 📖 Project Overview
This repository contains the code, data sanitization scripts, and methodology framework for our research on password predictability. [cite_start]Cryptographic security often relies on the theoretical search space equation ($S = R^L$), assuming humans select characters uniformly at random[cite: 23, 34]. 

[cite_start]Our research empirically demonstrates that human-generated passwords exhibit severe structural and linguistic predictability[cite: 24]. [cite_start]By utilizing a Probabilistic Context-Free Grammar (PCFG) and a character-level Long Short-Term Memory (LSTM) neural network, we developed a predictive ranking pipeline[cite: 25]. [cite_start]This pipeline effectively collapses the search space, allowing attackers to bypass the hardware limitations of memory-hard KDFs like Argon2id[cite: 62].

### ⚡ Key Findings
[cite_start]When mapped against the hardware constraints of the memory-hard Argon2id hashing algorithm running on an NVIDIA RTX 4090 (~5,000 Hashes/second)[cite: 27, 70]:
* [cite_start]**10% Database Compromise:** Achieved in 2.00 seconds[cite: 164].
* [cite_start]**30% Database Compromise:** Achieved in exactly 6.00 seconds[cite: 27, 164].

## 🧠 Methodology Framework
[cite_start]The adversarial pipeline is broken down into six distinct phases[cite: 64, 65, 68, 71, 82, 83]:

1. [cite_start]**Raw Breach Data:** Sourced from the RockYou breach corpus[cite: 64].
2. [cite_start]**Filter & Sanitize:** Filtered for strictly ASCII-compliant strings between 8 and 24 characters[cite: 65, 87].
3. [cite_start]**PCFG Structural Mapping:** Tokenization to prove mass structural reuse (e.g., `LLLLLLDD`)[cite: 68, 93, 97].
4. [cite_start]**LSTM Neural Training:** A character-level LSTM trained over 100 epochs to model human keystroke probabilities[cite: 71, 131].
5. [cite_start]**Perplexity Scoring & Ranking:** Calculating exact cross-entropy loss for 100,000 unseen validation passwords and sorting them from most to least predictable[cite: 26, 61, 82].
6. [cite_start]**GPU Hardware Execution:** Feeding the optimized list to an RTX 4090 to bypass Argon2id[cite: 83].

## 💻 Hardware Environment
* [cite_start]**Intelligence Generation Machine:** Apple Silicon (M-Series) using Metal Performance Shaders (MPS) via PyTorch `mps` backend[cite: 131, 244].
* [cite_start]**Target Attack Hardware (Simulated):** NVIDIA RTX 4090[cite: 27].
* [cite_start]**Target KDF:** Argon2id ($m=65536, t=3, p=4$)[cite: 178].

## 📂 Repository Structure
*(Note: Please ensure you create these files/folders in your repo)*
```text
├── data/
│   ├── validation_set_sample.txt   # Small sample of unseen targets
│   └── pcfg_top_skeletons.csv      # Extracted structural templates
├── src/
│   ├── sanitize_and_tokenize.py    # PCFG Tokenizer
│   ├── train_lstm.py               # PyTorch training script
│   └── score_lstm.py               # Perplexity scoring engine
├── models/
│   └── lstm_weights.pth            # (Optional: Upload only if under 100MB)
├── paper.pdf                       # The compiled IEEE manuscript
└── README.md
