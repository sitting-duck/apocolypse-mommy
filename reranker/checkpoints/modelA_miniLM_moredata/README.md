---
tags:
- sentence-transformers
- cross-encoder
- reranker
- generated_from_trainer
- dataset_size:16200
- loss:FitMixinLoss
base_model: cross-encoder/ms-marco-MiniLM-L6-v2
pipeline_tag: text-ranking
library_name: sentence-transformers
---

# CrossEncoder based on cross-encoder/ms-marco-MiniLM-L6-v2

This is a [Cross Encoder](https://www.sbert.net/docs/cross_encoder/usage/usage.html) model finetuned from [cross-encoder/ms-marco-MiniLM-L6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2) using the [sentence-transformers](https://www.SBERT.net) library. It computes scores for pairs of texts, which can be used for text reranking and semantic search.

## Model Details

### Model Description
- **Model Type:** Cross Encoder
- **Base model:** [cross-encoder/ms-marco-MiniLM-L6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2) <!-- at revision c5ee24cb16019beea0893ab7796b1df96625c6b8 -->
- **Maximum Sequence Length:** 256 tokens
- **Number of Output Labels:** 1 label
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Documentation:** [Cross Encoder Documentation](https://www.sbert.net/docs/cross_encoder/usage/usage.html)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Cross Encoders on Hugging Face](https://huggingface.co/models?library=sentence-transformers&other=cross-encoder)

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import CrossEncoder

# Download from the 🤗 Hub
model = CrossEncoder("cross_encoder_model_id")
# Get scores for pairs of texts
pairs = [
    ['explain "keeping your garden healthy" in part 1', 'for the Northeastern states”--Provided by publisher. ISBN 978-1-58923-649-3 (soft cover) 1. Gardening--Northeastern States. Gardening--Canada, Eastern. Series: Complete guide (Creative Publishing International) SB453.2.N82S74 2012 635.0974--dc23 2011036949 The Complete Guide to Northeast Gardening Created by: The Editors of Creative Publishing international, Inc., in cooperation with Black & Decker. Black & Decker® is a trademark of The Black & Decker Corporation and is used under license. NOTICE TO READERS For safety, use caution, care, and good judgment when following the procedures described in this book. The publisher and Black & Decker cannot assume responsibility for any damage to property or injury to persons as a result of misuse of the information provided. The techniques shown in this book are general techniques for various applications. In some instances, additional tech- niques not shown in this book may be required. Always follow manufacturers’ instructions included with products, since deviating from the directions may void warranties. The projects in this book vary widely as to skill levels required: some may not be appropriate for all do-it-yourselfers, and some may require professional help.'],
    ['explain these contain small high energy foods (candy, cereal bars) to be eaten', "a declination circle to find out where the shadow stick or gnomon should be placed for any day of the year. Mark off the outer circle where the 23½ degree position is, and transfer to the North-South line. Using this as a radius, draw a circle from the centre of the big circle you drew first. Mark this off by the method given above and set your shadow stick on the North-South line opposite the appropriate date. This shadow stick should be vertical, and should be set up with a plumb-bob. The shadow will fall across the elliptical line, and where it falls is Solar Time. This must be correct for the Equation of Time and Longitude Corrections. Note: A sun compass-sun clock drawn on an 'ordnance' (military) map can be used to obtain time accurately by orienting the map with the recognisable ground features, and then with the gnomon on the correct position, and the correction for time and the longitude corrections made, it should be possible to obtain accurate standard time within a minute or so."],
    ['explain wilted or yellowed stalks', 'plate facing 60 Rusty brown spore print 68 Saddle fungi 90 Saddle fungus^ 11 tfj Scleroderma vulgare 89 Shaggymane frontispiece Shoestring fungus 6 Sponge mushrooms 18 123 COMMON EDIBLE MUSHROOMS Spore color i z Spore print how to make as means of reproduction prevalence in the air 8 strobilaceus Strobilomyces 94 Strobilomyces strobilaceus 94 subdulcis plate facing 78 sublateritium 7% plate facing 44 sulphureus 94 Sulphur polypore 94 Sulphur shelf mushroom 115 Uncertain Hypholoma plate fac- ing 78 vaginata Amanltopsis 36 Vase-shaped puffball 88 Veil on stem of mushroom 13 velutipes plate fac- ing 44 Velvet-stemmed Collybia plate facing 44 verna 31 Volva at base of mushroom stem Scleroderma 89 Tooth fungi 98 Tremella lutescens 101 White spore print 27 ulmarius 66 Yellow jelly fungus'],
    ['explain fairly long distance from a disaster in my home area, so as', 'Terrain - The way the land is arranged. I think he’s on point 60 - Basic Hunting This publication was written to give new hunters ideas about hunting many species. The next step is up to you. For those people who are using the web based version, we recommend you use your search engine on the web to specify your individual needs. Most sites also contain a list of books, videos, and cookbooks. For those who are reading the printed version of this booklet, we recommend you use your local library. Look for books and magazine articles that focus on hunting specialties that interest you. Good friends - a good meal Basic Hunting - 61 Firearm SaFety tipS:• Properly store firearms and ammunition when they are not in use.• Treat every firearm as if it were loaded, every time.• When handling firearms, keep them pointed in a safe direction whether they are loaded or not.• Point firearms only at objects that you intend to shoot. This does not include televisions.• When hunting, know the location of all hunting'],
    ['explain dig two trenches about a metre apart with enough room in their', 'The defender gains control by grabbing his opponent’s head, hair, ears, or shoulders and strikes him in the groin with his knee (Figure 4-26). 4-26 FM 21-150 (5) Knee strike to face. The defender controls his opponent by grabbing behind his head with both hands and forcefully pushing his head down. At the same time, the defender brings his knee up and smashes the opponent in the face (Figure 4-27). When properly executed, the knee strike to the face is a devastating technique that can cause serious injury to the opponent.'],
]
scores = model.predict(pairs)
print(scores.shape)
# (5,)

# Or rank different texts based on similarity to a single text
ranks = model.rank(
    'explain "keeping your garden healthy" in part 1',
    [
        'for the Northeastern states”--Provided by publisher. ISBN 978-1-58923-649-3 (soft cover) 1. Gardening--Northeastern States. Gardening--Canada, Eastern. Series: Complete guide (Creative Publishing International) SB453.2.N82S74 2012 635.0974--dc23 2011036949 The Complete Guide to Northeast Gardening Created by: The Editors of Creative Publishing international, Inc., in cooperation with Black & Decker. Black & Decker® is a trademark of The Black & Decker Corporation and is used under license. NOTICE TO READERS For safety, use caution, care, and good judgment when following the procedures described in this book. The publisher and Black & Decker cannot assume responsibility for any damage to property or injury to persons as a result of misuse of the information provided. The techniques shown in this book are general techniques for various applications. In some instances, additional tech- niques not shown in this book may be required. Always follow manufacturers’ instructions included with products, since deviating from the directions may void warranties. The projects in this book vary widely as to skill levels required: some may not be appropriate for all do-it-yourselfers, and some may require professional help.',
        "a declination circle to find out where the shadow stick or gnomon should be placed for any day of the year. Mark off the outer circle where the 23½ degree position is, and transfer to the North-South line. Using this as a radius, draw a circle from the centre of the big circle you drew first. Mark this off by the method given above and set your shadow stick on the North-South line opposite the appropriate date. This shadow stick should be vertical, and should be set up with a plumb-bob. The shadow will fall across the elliptical line, and where it falls is Solar Time. This must be correct for the Equation of Time and Longitude Corrections. Note: A sun compass-sun clock drawn on an 'ordnance' (military) map can be used to obtain time accurately by orienting the map with the recognisable ground features, and then with the gnomon on the correct position, and the correction for time and the longitude corrections made, it should be possible to obtain accurate standard time within a minute or so.",
        'plate facing 60 Rusty brown spore print 68 Saddle fungi 90 Saddle fungus^ 11 tfj Scleroderma vulgare 89 Shaggymane frontispiece Shoestring fungus 6 Sponge mushrooms 18 123 COMMON EDIBLE MUSHROOMS Spore color i z Spore print how to make as means of reproduction prevalence in the air 8 strobilaceus Strobilomyces 94 Strobilomyces strobilaceus 94 subdulcis plate facing 78 sublateritium 7% plate facing 44 sulphureus 94 Sulphur polypore 94 Sulphur shelf mushroom 115 Uncertain Hypholoma plate fac- ing 78 vaginata Amanltopsis 36 Vase-shaped puffball 88 Veil on stem of mushroom 13 velutipes plate fac- ing 44 Velvet-stemmed Collybia plate facing 44 verna 31 Volva at base of mushroom stem Scleroderma 89 Tooth fungi 98 Tremella lutescens 101 White spore print 27 ulmarius 66 Yellow jelly fungus',
        'Terrain - The way the land is arranged. I think he’s on point 60 - Basic Hunting This publication was written to give new hunters ideas about hunting many species. The next step is up to you. For those people who are using the web based version, we recommend you use your search engine on the web to specify your individual needs. Most sites also contain a list of books, videos, and cookbooks. For those who are reading the printed version of this booklet, we recommend you use your local library. Look for books and magazine articles that focus on hunting specialties that interest you. Good friends - a good meal Basic Hunting - 61 Firearm SaFety tipS:• Properly store firearms and ammunition when they are not in use.• Treat every firearm as if it were loaded, every time.• When handling firearms, keep them pointed in a safe direction whether they are loaded or not.• Point firearms only at objects that you intend to shoot. This does not include televisions.• When hunting, know the location of all hunting',
        'The defender gains control by grabbing his opponent’s head, hair, ears, or shoulders and strikes him in the groin with his knee (Figure 4-26). 4-26 FM 21-150 (5) Knee strike to face. The defender controls his opponent by grabbing behind his head with both hands and forcefully pushing his head down. At the same time, the defender brings his knee up and smashes the opponent in the face (Figure 4-27). When properly executed, the knee strike to the face is a devastating technique that can cause serious injury to the opponent.',
    ]
)
# [{'corpus_id': ..., 'score': ...}, {'corpus_id': ..., 'score': ...}, ...]
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 16,200 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                                      | sentence_1                                                                                           | label                                                          |
  |:--------|:------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                                          | string                                                                                               | float                                                          |
  | details | <ul><li>min: 26 characters</li><li>mean: 66.25 characters</li><li>max: 114 characters</li></ul> | <ul><li>min: 156 characters</li><li>mean: 1215.33 characters</li><li>max: 14045 characters</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.16</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                                                                  | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | label            |
  |:--------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>explain "keeping your garden healthy" in part 1</code>                                | <code>for the Northeastern states”--Provided by publisher. ISBN 978-1-58923-649-3 (soft cover) 1. Gardening--Northeastern States. Gardening--Canada, Eastern. Series: Complete guide (Creative Publishing International) SB453.2.N82S74 2012 635.0974--dc23 2011036949 The Complete Guide to Northeast Gardening Created by: The Editors of Creative Publishing international, Inc., in cooperation with Black & Decker. Black & Decker® is a trademark of The Black & Decker Corporation and is used under license. NOTICE TO READERS For safety, use caution, care, and good judgment when following the procedures described in this book. The publisher and Black & Decker cannot assume responsibility for any damage to property or injury to persons as a result of misuse of the information provided. The techniques shown in this book are general techniques for various applications. In some instances, additional tech- niques not shown in this book may be required. Always follow manufacturers’ instructions included with p...</code> | <code>0.0</code> |
  | <code>explain these contain small high energy foods (candy, cereal bars) to be eaten</code> | <code>a declination circle to find out where the shadow stick or gnomon should be placed for any day of the year. Mark off the outer circle where the 23½ degree position is, and transfer to the North-South line. Using this as a radius, draw a circle from the centre of the big circle you drew first. Mark this off by the method given above and set your shadow stick on the North-South line opposite the appropriate date. This shadow stick should be vertical, and should be set up with a plumb-bob. The shadow will fall across the elliptical line, and where it falls is Solar Time. This must be correct for the Equation of Time and Longitude Corrections. Note: A sun compass-sun clock drawn on an 'ordnance' (military) map can be used to obtain time accurately by orienting the map with the recognisable ground features, and then with the gnomon on the correct position, and the correction for time and the longitude corrections made, it should be possible to obtain accurate standard time within a minute o...</code> | <code>0.0</code> |
  | <code>explain wilted or yellowed stalks</code>                                              | <code>plate facing 60 Rusty brown spore print 68 Saddle fungi 90 Saddle fungus^ 11 tfj Scleroderma vulgare 89 Shaggymane frontispiece Shoestring fungus 6 Sponge mushrooms 18 123 COMMON EDIBLE MUSHROOMS Spore color i z Spore print how to make as means of reproduction prevalence in the air 8 strobilaceus Strobilomyces 94 Strobilomyces strobilaceus 94 subdulcis plate facing 78 sublateritium 7% plate facing 44 sulphureus 94 Sulphur polypore 94 Sulphur shelf mushroom 115 Uncertain Hypholoma plate fac- ing 78 vaginata Amanltopsis 36 Vase-shaped puffball 88 Veil on stem of mushroom 13 velutipes plate fac- ing 44 Velvet-stemmed Collybia plate facing 44 verna 31 Volva at base of mushroom stem Scleroderma 89 Tooth fungi 98 Tremella lutescens 101 White spore print 27 ulmarius 66 Yellow jelly fungus</code>                                                                                                                                                                                                                    | <code>0.0</code> |
* Loss: [<code>FitMixinLoss</code>](https://sbert.net/docs/package_reference/cross_encoder/losses.html#fitmixinloss)

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `num_train_epochs`: 1
- `fp16`: True

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 1
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `bf16`: False
- `fp16`: True
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 0.4936 | 500  | 0.4083        |
| 0.9872 | 1000 | 0.2858        |


### Framework Versions
- Python: 3.11.0rc1
- Sentence Transformers: 5.1.2
- Transformers: 4.57.1
- PyTorch: 2.6.0+cu124
- Accelerate: 1.11.0
- Datasets: 4.3.0
- Tokenizers: 0.22.1

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->