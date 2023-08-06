from pathlib import Path

from invoke import task
from jinja2 import Template


@task(name="docs")
def documentation(c):
    """Build the documentation."""
    c.run("python3 -m sphinx docs docs/build/html")


@task
def test(c):
    """Run all tests under the tests directory."""
    c.run("python3 -m unittest discover tests 'test_*' -v")


@task(name="migrate")
def migrate_requirements(c):
    """Copy requirements from the requirements.txt file to pyproject.toml."""
    lines = Path("requirements.txt").read_text().split("\n")
    requirements = {"spendpoint": [], "test": [], "doc": [], "dev": []}
    current = "spendpoint"
    for line in lines:
        if line.startswith("#"):
            candidate = line[1:].lower().strip()
            if candidate in requirements.keys():
                current = candidate
                continue
        if line.strip() == "":
            continue
        requirements[current].append("".join(line.split()))
    template = Template(Path("docs/templates/pyproject.toml").read_text())
    Path("pyproject.toml").write_text(template.render(requirements=requirements))


@task
def release(c, version):
    """"""
    if version not in ["minor", "major", "patch"]:
        print("Version can be either major, minor or patch.")
        return

    from spendpoint import __version_info__, __version__
    _major, _minor, _patch = __version_info__

    if version == "patch":
        _patch = _patch + 1
    elif version == "minor":
        _minor = _minor + 1
        _patch = 0
    elif version == "major":
        _major = _major + 1
        _minor = 0
        _patch = 0

    c.run(f"git checkout -b release-{_major}.{_minor}.{_patch} dev")
    c.run(f"sed -i 's/{__version__}/{_major}.{_minor}.{_patch}/g' spendpoint/__init__.py")
    print(f"Update the readme for version {_major}.{_minor}.{_patch}.")
    input("Press enter when ready.")
    c.run(f"git add -u")
    c.run(f'git commit -m "Update changelog version {_major}.{_minor}.{_patch}"')
    c.run(f"git push --set-upstream origin release-{_major}.{_minor}.{_patch}")
    c.run(f"git checkout main")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f'git tag -a {_major}.{_minor}.{_patch} -m "Release {_major}.{_minor}.{_patch}"')
    c.run(f"git push")
    c.run(f"git checkout dev")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f"git push")
    c.run(f"git branch -d release-{_major}.{_minor}.{_patch}")
    c.run(f"git push origin --tags")
