import paramiko

class SSHClient():
    """SSH 连接类"""
    
    def __init__(self, ip, username, password, port=22):
        """
        初始化 SSH 连接
        
        Args:
            ip: 远程主机 IP 地址
            username: 用户名
            password: 密码
            port: SSH 端口，默认 22
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def shell_cmd(self, cmd):
        """远程执行 shell 命令
            
        Args:
            cmd: 要执行的命令
                
        Returns:
            命令执行结果列表，失败返回 False
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode('utf-8')
            result = result.split('\n')
            ssh.close()
            return result
        except Exception as e:
            print(f"远程执行 shell 命令失败！！！！，失败原因：{e}")
            return False

    def shell_upload(self, local_path, remote_path):
        """远程上传文件
            
        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径
                
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            transport = paramiko.Transport((self.ip, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            if sftp:
                sftp.put(local_path, remote_path)
                sftp.close()
            transport.close()
            print(f"文件上传成功：{local_path} -> {remote_path}")
            return True
        except Exception as e:
            print(f"文件上传失败！！！！，失败原因：{e}")
            return False

    def shell_download(self, remote_path, local_path):
        """远程下载文件
            
        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径
                
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            transport = paramiko.Transport((self.ip, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            if sftp:
                sftp.get(remote_path, local_path)
                sftp.close()
            transport.close()
            print(f"文件下载成功：{remote_path} -> {local_path}")
            return True
        except Exception as e:
            print(f"文件下载失败！！！！，失败原因：{e}")
            return False

    # def shell_cmd_result(self, cmd):
    #     """远程执行shell命令并返回结果"""
    #     try:
    #         ssh = paramiko.SSHClient()
    #         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
    #         stdin, stdout, stderr = ssh.exec_command(cmd)
    #         result = stdout.read().decode('utf-8')
    #         ssh.close()
    #         return result
    #     except Exception as e:
    #         print(f"远程执行shell命令失败！！！！，失败原因: {e}")
    #         return False

