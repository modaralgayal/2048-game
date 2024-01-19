from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/main.py")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")