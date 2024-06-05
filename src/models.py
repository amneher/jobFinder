from dataclasses import dataclass
from datetime import datetime, date
from uuid import uuid4
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    Integer,
    PickleType,
    String,
    ForeignKey,
    func,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

# All the entities we need to manipulate/interact with.


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("JobSeeker.id"))
    user: Mapped["JobSeeker"] = relationship(back_populates="profile")
    interests: Mapped[str] = mapped_column(String(5000))
    co_size_preference: Mapped[str] = mapped_column(String(5000))
    preferred_industries: Mapped[str] = mapped_column(String(5000))

    def __init__(
        self,
        user_id: str,
        interests: list[str],
        co_size_preference: list[str],
        preferred_industries: list[str],
    ):
        super().__init__()
        self.id = str(uuid4())
        self.user_id = user_id
        self.interests = ", ".join(interests)
        self.co_size_preference = ", ".join(co_size_preference)
        self.preferred_industries = ", ".join(preferred_industries)


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("JobSeeker.id"))
    user: Mapped["JobSeeker"] = relationship(back_populates="skills")
    key = mapped_column(String(50), nullable=False)
    value = mapped_column(Integer)

    def __init__(self, user_id: str, key: str, value: int):
        super().__init__()
        self.id = str(uuid4())
        self.user_id = user_id
        self.key = key
        self.value = value


@dataclass
class WorkExperience:
    start_date: date
    end_date: date | None
    title: str | None
    company: str | None
    location: str | None
    highlights: list[str]
    is_current: bool = False
    remote: bool = False
    skills_used: list[str] | None = None


@dataclass
class Education:
    start_date: date
    end_date: date | None
    institution: str
    level: str
    major: str
    is_current: bool = False
    graduated: bool = False


class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("JobSeeker.id"))
    user: Mapped["JobSeeker"] = relationship(back_populates="resume")
    work_experience: Mapped[WorkExperience] = mapped_column(PickleType)
    education: Mapped[Education] = mapped_column(PickleType)


class User(Base):
    __tablename__ = "users"
    id = mapped_column(String, primary_key=True)
    type: Mapped[str]
    username = mapped_column(String(100), unique=True, nullable=False)
    email = mapped_column(String(100), unique=True)
    active = mapped_column(Boolean, default=True)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    date_joined: Mapped[datetime] = mapped_column(insert_default=func.now())
    date_last_seen: Mapped[datetime] = mapped_column(insert_default=func.now())
    birthday = mapped_column(Date, nullable=True)
    is_admin = mapped_column(Boolean, default=False)
    is_verified = mapped_column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "type"}

    def __init__(
        self,
        username: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
        birthday: date = datetime.now().date(),
        is_admin: bool = False,
        is_verified: bool = False,
    ):
        super().__init__()
        self.id = str(uuid4())
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.is_admin = is_admin
        self.is_verified = is_verified

    def verify(self, info: dict[str, bool] = {"success": False}):
        if info.get("success"):
            self.is_verified = True


class JobSeeker(User):
    telephone = mapped_column(String(50))
    profile_id: Mapped[Optional[str]] = mapped_column(ForeignKey("Profile.id"))
    profile: Mapped[Profile] = relationship(back_populates="user")
    skill_ids: Mapped[Optional[List[str]]] = mapped_column(ForeignKey("Skill.id"))
    skills: Mapped[List[Skill]] = relationship()
    resume_id: Mapped[Optional[str]] = mapped_column(ForeignKey("Resume.id"))
    resume: Mapped[Resume] = relationship(back_populates="user")

    __mapper_args__ = {"polymorphic_identity": "job_seeker"}

    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        birthday: date,
        is_admin: bool,
        is_verified: bool,
        telephone: str = "",
        profile: str = "",
        skill_ids: list[str] = [""],
        resume_id: str = "",
        **kwargs: dict[str, str] | None
    ):
        super().__init__(
            username,
            email,
            first_name,
            last_name,
            birthday,
            is_admin,
            is_verified,
            **kwargs
        )
        self.telephone = telephone
        self.profile_id = profile
        self.skill_ids = skill_ids
        self.resume_id = resume_id
