---
tags:
- sentence-transformers
- cross-encoder
- reranker
- generated_from_trainer
- dataset_size:15255
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
    ['explain choose the next hide area first', 'Actions in the hole-up area are the same as in hide site, except that you can move away from the hole-up area to get and prepare food. Actions in the hole-up area include-- • Selecting and occupying the next hide site (remember you are still in a dangerous situation; this is not a friendly area). • Reconnoitering the area for resources and potential concealed movement routes to the alternate hide site. • Gathering food (nuts, berries, vegetables). When moving around the area for food, maintain security and avoid leaving tracks or other signs. When setting traps and snares, keep them well- camouflaged and in areas where people are not likely to discover them. Remember, the local population sometimes heavily travels trails near water sources. Page 212 of 233 FM 21-76 US ARMY SURVIVAL MANUAL Reprinted as permitted by U.S. Department of the Army • Getting water from sources within the hide area. Be careful not to leave tracks of signs along the banks of water sources when getting water. Moving on hard rocks or logs along the banks to'],
    ['explain over 4 7 days to new baseline', '– UV-A rays of the sun kill germs such as viruses, bacteria and parasites. – Rule of thumb for cloudy weather: if less than half of the sky is clouded over, six hours will be sufficient to disinfect the water completely. If more than half of the sky is covered with clouds, the bottles must be placed in the sun for two consecutive days. – The method does not work satisfactorily during days with continuous rainfall. Explain Step 4: The water is ready for consumption. – The water can be stored for several days if the bottle is kept unopened after treatment and stored in a cool, dark place. – To prevent recontamination, drink the water directly from the bottle or pour it into a clean cup or glass immediately before drinking. Explain the advantages and drawbacks of the SODIS method in the local context. Man placing bottles on a SODIS table 44 School lessons Good behaviour practice - the SODIS method Materials: 12 PET bottles, 6 litres of raw water Infrastructure: SODIS station 1.'],
    ['explain of some egyptian aromatic plants', '26:245–250. 103 WHO monographs on selected medicinal plants 23. Janssen AM et al. Screening for antibacterial activity of some essential oils by the agar overlay technique. Pharmaceutisch Weekblad 8:289–292. 24. Ontengco DC et al. Screening for the antibacterial activity of essential oils from some Philippine plants. Acta Manilana 43:19–23. 25. Ross SA et al. Antimicrobial activity of some Egyptian plants. Fitoterapia 51: 201–205. 26. Kufferath F Mundualdo GM. The activity of some preparations containing essen- tial oils in tuberculosis. Fitoterapia 25:483–485. 27. Wagner H et al. In vitro inhibition of prostaglandin biosynthesis by essential oils and phenolic compounds. Planta Medica 3:184–187. 28. Boyd EM Pearson GL. On the expectorant action of volatile oils. American Journal of Medical Science 211:602–610. 29. Boyd EM Sheppard EP. The effect of steam inhalation of volatile oils on the output and composition of respiratory tract ﬂuid. Journal of Pharmaceutical and Experiential Practice 163:250–256. 30. Misawa M Kizawa M. Antitussive effects of several volatile oils especially of cedar leaf oil in guinea pigs. Pharmacometrics 39:81–87. 31. Burrows'],
    ['explain the bloom sharp, and is aided by a stiff brush', 'away in the direction the tooth grows: sweep upper teeth down and lower teeth up. Explain how important it is to use a brush with soft hairs. A brush that is stiff and hard will hurt the gums, not help them. YES You can make a hard brush softer by putting the hairs Into hot water for a few minutes. Do not put the plastic handle Into the hot water, or it w ~ l l melt. If your store has only hard brushes, tell the storekeeper that hard toothbrushes do not help the people in the community. Ask him to order and sell only soft toothbrushes. Note: Another important way to reduce cavities is by adding fluoride to teeth. Fluoride is a substance which, like calcium, makes teeth harder and stronger. Fluoride in drinking water, toothpaste, vilamins, and mouth rinses, helps t o prevent cavities. These methods are sometimes expensive. Perhaps the most effective and inexpensive rnethod is the weekly rinse a t school, described on page 167. Fluoride can also be found naturally in food and water.'],
    ['explain dry cement on the wet surface to absorb excess water', 'Remove the extra cement from around the cavity and the tooth. Explain things t o the person. The cavity and the area around it must be dry so you can see what you are doing. Just as important, cement stays longer inside a dry cavity. Place cotton between the cheek and gums t o keep the area dry. Put some cotton under the tongue when you work on a lower tooth. Use whatever kind of cotton you have: gauze, wool, or even rolls. Change the cotton whenever it becomes wet. Keep the cavity dry while you work. Wipe the inside of i t every now and then with a bit of cotton. Then leave a piece of cotton inside the cavity while you mix the cement. Lift out some of the decay. You do not need to remove all of the decay on the bottom of the cavity. You can leave some, as long as you cover it with cement. If you try t o dig out all of the'],
]
scores = model.predict(pairs)
print(scores.shape)
# (5,)

# Or rank different texts based on similarity to a single text
ranks = model.rank(
    'explain choose the next hide area first',
    [
        'Actions in the hole-up area are the same as in hide site, except that you can move away from the hole-up area to get and prepare food. Actions in the hole-up area include-- • Selecting and occupying the next hide site (remember you are still in a dangerous situation; this is not a friendly area). • Reconnoitering the area for resources and potential concealed movement routes to the alternate hide site. • Gathering food (nuts, berries, vegetables). When moving around the area for food, maintain security and avoid leaving tracks or other signs. When setting traps and snares, keep them well- camouflaged and in areas where people are not likely to discover them. Remember, the local population sometimes heavily travels trails near water sources. Page 212 of 233 FM 21-76 US ARMY SURVIVAL MANUAL Reprinted as permitted by U.S. Department of the Army • Getting water from sources within the hide area. Be careful not to leave tracks of signs along the banks of water sources when getting water. Moving on hard rocks or logs along the banks to',
        '– UV-A rays of the sun kill germs such as viruses, bacteria and parasites. – Rule of thumb for cloudy weather: if less than half of the sky is clouded over, six hours will be sufficient to disinfect the water completely. If more than half of the sky is covered with clouds, the bottles must be placed in the sun for two consecutive days. – The method does not work satisfactorily during days with continuous rainfall. Explain Step 4: The water is ready for consumption. – The water can be stored for several days if the bottle is kept unopened after treatment and stored in a cool, dark place. – To prevent recontamination, drink the water directly from the bottle or pour it into a clean cup or glass immediately before drinking. Explain the advantages and drawbacks of the SODIS method in the local context. Man placing bottles on a SODIS table 44 School lessons Good behaviour practice - the SODIS method Materials: 12 PET bottles, 6 litres of raw water Infrastructure: SODIS station 1.',
        '26:245–250. 103 WHO monographs on selected medicinal plants 23. Janssen AM et al. Screening for antibacterial activity of some essential oils by the agar overlay technique. Pharmaceutisch Weekblad 8:289–292. 24. Ontengco DC et al. Screening for the antibacterial activity of essential oils from some Philippine plants. Acta Manilana 43:19–23. 25. Ross SA et al. Antimicrobial activity of some Egyptian plants. Fitoterapia 51: 201–205. 26. Kufferath F Mundualdo GM. The activity of some preparations containing essen- tial oils in tuberculosis. Fitoterapia 25:483–485. 27. Wagner H et al. In vitro inhibition of prostaglandin biosynthesis by essential oils and phenolic compounds. Planta Medica 3:184–187. 28. Boyd EM Pearson GL. On the expectorant action of volatile oils. American Journal of Medical Science 211:602–610. 29. Boyd EM Sheppard EP. The effect of steam inhalation of volatile oils on the output and composition of respiratory tract ﬂuid. Journal of Pharmaceutical and Experiential Practice 163:250–256. 30. Misawa M Kizawa M. Antitussive effects of several volatile oils especially of cedar leaf oil in guinea pigs. Pharmacometrics 39:81–87. 31. Burrows',
        'away in the direction the tooth grows: sweep upper teeth down and lower teeth up. Explain how important it is to use a brush with soft hairs. A brush that is stiff and hard will hurt the gums, not help them. YES You can make a hard brush softer by putting the hairs Into hot water for a few minutes. Do not put the plastic handle Into the hot water, or it w ~ l l melt. If your store has only hard brushes, tell the storekeeper that hard toothbrushes do not help the people in the community. Ask him to order and sell only soft toothbrushes. Note: Another important way to reduce cavities is by adding fluoride to teeth. Fluoride is a substance which, like calcium, makes teeth harder and stronger. Fluoride in drinking water, toothpaste, vilamins, and mouth rinses, helps t o prevent cavities. These methods are sometimes expensive. Perhaps the most effective and inexpensive rnethod is the weekly rinse a t school, described on page 167. Fluoride can also be found naturally in food and water.',
        'Remove the extra cement from around the cavity and the tooth. Explain things t o the person. The cavity and the area around it must be dry so you can see what you are doing. Just as important, cement stays longer inside a dry cavity. Place cotton between the cheek and gums t o keep the area dry. Put some cotton under the tongue when you work on a lower tooth. Use whatever kind of cotton you have: gauze, wool, or even rolls. Change the cotton whenever it becomes wet. Keep the cavity dry while you work. Wipe the inside of i t every now and then with a bit of cotton. Then leave a piece of cotton inside the cavity while you mix the cement. Lift out some of the decay. You do not need to remove all of the decay on the bottom of the cavity. You can leave some, as long as you cover it with cement. If you try t o dig out all of the',
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

* Size: 15,255 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                                      | sentence_1                                                                                          | label                                                          |
  |:--------|:------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                                          | string                                                                                              | float                                                          |
  | details | <ul><li>min: 15 characters</li><li>mean: 65.18 characters</li><li>max: 130 characters</li></ul> | <ul><li>min: 263 characters</li><li>mean: 1073.81 characters</li><li>max: 8457 characters</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.17</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                            | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | label            |
  |:------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>explain choose the next hide area first</code>  | <code>Actions in the hole-up area are the same as in hide site, except that you can move away from the hole-up area to get and prepare food. Actions in the hole-up area include-- • Selecting and occupying the next hide site (remember you are still in a dangerous situation; this is not a friendly area). • Reconnoitering the area for resources and potential concealed movement routes to the alternate hide site. • Gathering food (nuts, berries, vegetables). When moving around the area for food, maintain security and avoid leaving tracks or other signs. When setting traps and snares, keep them well- camouflaged and in areas where people are not likely to discover them. Remember, the local population sometimes heavily travels trails near water sources. Page 212 of 233 FM 21-76 US ARMY SURVIVAL MANUAL Reprinted as permitted by U.S. Department of the Army • Getting water from sources within the hide area. Be careful not to leave tracks of signs along the banks of water sources when getting water. Mo...</code> | <code>0.0</code> |
  | <code>explain over 4 7 days to new baseline</code>    | <code>– UV-A rays of the sun kill germs such as viruses, bacteria and parasites. – Rule of thumb for cloudy weather: if less than half of the sky is clouded over, six hours will be sufficient to disinfect the water completely. If more than half of the sky is covered with clouds, the bottles must be placed in the sun for two consecutive days. – The method does not work satisfactorily during days with continuous rainfall. Explain Step 4: The water is ready for consumption. – The water can be stored for several days if the bottle is kept unopened after treatment and stored in a cool, dark place. – To prevent recontamination, drink the water directly from the bottle or pour it into a clean cup or glass immediately before drinking. Explain the advantages and drawbacks of the SODIS method in the local context. Man placing bottles on a SODIS table 44 School lessons Good behaviour practice - the SODIS method Materials: 12 PET bottles, 6 litres of raw water Infrastructure: SODIS station 1.</code>               | <code>0.0</code> |
  | <code>explain of some egyptian aromatic plants</code> | <code>26:245–250. 103 WHO monographs on selected medicinal plants 23. Janssen AM et al. Screening for antibacterial activity of some essential oils by the agar overlay technique. Pharmaceutisch Weekblad 8:289–292. 24. Ontengco DC et al. Screening for the antibacterial activity of essential oils from some Philippine plants. Acta Manilana 43:19–23. 25. Ross SA et al. Antimicrobial activity of some Egyptian plants. Fitoterapia 51: 201–205. 26. Kufferath F Mundualdo GM. The activity of some preparations containing essen- tial oils in tuberculosis. Fitoterapia 25:483–485. 27. Wagner H et al. In vitro inhibition of prostaglandin biosynthesis by essential oils and phenolic compounds. Planta Medica 3:184–187. 28. Boyd EM Pearson GL. On the expectorant action of volatile oils. American Journal of Medical Science 211:602–610. 29. Boyd EM Sheppard EP. The effect of steam inhalation of volatile oils on the output and composition of respiratory tract ﬂuid. Journal of Pharmaceutical and Experiential Pract...</code> | <code>0.0</code> |
* Loss: [<code>FitMixinLoss</code>](https://sbert.net/docs/package_reference/cross_encoder/losses.html#fitmixinloss)

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `num_train_epochs`: 2
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
- `num_train_epochs`: 2
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
| 0.5241 | 500  | 0.7468        |
| 1.0482 | 1000 | 0.049         |
| 1.5723 | 1500 | 0.0276        |


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