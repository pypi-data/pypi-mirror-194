import pytest

from hmd_lang_deployment.change_set import ChangeSet
from hmd_lang_deployment.deployment_set import DeploymentSet


def test_change_set():

    ChangeSet(
        name="abc",
        definition=[
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "config_spec": "name@version:type:file_spec",
            },
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "instance_configuration": {"hi": "there"},
                "dependencies": {"a": "B", "c": "d", "e": ["a", "b"]},
            },
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "image_only": True,
            },
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "auto_deploy": "true",
                "config_spec": "name@version:type:file_spec",
            },
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "auto_deploy": "true",
                "instance_configuration": {"hi": "there"},
                "dependencies": {"a": "B", "c": "d", "e": ["a", "b"]},
            },
            {
                "deployment_id": "abc",
                "repo_instance_name": "inst",
                "repo_class_name": "a_class",
                "repo_class_version": "1.2.3",
                "auto_deploy": "true",
                "image_only": True,
            },
        ],
    )

    with pytest.raises(ValueError, match='Invalid value for field "definition"'):
        ChangeSet(name="abc", definition=["a"])

    # fields from both setups...
    with pytest.raises(ValueError):
        ChangeSet(
            name="abc",
            definition=[
                {
                    "deployment_id": "abc",
                    "repo_instance_name": "inst",
                    "repo_class_name": "a_class",
                    "repo_class_version": "1.2.3",
                    "image_only": False,
                }
            ],
        )

    # fields from both setups...
    with pytest.raises(ValueError):
        ChangeSet(
            name="abc",
            definition=[
                {
                    "deployment_id": "abc",
                    "repo_instance_name": "inst",
                    "repo_class_name": "a_class",
                    "repo_class_version": "1.2.3",
                    "instance_configuration": {"hi": "there"},
                    "dependencies": {"a": "B", "c": "d"},
                    "config_spec": "name@version:type:file_spec",
                }
            ],
        )

    # missing field
    with pytest.raises(ValueError):
        ChangeSet(
            name="abc",
            definition=[
                {
                    "deployment_id": "abc",
                    "repo_instance_name": "inst",
                    "repo_class_version": "1.2.3",
                    "config_spec": "name@version:type:file_spec",
                }
            ],
        )

    # bad dependencies value
    with pytest.raises(ValueError):
        ChangeSet(
            name="abc",
            definition=[
                {
                    "deployment_id": "abc",
                    "repo_instance_name": "inst",
                    "repo_class_name": "a_class",
                    "repo_class_version": "1.2.3",
                    "instance_configuration": {"hi": "there"},
                    "dependencies": {"a": 5, "c": "d"},
                }
            ],
        )


def test_deployment_set():

    DeploymentSet(
        name="dev",
        definition=[
            {
                "environment": "dev",
                "deployment_gate": {"transforms": [], "approval": False},
            },
            {
                "environment": "test",
                "deployment_gate": {
                    "transforms": [
                        {
                            "apply_to": ".*",
                            "transform": {"image_name": "abc", "tag": "def"},
                        },
                        {
                            "apply_to": "fi",
                            "transform": {"image_name": "abc", "tag": "def"},
                            "artifact_ref": "abc_def",
                        },
                    ],
                    "approval": True,
                },
            },
        ],
    )

    with pytest.raises(ValueError):
        DeploymentSet(
            name="dev",
            definition=[
                {
                    "environment": "test",
                    "deployment_gate": {
                        "transforms": [
                            {
                                "apply_to": ".*",
                                "transform": {"image_name": 5, "tag": "def"},
                            },
                            {
                                "apply_to": "fi",
                                "transform": {"image_name": "abc", "tag": "def"},
                                "artifact": {
                                    "artifact_name": "abc",
                                    "artifact_version": "def",
                                },
                            },
                        ],
                        "approval": True,
                    },
                }
            ],
        )

    with pytest.raises(ValueError):
        DeploymentSet(
            name="dev",
            definition=[
                {
                    "environment": "test",
                    "deployment_gate": {
                        "transforms": [
                            {
                                "apply_to": ".*",
                                "transform": {
                                    "image_name": 5,
                                    "tag": "def",
                                    "extra": "hi",
                                },
                            }
                        ],
                        "approval": True,
                    },
                }
            ],
        )

    with pytest.raises(ValueError):
        DeploymentSet(
            name="dev",
            definition=[
                {
                    "environment": "test",
                    "deployment_gate": {
                        "transforms": [
                            {
                                "apply_to": ".*",
                                "transform": {"image_name": "hi", "tag": "def"},
                            }
                        ]
                    },
                }
            ],
        )
