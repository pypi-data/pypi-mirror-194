import logging
import os
import shutil

from roboflow2huggingface.hf_utils.dataset_script import \
    export_hf_dataset_script

from .hf_utils.dataset_card import export_hf_dataset_card
from .hf_utils.hub import export_thumbnail, upload_dataset_to_hfhub
from .other_utils import extract_random_image_from_valid_zip
from .roboflow_utils import (create_mini_valid_split_from_coco,
                             create_mini_valid_split_from_folder,
                             download_roboflow_dataset, fix_annotations_files,
                             normalize_dataset_labels,
                             read_dataset_labels_from_coco,
                             zip_roboflow_dataset)
from .yolov5_utils import make_dataset_yolov5_trainable

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
LOGGER = logging.getLogger(__name__)


__version__ = "0.0.21"


def roboflow_to_huggingface_pipeline(
    roboflow_universe_url: str,
    hf_dataset_id: str,
    roboflow_api_key: str = None,
    local_data_dir: str = "roboflow_dataset",
    hf_private: bool = False,
    hf_write_token: str = None,
    keep_local: bool = False,
    make_yolov5_trainable: bool = False,
    mini_valid_split_sample_num: int = 3,
):
    """
    Downloads a Roboflow dataset and uploads it to the Hugging Face Hub.

    Args:
        roboflow_universe_url (str): The Roboflow universe URL.
        hf_dataset_id (str): The name of the dataset on the Hugging Face Hub.
        roboflow_api_key (str, optional): The Roboflow API key. Defaults to None.
        local_data_dir (str, optional): The local directory to download the dataset to. Defaults to "roboflow_dataset".
        hf_private (bool, optional): Whether the dataset should be private on the Hugging Face Hub. Defaults to False.
        hf_write_token (str, optional): The token to use to authenticate to the Hugging Face Hub. Defaults to None.
        keep_local (bool, optional): Whether to keep the local dataset. Defaults to False.
        make_yolov5_trainable (bool, optional): Whether to convert the dataset to a YOLOv5 trainable format. Defaults to False.
        mini_valid_split_sample_num (int, optional): The number of samples to use for the mini validation split. Defaults to 3.
    """
    roboflow_api_key = roboflow_api_key or os.environ.get("ROBOFLOW_API_KEY")

    roboflow_project, roboflow_dataset, task = download_roboflow_dataset(
        roboflow_universe_url, api_key=roboflow_api_key, location=local_data_dir
    )
    normalize_dataset_labels(local_data_dir)
    fix_annotations_files(local_data_dir)

    # create mini validation split
    if task in ["object-detection", "instance-segmentation"]:
        create_mini_valid_split_from_coco(
            local_data_dir, num_samples=mini_valid_split_sample_num
        )
    elif task == "image-classification":
        create_mini_valid_split_from_folder(local_data_dir)

    # read dataset labels
    if task in ["object-detection", "instance-segmentation"]:
        dataset_labels = read_dataset_labels_from_coco(local_data_dir)
    elif task == "image-classification":
        dataset_labels = list(roboflow_project.classes.keys())

    zip_roboflow_dataset(local_data_dir, roboflow_dataset=roboflow_dataset)

    # export dataset python script
    export_hf_dataset_script(
        hf_dataset_id=hf_dataset_id,
        dataset_labels=dataset_labels,
        roboflow_dataset=roboflow_dataset,
        export_dir=local_data_dir,
        roboflow_universe_url=roboflow_universe_url,
        task=task,
    )

    # export thumbnail
    image_path = extract_random_image_from_valid_zip(
        local_data_dir, export_dir=local_data_dir, task=task
    )
    export_thumbnail(image_path=image_path, repo_id=hf_dataset_id, task=task)
    os.remove(image_path)

    export_hf_dataset_card(
        dataset_labels=dataset_labels,
        export_dir=local_data_dir,
        task=task,
        roboflow_universe_url=roboflow_universe_url,
        hf_dataset_id=hf_dataset_id,
        split_name_to_num_samples=roboflow_dataset.splits,
    )

    upload_dataset_to_hfhub(
        dataset_dir=local_data_dir,
        repo_id=hf_dataset_id,
        token=hf_write_token,
        private=hf_private,
    )

    if not keep_local:
        shutil.rmtree(local_data_dir)

    if make_yolov5_trainable and keep_local:
        LOGGER.info("Making dataset YOLOv5 trainable...")
        datayaml_path = make_dataset_yolov5_trainable(
            roboflow_dataset_dir=local_data_dir
        )

        LOGGER.info(
            f"YOLOv5 training data is ready! You can find the data.yaml file at {datayaml_path}"
        )

        return datayaml_path
