from invoke import task


@task
def build(ctx):
    ctx.run("hatch build")


@task
def test(ctx):
    ctx.run("hatch run test:tests")
