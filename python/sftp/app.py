#/usr/bin/env python
import paramiko

if __name__ == '__main__':
    tport = paramiko.Transport(('test.rebex.net',2222))
    tport.connect(username='demo',password='password')

    sftp = paramiko.SFTPClient.from_transport(tport)
    sftp.get('readme.txt','readme.txt')
    sftp.close()

    tport.close()
