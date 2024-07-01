from dataclasses import dataclass
import json
import pytest

from src.models import JobSeeker, Profile, db, User


@pytest.fixture
def session(request):
    if "use_root_db_user" in request.node.keywords:
        with_admin_user = True
    else:
        with_admin_user = False
    engine = db.new_engine(with_admin_user=with_admin_user)
    session = db.new_session(engine, autoflush=False, autocommit=False)
    yield session
    session.close()
    engine.dispose()


# Users
@pytest.fixture(scope="class")
def user_1_data():
    with open("./fixtures/test_users.json", "r+") as fp:
        data = json.loads(fp.read())
        user_1_data = data["test_user_1"]
        return user_1_data


@pytest.fixture(scope="class")
def test_user_1(session, user_1_data):
    user_1 = User(**user_1_data)
    session.add(user_1)
    session.commit()
    return user_1


@pytest.fixture(scope="class")
def user_2_data():
    with open("./fixtures/test_users.json", "r+") as fp:
        data = json.loads(fp.read())
        user_2_data = data["test_user_2"]
        return user_2_data


@pytest.fixture(scope="class")
def test_user_2(session, user_2_data):
    user_2 = User(**user_2_data)
    session.add(user_2)
    session.commit()
    return user_2


@pytest.fixture(scope="class")
def user_3_data():
    with open("./fixtures/test_users.json", "r+") as fp:
        data = json.loads(fp.read())
        user_3_data = data["test_user_3"]
        return user_3_data


@pytest.fixture(scope="class")
def test_user_3(session, user_3_data):
    user_3 = User(**user_3_data)
    session.add(user_3)
    session.commit()
    return user_3


@pytest.fixture(scope="class")
def user_4_data():
    with open("./fixtures/test_users.json", "r+") as fp:
        data = json.loads(fp.read())
        user_4_data = data["test_user_4"]
        return user_4_data


@pytest.fixture(scope="class")
def test_user_4(session, user_4_data):
    user_4 = User(**user_4_data)
    session.add(user_4)
    session.commit()
    return user_4


@pytest.fixture(scope="class")
def user_5_data():
    with open("./fixtures/test_users.json", "r+") as fp:
        data = json.loads(fp.read())
        user_5_data = data["test_user_5"]
        return user_5_data


@pytest.fixture(scope="class")
def test_user_5(session, user_5_data):
    user_5 = User(**user_5_data)
    session.add(user_5)
    session.commit()
    return user_5


# JobSeekers
@dataclass
class JobSeekerData:
    user_id: str
    #TODO: flesh this out.

@pytest.fixture(scope="class")
def get_job_seeker_data(index: int) -> JobSeekerData:
    with open("./fixtures/test_job_seekers.json", "r+") as fp:
        data = json.loads(fp.read())
        job_seeker_data = data[f"test_job_seeker_{str(index)}"]
        return job_seeker_data

@pytest.fixture(scope="class")
def test_job_seeker_1(session, user_1_data):
    job_seeker_1_data = get_job_seeker_data(1)

    """ 
    test_user_1,
    test_profile_1,
    test_skills_1,2,3,
    test_resume_1,
    test_education_1,2,
    test_work_experience_1,2,3 
    """
    pass


@pytest.fixture(scope="class")
def job_seeker_2_data():
    with open("./fixtures/test_job_seekers.json", "r+") as fp:
        data = json.loads(fp.read())
        job_seeker_2_data = data["test_job_seeker_2"]
        return job_seeker_2_data


@pytest.fixture(scope="class")
def test_job_seeker_2(session, user_2_data, job_seeker_2_data):
    pass


@pytest.fixture(scope="class")
def job_seeker_3_data():
    with open("./fixtures/test_job_seekers.json", "r+") as fp:
        data = json.loads(fp.read())
        job_seeker_3_data = data["test_job_seeker_3"]
        return job_seeker_3_data


@pytest.fixture(scope="class")
def test_job_seeker_3(session, user_3_data, job_seeker_3_data):
    pass


@pytest.fixture(scope="class")
def job_seeker_4_data():
    with open("./fixtures/test_job_seekers.json", "r+") as fp:
        data = json.loads(fp.read())
        job_seeker_4_data = data["test_job_seeker_4"]
        return job_seeker_4_data


@pytest.fixture(scope="class")
def test_job_seeker_4(session, user_4_data, job_seeker_4_data):
    pass


@pytest.fixture(scope="class")
def job_seeker_5_data():
    with open("./fixtures/test_job_seekers.json", "r+") as fp:
        data = json.loads(fp.read())
        job_seeker_5_data = data["test_job_seeker_5"]
        return job_seeker_5_data


@pytest.fixture(scope="class")
def test_job_seeker_5(session, user_5_data) -> JobSeeker:
    job_seeker_5_data = get_job_seeker_data(5)
    test_job_seeker_5 = JobSeeker(**user_5_data, **job_seeker_5_data)


# Profiles
@dataclass
class ProfileData:
    user_id: str
    interests: list[str]
    co_size_preference: list[str]
    preferred_industries: list[str]


def get_profile_data(index: int) -> ProfileData:
    with open("./fixtures/test_profiles.json", "r+") as fp:
        data = json.loads(fp.read())
        profile_data = data.get(f"test_profile_{str(index)}")
        return profile_data


@pytest.fixture(scope="class")
def test_profile_1(session, test_job_seeker_1) -> Profile:
    profile_1_data = get_profile_data(1)
    test_profile_1 = Profile(
        user_id=test_job_seeker_1.id,
        interests=profile_1_data.interests,
        co_size_preference=profile_1_data.co_size_preference,
        preferred_industries=profile_1_data.preferred_industries,
    )
    session.add(test_profile_1)
    session.commit()
    return test_profile_1


@pytest.fixture(scope="class")
def test_profile_2(session, test_job_seeker_2) -> Profile:
    profile_2_data = get_profile_data(2)
    test_profile_2 = Profile(
        user_id=test_job_seeker_2.id,
        interests=profile_2_data.interests,
        co_size_preference=profile_2_data.co_size_preference,
        preferred_industries=profile_2_data.preferred_industries,
    )
    session.add(test_profile_2)
    session.commit()
    return test_profile_2


@pytest.fixture(scope="class")
def test_profile_3(session, test_job_seeker_3) -> Profile:
    profile_3_data = get_profile_data(3)
    test_profile_3 = Profile(
        user_id=test_job_seeker_3.id,
        interests=profile_3_data.interests,
        co_size_preference=profile_3_data.co_size_preference,
        preferred_industries=profile_3_data.preferred_industries,
    )
    session.add(test_profile_3)
    session.commit()
    return test_profile_3


@pytest.fixture(scope="class")
def test_profile_4(session, test_job_seeker_4) -> Profile:
    profile_4_data = get_profile_data(4)
    test_profile_4 = Profile(
        user_id=test_job_seeker_4.id,
        interests=profile_4_data.interests,
        co_size_preference=profile_4_data.co_size_preference,
        preferred_industries=profile_4_data.preferred_industries,
    )
    session.add(test_profile_4)
    session.commit()
    return test_profile_4


@pytest.fixture(scope="class")
def test_profile_5(session, test_job_seeker_5) -> Profile:
    profile_5_data = get_profile_data(5)
    test_profile_5 = Profile(
        user_id=test_job_seeker_5.id,
        interests=profile_5_data.interests,
        co_size_preference=profile_5_data.co_size_preference,
        preferred_industries=profile_5_data.preferred_industries,
    )
    session.add(test_profile_5)
    session.commit()
    return test_profile_5
