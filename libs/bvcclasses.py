import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from libs.bvcutils import (
    generate_fake_profile,
    generate_uuid,
    get_random_photo,
    get_random_voice,
    read_patients,
)
from libs.bvcutils import read_models

class Role(Enum):
    VISITOR = "访客"
    STUDENT = "学生"
    TEACHER = "教师"
    ADMIN = "管理员"

    def __str__(self):
        return self.value

def assign_patients(role, mode) -> list:
    match (role, mode):
        case _:
        # case (Role.TEACHER, '模型研究'):
            models = read_models()
            patients = [Patient(model=Model(**model)) for model in models.to_dict(orient="records")]
        # case _:
        #     patients_df = read_patients()
        #     match role:
        #         case _:
        #             patients_list = patients_df.sample(n=1, ignore_index=True).to_dict(orient="records")
        #     patients = [Patient(**set_model(), **patient) for patient in patients_list]
        #     for patient in patients:
        #         for question in patient.questions:
        #             random.shuffle(question['answers'])
    return patients

def set_model() -> dict:
    return read_models().sample(n=1).to_dict(orient="records")[0]

@dataclass
class User:
    role: Role = Role.VISITOR
    mode: str = None
    id: str = field(default_factory=generate_uuid)
    name: str = None
    grade: str = None
    major: str = None
    patients: list = field(default_factory=list)

    def assign_patients(self):
        pass
        # self.patients = assign_patients(self.role, self.mode)

@dataclass
class Model:
    use: bool = None
    platform: str = None
    series: str = None
    name: str = None
    module: str = None
    free: bool = None


@dataclass
class Patient:
    model: Model = None
    messages: list = field(default_factory=list)
    begin_time: datetime  = None
    chat_duration_time: timedelta = timedelta(seconds=0)
    end_time: datetime  = None
    inquiry_count: int = 1
    info: dict|str = field(default_factory=dict)
    reports: dict = field(default_factory=dict)
    questions: list = field(default_factory=list)



@dataclass
class FakeProfile:
    profile: dict = field(default_factory=generate_fake_profile)
    photo: str = field(default_factory=get_random_photo)
    voice: str = field(default_factory=get_random_voice)
