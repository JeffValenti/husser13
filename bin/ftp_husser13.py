#!/usr/bin/env python

from ftplib import error_perm, FTP
from pathlib import Path


def ftp_make_local_copy(host, remote_dir='/', local_dir='ftp'):
    '''Copy directory tree from ftp server to local disk.'''
    local_path = Path(local_dir).expanduser().resolve()
    print(f'copying from {host} to {local_path}')
    # local_path.mkdir(exist_ok=True)
    ftp = FTP(host)
    ftp.login()
    ftp_process_dir(ftp, Path(remote_dir), local_path)


def ftp_process_dir(ftp, remote_path, local_path):
    ftp.cwd(str(remote_path))

    # Create list of subdirectories. Copy normal files. Ignore links.
    subdir_names = []
    for fileinfo in ftp.mlsd():
        name, info = fileinfo
        if info['type'] == 'dir':
            subdir_names.append(name)
        elif info['type'] == 'file':
            remote_file = remote_path / name
            local_file = local_path / name
            if not local_file.is_file():
                print(f'{str(remote_file)[1:]}')
                with open(local_file, 'wb') as fp:
                    ftp.retrbinary(f'RETR {str(remote_file)}', fp.write)

    # Recursively process subdirectories.
    for subdir_name in subdir_names:
        remote_subdir = remote_path / subdir_name
        print(f'{str(remote_subdir)[1:]}')
        local_subdir = local_path / subdir_name
        local_subdir.mkdir(parents=True, exist_ok=True)
        ftp_process_dir(ftp, remote_subdir, local_subdir)

if __name__ == '__main__':
    ftp_make_local_copy('phoenix.astro.physik.uni-goettingen.de')
