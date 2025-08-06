#!/usr/bin/env python3
"""
Flask application runner script.
"""
import click
from app import app


@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, default=True, help='Enable debug mode')
def runserver(host, port, debug):
    """Run the development server."""
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    runserver() 