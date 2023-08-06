import logging
import os
import subprocess
import sys


def generate_ssh_key():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Prompt the user to enter their username and email addressæ
    sys.stdout.write('Enter your username: ')
    sys.stdout.flush()
    username = input()

    sys.stdout.write('Enter your email address: ')
    sys.stdout.flush()
    email = input()

    logger.info(f"Username: {username} and Email: {email}")
    # Set the path where you want to save the SSH key
    ssh_key_path = f'C:\\Users\\{username}\\.ssh\\id_rsa'

    # Check if an SSH key already exists at the specified path
    if os.path.exists(ssh_key_path):
        print('An SSH key already exists at the specified path. Aborting.')
        exit()

    # Generate a new SSH key
    command = ['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', email, '-f', ssh_key_path, '-N', '', '-q']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if the SSH key file exists
    if not os.path.exists(ssh_key_path):
        raise Exception(f'Failed to generate SSH key: {error.decode("utf-8")}')

    print('SSH key generated successfully')

    # Print the public key so you can copy it to your Github account
    with open(f'{ssh_key_path}.pub', 'r') as f:
        public_key = f.read()
        print(f'Public key:\n{public_key}')
        logger.info(f"Public key: {public_key} for {username}")
    # Saved in the path
    print(f"Saved in the path: {ssh_key_path} \n")
    # Use the same ssh-key for github and gitlab
    print(f"Use the same ssh-key for github and gitlab in {ssh_key_path} \n")
