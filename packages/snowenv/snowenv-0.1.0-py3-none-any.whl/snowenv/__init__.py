import os
import jinja2
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from snowflake.connector import SnowflakeConnection
from ruamel.yaml import YAML
from .connector import connect


def connect_env(path: Optional[str] = None) -> SnowflakeConnection:
    """Connect to Snowflake using environment variables SNOWFLAKE_*.

    Args:
        path (str): Path to .env file to load. Defaults to None.

    Returns:
        SnowflakeConnection: Opened Snowflake connection.
    """

    if path:
        load_dotenv(path, override=True)

    return connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        private_key_path=os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH"),
        private_key_passphrase=os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def connect_dbt(
    profile: Optional[str] = None,
    target: Optional[str] = None,
    path: Optional[str] = str(Path.home() / ".dbt" / "profiles.yml"),
) -> SnowflakeConnection:
    """Connect to Snowflake using dbt profiles.

    Args:
        profile (str, optional): Profile name, optional if there's only one. Defaults to None.
        target (str, optional): Target name, optional if target field specified. Defaults to None.
        path (str, optional): Path to profiles.yml file. Defaults to ~/.dbt/profiles.yml.

    Returns:
        SnowflakeConnection: Opened Snowflake connection.
    """

    with open(str(path), mode="r", encoding="utf-8") as f:
        body_template = jinja2.Template(f.read())
        body_rendered = body_template.render(
            env_var=os.getenv,
        )

    yaml = YAML(typ="safe")
    profiles = yaml.load(body_rendered)

    if profile not in profiles:
        raise ValueError(f"No profile '{profile}' found in '{path}'")

    profile_dict = profiles.get(profile)
    profile_target = target or profile_dict.get("target")
    if not profile_target:
        raise ValueError("No target supplied or specified in profile")

    output = profile_dict.get("outputs", {}).get(profile_target)
    if not output:
        raise ValueError(f"No output for profile '{profile}' target '{profile_target}'")
    if output.get("type") != "snowflake":
        raise ValueError(f"Profile '{profile}' target '{profile_target}' not Snowflake")

    return connect(
        account=output.get("account"),
        user=output.get("user"),
        password=output.get("password"),
        private_key_path=output.get("private_key_path"),
        private_key_passphrase=output.get("private_key_passphrase"),
        role=output.get("role"),
        database=output.get("database"),
        warehouse=output.get("warehouse"),
        schema=output.get("schema"),
    )
