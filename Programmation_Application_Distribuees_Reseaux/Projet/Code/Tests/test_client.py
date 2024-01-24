from unittest.mock import Mock, MagicMock
from Communication import Client
from Communication import Certificate
from Communication.Exception import NoDataError
from unittest import mock
import socket
import builtins
import pytest
from unittest.mock import patch
import pickle
import os
import platform


def test_ip():
    client = Client.Client()
    ip = "10.10.10.10"
    client.ip = ip
    assert client.ip == "10.10.10.10"

'''
@patch.object(platform, "system", side_effect=("Linux","Windows","Linux","Linux"))
@patch.object(os.path, "exists", side_effect=(True, True, os.error, False))
@patch.object(os, "mkdir", return_value=True)
@patch.object(Certificate, "create_cert_repo")
def test_create_repo(mock_repo, mock_os, mock_exist, mock_sys):
    client = Client.Client()
    assert client.repository == "./DistribAppShare"
    #assert Client.create_repo() == "./DistribAppShare"
    # assert os.path.exists("./DistribAppShare")
    #with mock.patch.object(platform, "system", return_value=("Windows")):
    client2 = Client.Client()
    assert client2.repository == ".\\DistribAppShare"
        #assert Client.create_repo() == ".\\DistribAppShare"
    try:
        client3 = Client.Client()
    except os.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "Error while reading repository. Please check for permission error."
    client4 = Client.Client()
'''
@patch.object(platform, "system", return_value=("Linux"))
@patch.object(os.path, "exists", side_effect=(True, False, True, False, os.error, False, False, False, True, False, False, False)) # je mets un false entre chaque side effect car create_cert_repo est également appelé à la création d'un client
@patch.object(os, "mkdir", side_effect=(True,True,True,True,True,True, os.error, True))
@patch.object(os, "listdir", side_effect=[["test2"], []])
@patch.object(Client.Client, "get_network_files", side_effect=[["test3", "test1"], []])
@patch.object(Certificate, "create_cert_repo", return_value=True)
@patch.object(Certificate, "cleanup_mess", return_value=True)
def test_create_repo_and_list_file(mock_mess, mock_cert_repo, mock_net_list, mock_list, mock_os, mock_exists, mock_plat):
    client = Client.Client()
    assert client.repository == "./DistribAppShare"
    #assert Client.create_repo() == "./DistribAppShare"
    # assert os.path.exists("./DistribAppShare")
    with mock.patch.object(platform, "system", return_value=("Windows")):
        client = Client.Client()
        assert client.repository == ".\\DistribAppShare"
        #assert Client.create_repo() == ".\\DistribAppShare"
    try:
        client = Client.Client()
    except os.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "Error while reading repository. Please check for permission error."
    client = Client.Client()

    assert client.repository != ""
    assert client.repository is not None
    assert client.repository == "./DistribAppShare"
    client.list_files()
    assert len(client.repository_content) != 0
    assert len(client.repository_content) == 3
    assert client.repository_content[0] in ["test1", "test2", "test3"]
    assert client.repository_content[1] in ["test1", "test2", "test3"]
    assert client.repository_content[2] in ["test1", "test2", "test3"]

    # test pour rentrer dans le OS.error -> fonctionne pas
    try:
        client.list_files()
    except os.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "Error while reading repository. Please check for permission error."

    # test le "no element"
    client.list_files()


def test_add_peer():
    c1 = Client.Client()
    # create client
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10"]
    # Verify that i can add an user
    assert c1.add_peer("10.0.0.45") == (b"You are added to my peers list", ["10.10.10.10", "10.0.0.45"])
    # Verify that it can't has a duplicate
    assert c1.add_peer("10.0.0.45") == (b"You are already in the peers list", ["10.10.10.10", "10.0.0.45"])
    # Verify that it add to "peers" attribute
    assert c1.peers == ["10.10.10.10", "10.0.0.45"]


# Don't need to verify the format of the IP because when this method is call the IP come from the data of a socket
# connection so a good format


def test_create_socket():
    client = Client.Client()
    client.create_socket()
    assert client.socket.family == socket.AF_INET
    assert client.socket.type == socket.SOCK_STREAM
    assert client.socket is not None

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



@patch.object(Client.socket.socket, "accept", return_value=(s1, ("10.10.10.9", 8000)))
@patch.object(Client.socket.socket, "recv", side_effect=[str.encode(f"Join request 10.10.10.10 i listen on {7000}"), socket.error])
@patch.object(Client.socket.socket, "send")
def test_create_network(mock_send, mock_recv, mock_accept):
    c1 = Client.Client()
    c1.create_socket()
    try:
        c1.create_network()
        assert c1.peers == ["10.10.10.10:8000", "10.10.10.9:7000"]
        mock_send.assert_called_with(pickle.dumps(["10.10.10.10:8000", "10.10.10.9:7000"]))
    except socket.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "exception socket error"



@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
@patch.object(Client.socket.socket, "recv",
              side_effect=[str.encode("You are added to my peers list"), pickle.dumps(["10.10.10.10", "10.10.10.9"])])
def test_join_network(mock_recv, mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.create_socket()
    c1.ip = "127.0.0.1"
    with mock.patch.object(builtins, 'input', lambda _: "8000"):
        c1.join_network("10.10.10.10")

    mock_conn.assert_called_with(("10.10.10.10", 8000))
    mock_send.assert_called_with(str.encode(f"Join request 10.10.10.10 i listen on {8000}"))
    assert c1.ip == "10.10.10.9"
    assert c1.peers == ["10.10.10.9", "10.10.10.10"]


s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "accept", return_value=(s2, ("10.10.10.9", 8000)))
@patch.object(Client.socket.socket, "recv",
              side_effect=[str.encode("quelque_chose_pour_entrer_dans_le_else"), str.encode("Files request"), str.encode("Join request 10.10.10.10 i listen on 7000"), socket.error, str.encode("Disconnect"), NoDataError])
@patch.object(Client.socket.socket, "send")
@patch.object(Client.socket.socket, "bind")
@patch.object(os.path, "exists", return_value= True)
@patch.object(os, "mkdir")
@patch.object(os, "listdir", return_value=["test2"])
def test_answer_request(mock_list, mock_mkdir, mock_exists, mock_bind, mock_send, mock_recv, mock_accept, mock_sock):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10"]
    # test le 'continue', le list files, le join, et le socket.error
    try:
        c1.answer_request()
        mock_list.assert_called()
        assert c1.peers == ["10.10.10.10", "10.10.10.9:7000"]
        mock_send.assert_called_with(pickle.dumps(["10.10.10.10", "10.10.10.9:7000"]))

    except socket.error:
        with mock.patch.object(builtins, 'input') as mock_print:
            mock_print.assert_called_with("exception socket error")


    # test le disconnect et le no data error
    try:
        c1.answer_request()
    except NoDataError:
        with mock.patch.object(builtins, 'input') as mock_print:
            assert mock_print == "no data, connexion isn't alive anymore"



# s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
@patch.object(Client.socket.socket, "recv",
              side_effect=[str.encode("You are added to my peers list"), pickle.dumps(["10.10.10.10:8000", "10.10.10.9:8000"])])
def test_reach_to_peers(mock_recv, mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10:8000", "10.10.10.11:8000", "10.10.10.12:8000"]
    c1.reach_to_peers()



@patch.object(os, "listdir", return_value=["test2"])
@patch.object(Client.Client, "get_network_files", return_value=["test3", "test1"])
def test_select_file_to_download(mock_net_list, mock_list):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10", "10.10.10.11"]

    # Le premier vérifie la valueError, le second le else, et le troisième le if et le reste
    with mock.patch('builtins.input', side_effect=["a", "200", "3"]):
        try:
            file_to_dl = c1.select_file_to_download()
            assert c1.repository_content == ["test2", "test3", "test1"]
            assert file_to_dl == ["test1"]
        except ValueError:
            with mock.patch.object(builtins, 'input') as mock_print:
                assert mock_print == "Value error, Please enter a valid number."


@patch.object(Client.socket, "socket", side_effect=[socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                                                    socket.socket(socket.AF_INET, socket.SOCK_STREAM)])
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
@patch.object(Client.socket.socket, "recv",
              side_effect=[pickle.dumps(["test2", "test3", "test1"]), pickle.dumps(["test2", "test7", "test6"])])
def test_get_network_files(mock_recv, mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10:8000", "10.10.10.11:8000", "10.10.10.12:8000"]
    net_files = c1.get_network_files()
    assert net_files == ["test2", "test3", "test1", "test7", "test6"]


@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
def test_disconnect(mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10:8000", "10.10.10.11:8000"]
    c1.disconnect()

    mock_conn.assert_called_with(("10.10.10.11", 8000))
    mock_send.assert_called_with(str.encode("Disconnect"))


@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
def test_in_transfer(mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "192.168.24.23"
    c1.peers = ["192.168.24.23:8000", "192.168.24.24:8000", "192.168.24.25:8000", "192.168.24.26:8000"]
    assert c1.peers[1::] == ["192.168.24.24:8000", "192.168.24.25:8000", "192.168.24.26:8000"]
    c1.transfer_list = ["192.168.24.24", "192.168.24.25"]
    c1.in_transfer("in_transfer", "192.168.24.26")

    # on vérifie 192.168.24.26 car c'est le dernier de la boucle
    mock_conn.assert_called_with(("192.168.24.26", 8000))
    mock_send.assert_called_with(pickle.dumps(["in_transfer", "192.168.24.26"]))

    c1.in_transfer("not_in_transfer", "192.168.24.24")
    """

    mock_conn.assert_called_with(("192.168.24.24", 8000))
    mock_send.assert_called_with(pickle.dumps(["not_in_transfer", "192.168.24.24"]))
    mock_conn.assert_called_with(("192.168.24.25", 8000))
    mock_send.assert_called_with(pickle.dumps(["not_in_transfer", "192.168.24.24"]))
    """

    # on vérifie 192.168.24.26 car c'est le dernier de la boucle
    mock_conn.assert_called_with(("192.168.24.26", 8000))
    mock_send.assert_called_with(pickle.dumps(["not_in_transfer", "192.168.24.24"]))

    assert c1.transfer_list == ["192.168.24.25", "192.168.24.26"]

'''#comm
@patch.object(socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(socket.socket, "connect", return_value=-1)
@patch.object(socket.socket, "sendall")
@patch.object(builtins, "open")
def test_send_file(mock_open, mock_send, mock_conn, mock_sock):
    client = Client.Client()
    client.send_file("10.0.0.1", "testfile.txt")
    # Le contenu de DistribAppShare/testfile.txt est "Hello Wold!"
    mock_send.assert_called_with(str.encode("Hello Wold!"))
'''



'''#comm
@patch.object(socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(socket.socket, "accept")#, return_value=(s1, ("10.10.10.9", 8000)))
@patch.object(socket.socket, "bind")
@patch.object(socket.socket, "listen")
@patch.object(socket.socket, "send")
@patch.object(socket.socket, "recv", side_effect=[str.encode("a content from file to store in new file"), ""])
def test_recv_file(mock_recv, mock_send, mock_lis, mock_bind, mock_accept, mock_sock):
    client = Client.Client()
    client.ip = "10.0.0.1"
    client.recv_file(["un_fichier", "10.0.0.2"])
    mock_send.assert_called_with("ask un_fichier")
    mock_recv.assert_called_with(str.encode("a content from file to store in new file"))'''


''' #probb unicode decode
@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
@patch.object(Client.socket.socket, "recv", return_value=(pickle.dumps(["10.10.10.12:8000", "10.10.10.13:8000", "10.10.10.14:8000"])))
def test_merge_request(mock_recv, mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10:8000", "10.10.10.11:8000"]
    c1.merge_request("10.10.10.12",8000)

    mock_conn.assert_called_with(("10.10.10.12", 8000))
    mock_recv.assert_called_with(pickle.dumps(["10.10.10.12", "10.10.10.13", "10.10.10.14"]))
'''

@patch.object(Client.socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(Client.socket.socket, "connect", return_value=-1)
@patch.object(Client.socket.socket, "send")
def test_send_merge(mock_send, mock_conn, mock_socket):
    c1 = Client.Client()
    c1.ip = "10.10.10.10"
    c1.peers = ["10.10.10.10:8000", "10.10.10.11:8000"]

    assert c1.send_merge("10.10.10.12", 2, 8000)
    peers = ["10.10.10.10", "10.10.10.11"]
    for peer in peers[1:2]:
        mock_conn.assert_called_with((peer, 8000))
        #mock_send.assert_called_with(str.encode("New network with 10.10.10.12"))
        mock_send.assert_called_with(pickle.dumps(c1.peers))



@patch.object(socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(socket.socket, "connect", return_value=-1)
@patch.object(socket.socket, "sendall")
@patch.object(builtins, "open")
@patch.object(socket.socket, "close")
def test_send_cert(mock_close, mock_open, mock_sendall, mock_conn, mock_sock):
    client = Client.Client()
    client.send_cert("10.0.0.1", 10000)

    mock_sock.assert_called()
    mock_conn.assert_called_with(("10.0.0.1", 10000))
    mock_open.assert_called()
    #mock_sendall.assert_called()
    mock_close.assert_called()


@patch.object(socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(socket.socket, "accept", return_value=(s1, ("10.10.10.9", 10000)))
@patch.object(socket.socket, "bind")
@patch.object(socket.socket, "listen")
@patch.object(socket.socket, "recv", side_effect=[str.encode("a content from file to store in new file"), ""])
@patch.object(socket.socket, "close")
def test_recv_cert(mock_close, mock_recv, mock_lis, mock_bind, mock_accept, mock_sock):
    client = Client.Client()
    client.recv_cert("10.0.0.1", 10000)

    mock_sock.assert_called()
    mock_bind.assert_called()
    mock_lis.assert_called()
    mock_accept.assert_called()
    mock_recv.assert_called()
    mock_close.assert_called()


@patch.object(socket, "socket", return_value=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
@patch.object(socket.socket, "connect", return_value=-1)
@patch.object(socket.socket, "send")
@patch.object(socket.socket, "close")
def test_ask_for_cert(mock_close, mock_send, mock_conn, mock_sock):
    client = Client.Client()
    client.ask_for_cert("10.0.0.1", 10000, 's-cert')

    mock_sock.assert_called()
    mock_conn.assert_called_with(("10.0.0.1", 10000))
    mock_send.assert_called()
    mock_close.assert_called()

