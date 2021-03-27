from controllers.tasks_controller import tasks
from controllers.lists_controller import lists
from controllers.auth_controller import auth

registerable_controllers = [
    auth,
    tasks,
    lists
]