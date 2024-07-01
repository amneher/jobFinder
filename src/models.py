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

    # get, add, remove, x in interests
    def get_interests(self) -> list[str]:
        interests = self.interests.split(", ")
        return sorted(interests)
    
    def add_interest(self, interest: str) -> list[str]:
        interests = self.interests.split(", ")
        interests.append("".join(interest.lower().strip().split(" ")))
        return sorted(interests)
    
    def remove_interest(self, interest: str) -> bool:
        old_interests = [i.lower().strip() for i in self.interests.split(", ")]
        new_interests = [i for i in old_interests if i != interest]
        self.interests = ", ".join(new_interests)
        return interest not in self.interests.split(", ")
    
    def has_interest(self, interest: str) -> bool:
        return interest in self.interests.split(", ")

    # get, add, remove, x in co_size_pref
    def get_co_size_preference(self) -> list[str]:
        co_size_preference = self.co_size_preference.split(", ")
        return sorted(co_size_preference)
    
    def add_co_size_preference(self, co_size_preference: str) -> list[str]:
        co_size_preferences = self.co_size_preference.split(", ")
        co_size_preferences.append("".join(co_size_preference.lower().strip().split(" ")))
        return sorted(co_size_preferences)
    
    def remove_co_size_preference(self, co_size_preference: str) -> bool:
        old_co_size_preferences = [i.lower().strip() for i in self.co_size_preference.split(", ")]
        new_co_size_preferences = [i for i in old_co_size_preferences if i != co_size_preference]
        self.co_size_preference = ", ".join(new_co_size_preferences)
        return co_size_preference not in self.co_size_preference.split(", ")
    
    def has_co_size_preference(self, co_size_preference: str) -> bool:
        return co_size_preference in self.co_size_preference.split(", ")

    # get, add, remove, x in pref_industries
    def get_preferred_industries(self) -> list[str]:
        preferred_industries = self.preferred_industries.split(", ")
        return sorted(preferred_industries)
    
    def add_preferred_industries(self, preferred_industry: str) -> list[str]:
        preferred_industries = self.preferred_industries.split(", ")
        preferred_industries.append("".join(preferred_industry.lower().strip().split(" ")))
        return sorted(preferred_industries)
    
    def remove_preferred_industries(self, preferred_industry: str) -> bool:
        old_preferred_industries = [i.lower().strip() for i in self.preferred_industries.split(", ")]
        new_preferred_industries = [i for i in old_preferred_industries if i != preferred_industry]
        self.preferred_industries = ", ".join(new_preferred_industries)
        return preferred_industry not in self.preferred_industries.split(", ")
    
    def has_preferred_industry(self, preferred_industry: str) -> bool:
        return preferred_industry in self.preferred_industries.split(", ")

    # get, add, remove, x in ...



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
