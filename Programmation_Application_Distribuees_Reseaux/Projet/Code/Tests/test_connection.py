from Communication.Connection import Connection
from Communication.Client import Client
from unittest import mock
import socket
import builtins
from unittest.mock import patch
import threading
import sys


def test_client():
    client = Client()
    connection = Connection(client)
    assert connection.client == client


def test_input_ip():
    # verify that a good ip pass and return this IP
    with mock.patch.object(builtins, 'input', lambda _: "10.10.10.10"):
        assert Connection.input_ip() == "10.10.10.10"

    # verify that a bad string don't pass
    bad_list = ["1010.10.10", "10.10.10.10.10", "10.3000.10.10", "10.-10.10.10", "a.b.c.d",
                "2001:db8:3c4d:15:0:d234:3eee::"]
    test_value = None
    not_normal_counter = 0
    for i in bad_list:
        with mock.patch.object(builtins, 'input', lambda _: i):
            try:
                test_value = Connection.input_ip()
                not_normal_counter += 1
            except ValueError:
                pass
            # because it loops with no argument for input
            except RecursionError:
                pass
            finally:
                # verify that the first line of the try raised error each time
                assert not_normal_counter == 0
                # verify that test_value didn't get any value
                assert test_value is None
    with mock.patch.object(builtins, 'input', lambda _: "10.10.10.10"):
        good_ipv4 = Connection.input_ip()
        assert good_ipv4 == "10.10.10.10"


@patch.object(Client, "list_files")
@patch.object(Client, "select_file_to_download")
@patch.object(Client, "recv_file")
def test_manage_files(mock_recvf, mock_dl, mock_list):
    client = Client()
    connection = Connection(client)
    assert connection.manage_files("1") is True
    assert connection.manage_files("2") is True


@patch.object(Client, "create_network", side_effect=[None, socket.error])
@patch.object(Connection, "input_ip", side_effect=["10.10.10.10", KeyboardInterrupt])
@patch.object(Client, "join_network")
@patch.object(Client, "reach_to_peers")
def test_initialize(mock_reach, mock_join, mock_ip, mock_net):
    with mock.patch.object(builtins, 'input', side_effect=["h", "1"]):
        client = Client()
        connection = Connection(client)
        assert connection.initialize() is True
        mock_net.assert_called()

    with mock.patch.object(builtins, 'input', lambda _: "2"):
        client = Client()
        connection = Connection(client)
        assert connection.initialize() is True
        mock_ip.assert_called()
        mock_join.assert_called()
        mock_reach.assert_called()

    with mock.patch.object(builtins, 'input', lambda _: "q"):
        client = Client()
        connection = Connection(client)
        assert connection.initialize() is False

    # cette fois, "1" va renvoyer false car create_network renvoie une socket.error grâce au décorateur
    with mock.patch.object(builtins, 'input', lambda _: "1"):
        client = Client()
        connection = Connection(client)
        assert connection.initialize() is False

    # Le test sur l'interruption clavier ne fonctionne pas
    # Ici, on relance l'entrée deux ce qui va relancer la méthode input_ip et donc entrer
    # dans le side_effect keyboard interrupt défini dans le décorrateur de input_ip
    with mock.patch.object(builtins, 'input', lambda _: "2"):
        assert connection.initialize() is False


@patch.object(Connection, "define_port", return_value=8000)
@patch.object(Connection, "initialize", return_value=True)
@patch.object(Connection, "manage_files", side_effect=[True, False, KeyboardInterrupt])
@patch.object(Connection, "input_ip", return_value="10.0.0.1")
@patch.object(Client, "merge_request", return_value=2)
@patch.object(Client, "send_merge", return_value=True)
@patch.object(Client, "disconnect")
@patch.object(sys, "exit")
def test_define_connection(mock_exit, mock_disconnect, mock_send_merge, mock_merge_request, mock_input_ip,
                           mock_manage_files, mock_init, mock_port):
    c1 = Client()
    c = Connection(c1)
    # c.define_connection()
    # Test 1: Test pour choix "1"

    with patch('builtins.input', side_effect=["a", "1", "q"]):
        c.define_connection()
        mock_manage_files.assert_called_with('1')

    # Test 2: Test pour choix "2"
    with patch('builtins.input', side_effect=["2", "q"]):
        c.define_connection()
        mock_manage_files.assert_called_with('2')

    # Test 3: Test pour choix "3"
    with patch('builtins.input', side_effect=["3", 8000, "q"]):
        c.define_connection()
        mock_input_ip.assert_called()
        mock_merge_request.assert_called_with("10.0.0.1", 8000)
        mock_send_merge.assert_called_with("10.0.0.1", 2, 8000)

    # Test 4: Test pour choix "4"
    with patch('builtins.input', return_value="4"):
        pass

    # Test 5: Test pour choix invalide
    with patch('builtins.input', return_value="q"):
        c.define_connection()
        mock_disconnect.assert_called()
        mock_exit.assert_called()


@patch.object(Connection, "define_port", side_effect=["9000", KeyboardInterrupt])
def test_define_port(mock_input):
    Connection.define_port()
    mock_input.assert_called()
