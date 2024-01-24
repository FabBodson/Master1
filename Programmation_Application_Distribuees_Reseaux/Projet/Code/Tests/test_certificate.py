from Communication import Certificate
from unittest.mock import patch
import os
import platform


@patch.object(platform, "system", side_effect=("Linux", "Windows", "Linux"))
@patch.object(os.path, "exists", side_effect=(False, True, os.error))
@patch.object(Certificate, "cleanup_mess")
@patch.object(os, "mkdir")
def test_create_cert_repo(mock_mkdir, mock_clean, mock_exist, mock_linux):
    Certificate.create_cert_repo()

    mock_linux.assert_called()
    mock_exist.assert_called()
    mock_mkdir.assert_called()

    Certificate.create_cert_repo()
    mock_clean.assert_called()
    
    try:
        Certificate.create_cert_repo()
    except os.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "Error while reading repository. Please check for permission error."
    

@patch.object(os.path, "exists", return_value=True)
@patch.object(os, "listdir", return_value=["file1.txt", "file2.txt"])
@patch.object(os.path, "isfile", side_effect=(True,False,True,True)) # les deux dernier c'est parce qu'il y a une appel récursif de la fonction cleanup_mess ...
@patch.object(os.path, "isdir", return_value=True)
@patch.object(os, "remove", return_value=True)
@patch.object(os, "rmdir", return_value=True)
def test_cleanup_mess(mock_rmdir, mock_remove, mock_isdir, mock_isfile, mock_listdir, mock_exist):
    Certificate.cleanup_mess("./cert")

    mock_exist.assert_called()
    mock_listdir.assert_called()
    mock_isfile.assert_called()
    mock_remove.assert_called()
    mock_rmdir.assert_called()
    mock_isdir.assert_called()

    #assert os.path.exists("./cert") is False
