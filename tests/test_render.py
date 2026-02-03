"""Tests for render module."""
from mazegen.generator import generate_maze
from mazegen.render import (
    render_ascii, render_ascii_compact, render_mlx, render_mlx_detailed
)


def test_render_ascii() -> None:
    """Test ASCII rendering."""
    maze = generate_maze(3, 3, algorithm='prim', seed=42)
    output = render_ascii(maze)

    # Check that output contains expected characters
    assert '+' in output
    assert '-' in output
    assert '|' in output
    assert '\n' in output

    # Check line count (4 lines per row + 1 top border)
    lines = output.split('\n')
    assert len(lines) == 3 * 2 + 1  # 2 lines per row + top border


def test_render_ascii_compact() -> None:
    """Test compact ASCII rendering."""
    maze = generate_maze(3, 3, algorithm='prim', seed=42)
    output = render_ascii_compact(maze)

    # Check that output contains box drawing characters
    assert '┌' in output or '└' in output or '│' in output
    assert '\n' in output

    lines = output.split('\n')
    assert len(lines) > 0


def test_render_mlx() -> None:
    """Test MLX rendering."""
    maze = generate_maze(3, 3, algorithm='prim', seed=42)
    output = render_mlx(maze)

    # Check that output contains hex characters
    lines = output.split('\n')
    assert len(lines) == 3

    for line in lines:
        cells = line.split()
        assert len(cells) == 3
        # Each cell should be a hex digit
        for cell in cells:
            assert all(c in '0123456789ABCDEF' for c in cell)


def test_render_mlx_detailed() -> None:
    """Test detailed MLX rendering."""
    maze = generate_maze(3, 3, algorithm='prim', seed=42)
    output = render_mlx_detailed(maze)

    # Check for header comments
    assert '# Maze dimensions' in output
    assert '# Wall encoding' in output

    lines = output.split('\n')
    # Should have header lines + data lines
    assert len(lines) > 3


def test_render_consistency() -> None:
    """Test that same maze renders consistently."""
    maze = generate_maze(5, 5, algorithm='prim', seed=42)

    output1 = render_ascii(maze)
    output2 = render_ascii(maze)
    assert output1 == output2

    output1 = render_mlx(maze)
    output2 = render_mlx(maze)
    assert output1 == output2
