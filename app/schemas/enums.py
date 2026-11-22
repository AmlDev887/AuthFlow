from enum import Enum
#---------------------TASKS ENUM ----------------------------
class TaskStatus(str, Enum):

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskSort(str,Enum):

    DESC = "desc"
    ASC = "asc"
#-------------------- USER ENUM -------------------------------
class UsersRole(str, Enum):

    ADMIN = "admin"
    USER = "user"
    SUPER_ADMIN = "super_admin"