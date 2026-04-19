import argparse
import os
from unittest.mock import MagicMock, patch

from ai_knowledge_assistant.cli import cmd_index


@patch("ai_knowledge_assistant.cli.save_chunks_vectors")
@patch("ai_knowledge_assistant.cli.EmbeddingBuilder")
@patch("ai_knowledge_assistant.cli.save_chunks")
@patch("ai_knowledge_assistant.cli.get_chunks_from_files", return_value=[MagicMock()])
@patch("ai_knowledge_assistant.cli.read_files", return_value={"f.txt": "hello"})
def test_cmd_index_creates_output_dir(
    mock_read, mock_chunks, mock_save, mock_emb_cls, mock_save_vec, tmp_path
):
    """Issue #9: cmd_index must create the output directory before saving."""
    index_file = str(tmp_path / "sub" / "index.json")
    vectors_file = str(tmp_path / "sub" / "vectors.json")

    mock_emb_instance = MagicMock()
    mock_emb_instance.build_vectors.return_value = []
    mock_emb_cls.return_value = mock_emb_instance

    args = argparse.Namespace(paths=["some/path"])

    with patch("ai_knowledge_assistant.cli.config") as mock_config:
        mock_config.INDEX_FILE = index_file
        mock_config.VECTORS_FILE = vectors_file
        mock_config.DEFAULT_EMBEDDING = MagicMock()

        result = cmd_index(args)

    assert result == 0
    assert os.path.isdir(str(tmp_path / "sub"))
