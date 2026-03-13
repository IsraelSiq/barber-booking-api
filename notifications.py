from datetime import datetime


class NotificationService:
    """
    Serviço de notificações. Por enquanto apenas loga no console (stub).
    Futuramente integrar com Mailgun/SendGrid (#8).
    """

    def sendWelcome(self, user):
        print(f"[NOTIF] Bem-vindo, {user.nome}! ({user.email}) — {datetime.now()}")

    def sendPasswordResetRequested(self, user, token: str):
        print(f"[NOTIF] Reset de senha solicitado para {user.email}. Token: {token} — {datetime.now()}")

    def sendPasswordChanged(self, user):
        print(f"[NOTIF] Senha alterada com sucesso para {user.email} — {datetime.now()}")

    def sendAppointmentCancelled(self, user, appointment):
        print(
            f"[NOTIF] Agendamento #{appointment.id} cancelado para {user.email} "
            f"(data: {appointment.data_hora}) — {datetime.now()}"
        )

    def sendAdminPasswordReset(self, user):
        print(
            f"[NOTIF] Sua senha foi redefinida pelo administrador. "
            f"Por favor, crie uma nova senha. ({user.email}) — {datetime.now()}"
        )


notification_service = NotificationService()
