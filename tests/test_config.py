"""Tests for config module."""
import pytest
import tempfile
import os
from mazegen.config import parse_config, validate_maze_config, ConfigError


def test_parse_simple_config() -> None:
    """Test parsing simple configuration."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("width=10\n")
        f.write("height=8\n")
        f.write("algorithm=prim\n")
        f.name_path = f.name

    try:
        config = parse_config(f.name_path)
        assert config['width'] == 10
        assert config['height'] == 8
        assert config['algorithm'] == 'prim'
    finally:
        os.unlink(f.name_path)


def test_parse_with_comments() -> None:
    """Test parsing with comments."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("# This is a comment\n")
        f.write("width=5\n")
        f.write("# Another comment\n")
        f.write("height=5\n")
        f.name_path = f.name

    try:
        config = parse_config(f.name_path)
        assert config['width'] == 5
        assert config['height'] == 5
    finally:
        os.unlink(f.name_path)


def test_parse_boolean_values() -> None:
    """Test parsing boolean values."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("width=5\n")
        f.write("height=5\n")
        f.write("perfect=true\n")
        f.write("debug=false\n")
        f.name_path = f.name

    try:
        config = parse_config(f.name_path)
        assert config['perfect'] is True
        assert config['debug'] is False
    finally:
        os.unlink(f.name_path)


def test_parse_quoted_strings() -> None:
    """Test parsing quoted strings."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("width=5\n")
        f.write("height=5\n")
        f.write('name="test maze"\n')
        f.write("output='output.txt'\n")
        f.name_path = f.name

    try:
        config = parse_config(f.name_path)
        assert config['name'] == "test maze"
        assert config['output'] == "output.txt"
    finally:
        os.unlink(f.name_path)


def test_parse_invalid_format() -> None:
    """Test parsing invalid format."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("width=5\n")
        f.write("invalid line without equals\n")
        f.name_path = f.name

    try:
        with pytest.raises(ConfigError):
            parse_config(f.name_path)
    finally:
        os.unlink(f.name_path)


def test_parse_missing_file() -> None:
    """Test parsing non-existent file."""
    with pytest.raises(FileNotFoundError):
        parse_config("/nonexistent/file.txt")


def test_validate_valid_config() -> None:
    """Test validating valid configuration."""
    config = {'width': 10, 'height': 8}
    validate_maze_config(config)
    assert config['algorithm'] == 'prim'  # default
    assert config['perfect'] is True  # default


def test_validate_missing_width() -> None:
    """Test validation with missing width."""
    config = {'height': 8}
    with pytest.raises(ConfigError, match="Missing required parameter: width"):
        validate_maze_config(config)


def test_validate_missing_height() -> None:
    """Test validation with missing height."""
    config = {'width': 10}
    with pytest.raises(ConfigError, match="Missing required parameter: height"):
        validate_maze_config(config)


def test_validate_invalid_width() -> None:
    """Test validation with invalid width."""
    config = {'width': 1, 'height': 8}
    with pytest.raises(ConfigError, match="Invalid width"):
        validate_maze_config(config)


def test_validate_invalid_height() -> None:
    """Test validation with invalid height."""
    config = {'width': 10, 'height': 0}
    with pytest.raises(ConfigError, match="Invalid height"):
        validate_maze_config(config)


def test_validate_too_large() -> None:
    """Test validation with too large dimensions."""
    config = {'width': 20000, 'height': 8}
    with pytest.raises(ConfigError, match="Maze dimensions too large"):
        validate_maze_config(config)


def test_validate_invalid_algorithm() -> None:
    """Test validation with invalid algorithm."""
    config = {'width': 10, 'height': 8, 'algorithm': 'invalid'}
    with pytest.raises(ConfigError, match="Invalid algorithm"):
        validate_maze_config(config)
