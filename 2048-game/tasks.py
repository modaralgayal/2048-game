from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/main.py")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def test(ctx):
    ctx.run("python3 -m coverage run -m unittest")

@task
def report(ctx):
    ctx.run("python3 -m coverage report")

@task
def reporthtml(ctx):
    ctx.run("python3 -m coverage html")

