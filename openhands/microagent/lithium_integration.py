"""
Lithium Framework Integration for OpenHands
Provides seamless integration with Lithium microagents and agent SDK
"""

import os
from pathlib import Path
from typing import Any

import yaml


def load_lithium_microagents(microagents_dir: str) -> list[dict[str, Any]]:
    """Load Lithium microagents from directory"""
    microagents: list[dict[str, Any]] = []
    microagents_path = Path(microagents_dir)

    if not microagents_path.exists():
        return microagents

    for ma_file in microagents_path.glob('*.md'):
        with open(ma_file, 'r') as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    microagent_content = parts[2].strip()

                    microagent = {
                        'name': frontmatter.get('name', ma_file.stem),
                        'type': frontmatter.get('type', 'microagent'),
                        'triggers': frontmatter.get('triggers', []),
                        'content': microagent_content,
                        'file': str(ma_file),
                    }
                    microagents.append(microagent)
                except yaml.YAMLError:
                    continue

    return microagents


def get_lithium_config() -> dict[str, Any]:
    """Get Lithium framework configuration"""
    config = {}

    # Load from environment variables
    config['project_root'] = os.getenv('LITHIUM_PROJECT_ROOT', '.')
    config['build_dir'] = os.getenv('LITHIUM_BUILD_DIR', '.build')
    config['openhands_dir'] = os.getenv('LITHIUM_OPENHANDS_DIR', '.openhands')
    config['microagents_dir'] = os.getenv(
        'LITHIUM_MICROAGENTS_DIR', '.openhands/microagents'
    )
    config['sdk_dir'] = os.getenv('LITHIUM_SDK_DIR', '.build/sdk')

    return config


def is_lithium_enabled() -> bool:
    """Check if Lithium framework is enabled"""
    return os.getenv('LITHIUM_PROJECT_ROOT') is not None
