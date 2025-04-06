from unittest.mock import patch, MagicMock
from app.services.cloudinary_service import upload_avatar


@patch("cloudinary.uploader.upload")
def test_upload_avatar_success(mock_upload):
    # Мок успішного завантаження
    mock_upload.return_value = {"secure_url": "https://example.com/avatar.jpg"}

    # Мок файлу
    mock_file = MagicMock()
    mock_file.file = "mock_file_content"

    result = upload_avatar(mock_file)

    # Перевірка результату
    assert result == "https://example.com/avatar.jpg"
    mock_upload.assert_called_once_with("mock_file_content", folder="avatars")


@patch("cloudinary.uploader.upload")
def test_upload_avatar_failure(mock_upload):
    # Мок помилки завантаження
    mock_upload.side_effect = Exception("Upload failed")

    # Мок файлу
    mock_file = MagicMock()
    mock_file.file = "mock_file_content"

    try:
        upload_avatar(mock_file)
    except RuntimeError as e:
        assert str(e) == "Failed to upload avatar to Cloudinary."
    mock_upload.assert_called_once_with("mock_file_content", folder="avatars")
