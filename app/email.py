
from threading import Thread

import requests

from flask import current_app, render_template
from flask_mail import Message

from . import mail


def send_async_email(app, msg):
    """Envia e-mail pelo SMTP em segundo plano."""
    with app.app_context():
        mail.send(msg)


def send_email_zoho(to, subject, template, **kwargs):
    """Envia e-mail utilizando o SMTP do Zoho."""
    app = current_app._get_current_object()

    msg = Message(
        subject=(
            app.config['FLASKY_MAIL_SUBJECT_PREFIX']
            + ' ' + subject
        ),
        sender=app.config['FLASKY_MAIL_SENDER'],
        recipients=[to]
    )

    msg.html = render_template(
        template + '.html',
        **kwargs
    )

    thread = Thread(
        target=send_async_email,
        args=(app, msg)
    )

    thread.start()
    return thread


def send_email(to, subject, template, **kwargs):
    """Envia e-mail utilizando a API do Mailgun."""

    app = current_app._get_current_object()

    api_url = app.config.get('API_URL')
    api_key = app.config.get('API_KEY')
    api_from = app.config.get('API_FROM')

    if not api_url or not api_key or not api_from:
        raise RuntimeError(
            'Configurações do Mailgun incompletas. '
            'Verifique API_URL, API_KEY e API_FROM.'
        )

    html = render_template(
        template + '.html',
        **kwargs
    )

    try:
        resposta = requests.post(
            api_url,
            auth=('api', api_key),
            data={
                'from': api_from,
                'to': to,
                'subject': (
                    app.config['FLASKY_MAIL_SUBJECT_PREFIX']
                    + ' ' + subject
                ),
                'html': html
            },
            timeout=30
        )
        if resposta.status_code != 200:
            print("STATUS MAILGUN:", resposta.status_code)
            print("DETALHE MAILGUN:", resposta.text)

        resposta.raise_for_status()

        return resposta

    except requests.exceptions.Timeout:
        app.logger.error(
            'Tempo limite excedido ao acessar o Mailgun.'
        )
        raise

    except requests.exceptions.ConnectionError:
        app.logger.error(
            'Erro de conexão com a API do Mailgun.'
        )
        raise

    except requests.exceptions.RequestException:
        app.logger.exception(
            'Erro na comunicação com o Mailgun.'
        )
        raise
