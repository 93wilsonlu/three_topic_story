from three_topic_story import app, db
import click


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
