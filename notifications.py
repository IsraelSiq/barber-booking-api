# notifications.py — Issue #7: NotificationService + stub
# Todas as notificações passam por aqui. Por enquanto usa console.log (print).
# Para integrar Mailgun/SendGrid real, substitua os métodos (_send_email) — Issue #8.

class NotificationService:
    """Serviço central de notificações. Stub via print."""

    def _send_email(self, to: str, subject: str, body: str):
        """Stub: imprime no console. Substituir por API real na issue #8."""
        print(f"[EMAIL] Para: {to} | Assunto: {subject}")
        print(f"  {body}")

    def send_welcome(self, email: str, nome: str):
        self._send_email(
            to=email,
            subject="Bem-vindo à Barbearia! 💈",
            body=f"Olá {nome}, seu cadastro foi realizado com sucesso!"
        )

    def send_password_reset_requested(self, email: str, nome: str, token: str):
        link = f"https://barber-booking.app/reset-password?token={token}"
        self._send_email(
            to=email,
            subject="Redefinição de senha solicitada",
            body=(
                f"Olá {nome},\n"
                f"Clique no link abaixo para redefinir sua senha (válido por 1h):\n"
                f"{link}\n\n"
                "Se não foi você, ignore este e-mail."
            )
        )

    def send_password_reset_done(self, email: str, nome: str):
        self._send_email(
            to=email,
            subject="Sua senha foi alterada",
            body=f"Olá {nome}, sua senha foi redefinida com sucesso. Se não foi você, entre em contato."
        )

    def send_forced_reset_by_admin(self, email: str, nome: str):
        self._send_email(
            to=email,
            subject="Sua senha foi redefinida pelo administrador",
            body=(
                f"Olá {nome},\n"
                "Sua senha foi redefinida pelo administrador. "
                "Por favor, crie uma nova senha no próximo acesso."
            )
        )

    def send_booking_cancelled_by_barber(self, email: str, nome: str, data_hora: str, motivo: str):
        self._send_email(
            to=email,
            subject="Seu agendamento foi cancelado",
            body=(
                f"Olá {nome},\n"
                f"Seu agendamento em {data_hora} foi cancelado pelo barbeiro.\n"
                f"Motivo: {motivo}\n"
                "Entre em contato para reagendar."
            )
        )


# Instância global — importe de qualquer lugar
notification_service = NotificationService()
