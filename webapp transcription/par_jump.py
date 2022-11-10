import os
import time
import paramiko


def connection(host, port, user, key):
    # setting the ssh protocol connection
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect('"jumphost"', port, '"username"', key)
    jumpbox_transport = c.get_transport()
    src_addr = ("jump.fbk.eu", 22)
    dest_addr = (host, 22)
    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)
    target = paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.connect(host, port, user, key, sock=jumpbox_channel)
    print("connected")
    stdin, stdout, stderr = target.exec_command('"command"')
    print(stdout.readlines())
    stdin.close()
    stderr.close()
    return target


def SetDocker(ssh):
    # enter the docker container
    stdin, stdout, stderr = ssh.exec_command('"command"')
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
    stdin, stdout, stderr = ssh.exec_command('"command"')
    print(stdout.readlines())
    stdin.close()
    stderr.close()


def getFile(getRemotePath, getLocalPath, ssh, rem):
    # setting the sftp protocol to send back the transcript .txt file
    filepass = ssh.open_sftp()
    filepass.get(getRemotePath, getLocalPath, callback=None)
    filepass.close()
    stdin, stdout, stderr = ssh.exec_command('"command"'.format(rem))
    print(stdout.readlines())
    stdin.close()
    stderr.close()


def execDockCom(ssh, command, idDock):
    # execution of the command built in runTranscript func.

    string = "docker exec -it {A} {B}".format(A=idDock, B=command)
    print(string)
    stdin, stdout, stderr = ssh.exec_command(string, get_pty=True)
    output = stdout.readlines()
    print("output =", output)
    rtfx = output[len(output) - 2].split(":")[1]
    audiolen=output[len(output) - 3].split(":")[1]
    runtime = output[len(output) - 4].split(":")[1]
    latencies = output[len(output) - 5].split('\t\t')[1]
    rtfx = rtfx[0:len(rtfx)-2]
    runtime=runtime[0:len(rtfx)-2]


    print(rtfx, runtime, latencies)
    stdin, stdout, stderr = ssh.exec_command('"command"')
    print(stdout.readlines())
    stdin.close()
    stderr.close()
    return rtfx, runtime, latencies,audiolen


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
    putremoteFile = '"/path/"'.format(basename)
    getRemote = '"/path/resp.txt"'
    getLocal = '"/path/resp.txt"'

    hostname = '"host"'
    username = '"user"'
    port = 22
    k = paramiko.RSAKey.from_private_key_file("rsa keys")

    c = connection(hostname, port, username, k)
    SetDocker(c)
    putFile(path, putremoteFile, c)
    idD = getDockerId(c)
    command = "riva_asr_client --audio_file /riva/{} --output_filename=/riva/resp.txt".format(basename)
    exec = execDockCom(c, command, idD)
    getFile(getRemote, getLocal, c, basename)
    transcript = handleOut(getLocal)
    end = time.perf_counter()
    print(end - start)
    timer = end - start
    data = [transcript, timer, exec[0], exec[1], exec[2], exec[3]]
    print(data)
    return data
