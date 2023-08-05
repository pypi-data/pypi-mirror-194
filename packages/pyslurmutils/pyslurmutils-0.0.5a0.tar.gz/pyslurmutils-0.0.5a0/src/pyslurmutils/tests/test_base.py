import pytest
from ..client.errors import SlurmClientError


def test_version(slurm_base_api):
    assert slurm_base_api.server_has_api()


def test_wrong_job_wait(slurm_script_api):
    job_id = 0
    with pytest.raises(SlurmClientError):
        slurm_script_api.wait_done(job_id)


def test_wrong_job_print(slurm_script_api):
    job_id = 0
    slurm_script_api.print_stdout_stderr(job_id)


def test_wrong_job_clean(slurm_base_api):
    job_id = 0
    slurm_base_api.clean_job_artifacts(job_id)
