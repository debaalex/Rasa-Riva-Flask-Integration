import os
import time
import paramiko


def connection(host, port, user, key):
    # setting the ssh protocol connection
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect("jump.fbk.eu", port, "adebertolis", key)
    jumpbox_transport = c.get_transport()
    src_addr = ("jump.fbk.eu", 22)
    dest_addr = (host, 22)
    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)
    target = paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.connect(host, port, user, key, sock=jumpbox_channel)
    print("connected")
    stdin, stdout, stderr = target.exec_command("cd matasso/riva ; ls; rm rec.wav; rm resp.txt")
    print(stdout.readlines())
    stdin.close()
    stderr.close()
    return target


def SetDocker(ssh):
    # enter the docker container
    stdin, stdout, stderr = ssh.exec_command("cd matasso/riva/riva_quickstart_v1.10.0-beta ;"
                                             "bash riva_start.sh ; bash riva_start_client.sh ; cd")
    # docker run riva-client ( alternative command)
    print(stdout.readlines())
    print("docker up")
    stdin.close()


def getDockerId(ssh):
    # retrive the docker id to use it in CLI exec command
    stdin, stdout, stderr = ssh.exec_command('docker ps --filter "name=riva-client" --format "{{.ID}}"')
    idDock = stdout.read()
    count = len(idDock)
    print(idDock)
    return idDock[0:count - 1].decode("ascii")


def putFile(putLocalPath, putRemotePath, ssh):
    # handling the sftp protocol to pass a local file to the remote machine
    print(putLocalPath)
    filepass = ssh.open_sftp()
    if os.path.isfile(putLocalPath):
        filepass.put(putLocalPath, putRemotePath, callback=None, confirm=False)
        filepass.close()
    else:
        raise IOError('Could not find localFile %s !!' % putLocalPath)
    print("file transferred")
    stdin, stdout, stderr = ssh.exec_command("cd matasso/riva ; ls")
    print(stdout.readlines())
    stdin.close()
    stderr.close()


def getFile(getRemotePath, getLocalPath, ssh, rem):
    # setting the sftp protocol to send back the transcript .txt file
    filepass = ssh.open_sftp()
    filepass.get(getRemotePath, getLocalPath, callback=None)
    filepass.close()
    stdin, stdout, stderr = ssh.exec_command("cd matasso/riva ; ls; rm {}; rm resp.txt;".format(rem))
    print(stdout.readlines())
    stdin.close()
    stderr.close()


def execDockCom(ssh, command, idDock):
    # execution of the command built in runTranscript func.

    string = "docker exec -it {A} {B}".format(A=idDock, B=command)
    print(string)
    stdin, stdout, stderr = ssh.exec_command(string, get_pty=True)
    print(stdout.readlines())
    stdin, stdout, stderr = ssh.exec_command("cd matasso/riva; ls")
    print(stdout.readlines())
    stdin.close()
    stderr.close()


def handleOut(file):
    # formatting the textual transcript in a readable string
    with open(file) as f:
        contents = f.read()
        print(contents)
        trans = contents.split(":")
        stringa = trans[2]
        count = len(stringa)
        print(stringa)
        out = (stringa[2:count - 3])
        print(out)
        return out


def runTranscript(path):
    start = time.perf_counter()
    basename = os.path.basename(path)
    print(basename)
    putremoteFile = '/raid/home/stek/matasso/riva/{}'.format(basename)
    getRemote = '/raid/home/stek/matasso/riva/resp.txt'
    getLocal = '/Users/alexdebertolis/Downloads/resp.txt'

    hostname = "digis-precision79203.fbk.eu"
    username = "stek"
    port = 22
    k = paramiko.RSAKey.from_private_key_file("/Users/alexdebertolis/chiavi-ssh/id_rsa")

    c = connection(hostname, port, username, k)
    SetDocker(c)
    putFile(path, putremoteFile, c)
    idD = getDockerId(c)
    command = "riva_asr_client --audio_file /riva/{} --output_filename=/riva/resp.txt".format(basename)
    execDockCom(c, command, idD)
    getFile(getRemote, getLocal, c, basename)
    transcript = handleOut(getLocal)
    end = time.perf_counter()
    print(end - start)
    timer = end - start
    data = [transcript, timer]
    return data
