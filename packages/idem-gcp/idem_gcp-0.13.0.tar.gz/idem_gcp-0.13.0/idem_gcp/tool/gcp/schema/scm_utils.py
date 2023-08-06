import os
import shutil
import subprocess
import tempfile


script_template = """
cd "{clone_dir}"
git clone "{repo_url}"
cd "{work_dir}"
git checkout --quiet {rev}
python -m venv venv
source "{work_dir}"/venv/bin/activate
pip uninstall -q -y --disable-pip-version-check --require-virtualenv idem-gcp
pip install -q --disable-pip-version-check --require-virtualenv -e .
idem doc states.gcp --output=json > "{out_file}"
"""


def fetch_schema(hub, repo_url: str, rev: str):
    tmp_dir = tempfile.mkdtemp()
    try:
        return _fetch_schema_for_rev(repo_url, rev, tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _fetch_schema_for_rev(repo_url: str, rev: str, clone_dir: str):
    # https://gitlab.com/vmware/idem/idem-gcp.git

    out_file = os.path.abspath(os.path.join(clone_dir, f"{rev}.json"))
    work_dir = os.path.join(clone_dir, os.path.splitext(os.path.basename(repo_url))[0])

    script_file = f"schema-{rev}.sh"
    command = ["/bin/bash", script_file]

    with open(os.path.join(clone_dir, script_file), "w") as f:
        script = script_template.format(
            **{
                "clone_dir": clone_dir,
                "repo_url": repo_url,
                "rev": rev,
                "out_file": out_file,
                "work_dir": work_dir,
            }
        )
        f.write(script)

    print(f"Fetching schema for commit/tag {rev}")

    ret = subprocess.run(
        command,
        cwd=clone_dir,
        capture_output=True,
    )

    if not ret or ret.returncode != 0:
        print(f"Error fetching schema: {str(ret.stderr, 'utf-8')}")
        return None

    with open(os.path.join(work_dir, out_file)) as f:
        result = f.read()

    if result:
        end_mark = result.rfind("}")
        if end_mark != -1:
            result = result[: end_mark + 1]

    return result
