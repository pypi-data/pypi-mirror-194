# roboflow2huggingface

Convert Roboflow datasets into HuggingFace datasets format and upload to HuggingFace Hub.

Supports `image-classification`, `object-detection`, and `instance-segmentation` formats.

## installation

```bash
pip install roboflow2huggingface
```

## api usage

```python
from roboflow2huggingface import roboflow_to_huggingface_pipeline

roboflow_to_huggingface_pipeline(
    roboflow_universe_url='https://universe.roboflow.com/boxer5/123-qq5ea/dataset/6',
    roboflow_api_key=YOUR-ROBOFLOW-API-KEY,
    hf_dataset_id=DESIRED-HF-HUB-ID,
    hf_write_token=YOUR-HF-WRITE-TOKEN,
)

```

## cli usage

```bash
roboflow2huggingface --roboflow_universe_url https://universe.roboflow.com/boxer5/123-qq5ea/dataset/6 --roboflow_api_key YOUR-ROBOFLOW-API-KEY --hf_dataset_id DESIRED-HF-HUB-ID --hf_write_token YOUR-HF-WRITE-TOKEN
```

## converted datasets

Check converted datasets on the 🤗 hub: https://huggingface.co/datasets?other=roboflow2huggingface