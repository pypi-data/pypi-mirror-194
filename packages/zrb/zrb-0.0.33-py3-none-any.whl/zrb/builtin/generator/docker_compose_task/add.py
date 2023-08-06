from typing import Any
from ..._group import project_add_group
from ....task.task import Task
from ....task.decorator import python_task
from ....task_input.str_input import StrInput
from ....task.resource_maker import ResourceMaker
from ....runner import runner
from .._common import (
    project_dir_input, task_name_input, http_port_input, validate_project_dir,
    get_automation_module_name, validate_automation_name, register_module,
    get_default_task_replacements, get_default_task_replacement_middlewares,
    new_task_scaffold_lock
)

import os

# Common definitions

current_dir = os.path.dirname(__file__)


@python_task(
    name='task-validate-create',
    inputs=[project_dir_input, task_name_input],
)
def validate(*args: Any, **kwargs: Any):
    project_dir = kwargs.get('project_dir')
    validate_project_dir(project_dir)
    task_name = kwargs.get(project_dir, 'task_name')
    validate_automation_name(project_dir, task_name)


replacements = get_default_task_replacements()
replacements.update({
    'composeCommand': '{{ util.coalesce(input.compose_command, "up") }}',
    'ENV_PREFIX': '{{ util.coalesce(input.env_prefix, "MY").upper() }}'
})
copy_resource = ResourceMaker(
    name='copy-resource',
    inputs=[
        project_dir_input,
        task_name_input,
        http_port_input,
        StrInput(
            name='compose-command', prompt='Compose command', default='up'
        ),
        StrInput(
            name='env-prefix', prompt='Env prefix', default='MY'
        ),
    ],
    upstreams=[validate],
    replacements=replacements,
    replacement_middlewares=get_default_task_replacement_middlewares(),
    template_path=os.path.join(current_dir, 'template'),
    destination_path='{{ input.project_dir }}',
    scaffold_locks=[new_task_scaffold_lock]
)


@python_task(
    name='docker-compose-task',
    group=project_add_group,
    inputs=[project_dir_input, task_name_input],
    upstreams=[copy_resource],
    runner=runner
)
def add_docker_compose_task(*args: Any, **kwargs: Any):
    task: Task = kwargs.get('_task')
    project_dir = kwargs.get('project_dir')
    validate_project_dir(project_dir)
    task_name = kwargs.get('task_name')
    task.print_out(f'Register docker-compose task: {task_name}')
    module_name = get_automation_module_name(task_name)
    register_module(project_dir, module_name)
