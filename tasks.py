import time

from invoke import task


def wait_port_is_open(host, port):
    import socket
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return
        time.sleep(1)

@task
def reset_db(ctx):
    wait_port_is_open('db', 5432)
    ctx.run('pip install -r requirements.txt')

@task
def run_dev(ctx):
    reset_db(ctx)
    ctx.run('python manage.py runserver 0.0.0.0:8000')