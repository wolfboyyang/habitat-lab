import copy
import os.path as osp
from typing import Any, Dict

import habitat
from habitat import Config
from habitat.core.dataset import Episode
from habitat.core.registry import registry
from habitat.datasets.rearrange.rearrange_dataset import RearrangeDatasetV0
from habitat.tasks.rearrange.rearrange_task import RearrangeTask

TASK_CONFIGS_DIR = "configs/tasks/rearrange/"


def load_task_object(
    task_cls_name: str,
    task_config_path: str,
    cur_config: Config,
    cur_env: RearrangeTask,
    cur_dataset: RearrangeDatasetV0,
    should_super_reset: bool,
    task_kwargs: Dict[str, Any],
    episode: Episode,
) -> RearrangeTask:
    """
    Loads a task. Used when a task needs to be simulated within another task. For example, this is used to get the starting state of another task as a navigation goal in the Habitat 2.0 navigation task. The loaded task uses the information and dataset from the main task (which is also passed into this function).

    :param task_cls_name: The name of the task to load.
    :param task_config_path: The path to the config for the task to load.
    :param cur_config: The config for the main task.
    :param cur_env: The main task.
    """
    task_cls = registry.get_task(task_cls_name)

    config = copy.copy(cur_config)
    config.defrost()
    if task_config_path is not None:
        task_config = habitat.get_config(
            osp.join(TASK_CONFIGS_DIR, task_config_path + ".yaml")
        )
        config.merge_from_other_cfg(task_config.TASK)
    config.freeze()
    task = task_cls(config=config, dataset=cur_dataset, sim=cur_env._sim)

    task.set_args(**task_kwargs)
    task.set_sim_reset(should_super_reset)
    task.reset(episode)
    return task
