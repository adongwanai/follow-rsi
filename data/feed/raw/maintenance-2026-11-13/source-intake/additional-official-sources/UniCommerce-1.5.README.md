# UniCommerce-1.5: A Compact Unified E-commerce LLM with Structured Prompts and CoT Distillation

A dataset for training and evaluating LLMs on e-commerce tasks.

## Overview

UniCommerce-1.5 is a compact unified large language model designed for e-commerce applications. Based on [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), the model leverages structured prompts and Chain-of-Thought (CoT) distillation to achieve strong performance across six e-commerce tasks:

- **Product Matching**: Determine if two product listings refer to the same product
- **Product Classification**: Classify product-query relevance
- **Product Substitute Identification**: Identify if a product can substitute for user needs
- **Product Relation Prediction**: Predict relationships between product pairs
- **Answer Generation**: Generate answers from product reviews
- **Sequential Recommendation**: Predict next purchase based on history

The training data is derived from [eCeLLM](https://ninglab.github.io/eCeLLM/) dataset.

## Dataset

The dataset contains training and test splits stored in JSON format under `datasets/`:
- `datasets/train_all.json` - Combined training data
- `datasets/test/` - Test sets for each task

## Installation

```bash
pip install -r requirements.txt
```

## Usage
### Model Fine-tuning

Fine-tune using [LlamaFactory](https://github.com/hiyouga/LlamaFactory):

### Evaluation

Test online large models:

```bash
python test_online_models.py
```

Evaluate fine-tuned model results:

```bash
python evaluate_result.py
```

## Project Structure

```
.
├── process_qapairs.py          # Data preprocessing
├── test_online_models.py       # Online model evaluation
├── evaluate_result.py          # Evaluate fine-tuned model results
├── <task_name>.py           # Data generation scripts
├── datasets/
│   ├── train_all.json         # Training data
│   └── test/                  # Test sets
└── requirements.txt           # Dependencies
```

## License
This project is licensed under the Apache-2.0 license.
