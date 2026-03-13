import os
from datetime import datetime
import resend

resend.api_key = os.environ.get("RESEND_API_KEY", "")

FROM_EMAIL = "Barber Booking <onboarding@resend.dev>"


class NotificationService:

    def _send(self, to: str, subject: str, html: str):
        if not resend.api_key:
            print(f"[NOTIF] RESEND_API_KEY não configurada. Email não enviado para {to}")
            return
        try:
            resend.Emails.send({
                "from": FROM_EMAIL,
                "to": [to],
                "subject": subject,
                "html": html,
            })
            print(f"[NOTIF] Email enviado para {to}: {subject}")
        except Exception as e:
            print(f"[NOTIF] Erro ao enviar email para {to}: {e}")

    def sendWelcome(self, user):
        self._send(
            to=user.email,
            subject="Bem-vindo ao Barber Booking! ✂️",
            html=f"""
            <div style="background:#0a0a0a;padding:40px;font-family:sans-serif;">
              <h1 style="color:#ffd600;">✂️ Barber Booking</h1>
              <p style="color:#fff;">Olá, <strong>{user.nome}</strong>!</p>
              <p style="color:#ccc;">Sua conta foi criada com sucesso. Agora você pode agendar seus cortes online!</p>
              <p style="color:#888;font-size:12px;">Barber Booking &copy; {datetime.now().year}</p>
            </div>
            """
        )

    def sendPasswordResetRequested(self, user, token: str):
        reset_url = f"{os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={token}"
        self._send(
            to=user.email,
            subject="Redefinição de senha - Barber Booking",
            html=f"""
            <div style="background:#0a0a0a;padding:40px;font-family:sans-serif;">
              <h1 style="color:#ffd600;">✂️ Barber Booking</h1>
              <p style="color:#fff;">Olá, <strong>{user.nome}</strong>!</p>
              <p style="color:#ccc;">Recebemos uma solicitação para redefinir sua senha.</p>
              <p style="margin:30px 0;">
                <a href="{reset_url}"
                   style="background:#ffd600;color:#000;padding:14px 28px;border-radius:8px;
                          text-decoration:none;font-weight:bold;font-size:16px;">
                  Redefinir minha senha
                </a>
              </p>
              <p style="color:#888;font-size:13px;">Este link expira em <strong>1 hora</strong>. Se você não solicitou, ignore este email.</p>
              <p style="color:#888;font-size:12px;">Barber Booking &copy; {datetime.now().year}</p>
            </div>
            """
        )

    def sendPasswordChanged(self, user):
        self._send(
            to=user.email,
            subject="Sua senha foi alterada - Barber Booking",
            html=f"""
            <div style="background:#0a0a0a;padding:40px;font-family:sans-serif;">
              <h1 style="color:#ffd600;">✂️ Barber Booking</h1>
              <p style="color:#fff;">Olá, <strong>{user.nome}</strong>!</p>
              <p style="color:#ccc;">Sua senha foi alterada com sucesso.</p>
              <p style="color:#888;font-size:13px;">Se você não realizou esta alteração, entre em contato imediatamente.</p>
              <p style="color:#888;font-size:12px;">Barber Booking &copy; {datetime.now().year}</p>
            </div>
            """
        )

    def sendAppointmentCancelled(self, user, appointment):
        self._send(
            to=user.email,
            subject="Seu agendamento foi cancelado - Barber Booking",
            html=f"""
            <div style="background:#0a0a0a;padding:40px;font-family:sans-serif;">
              <h1 style="color:#ffd600;">✂️ Barber Booking</h1>
              <p style="color:#fff;">Olá, <strong>{user.nome}</strong>!</p>
              <p style="color:#ccc;">Infelizmente seu agendamento do dia
                <strong style="color:#fff;">{appointment.data_hora.strftime('%d/%m/%Y às %H:%M')}</strong>
                foi cancelado pelo barbeiro.</p>
              <p style="color:#ccc;">Entre em contato para reagendar.</p>
              <p style="color:#888;font-size:12px;">Barber Booking &copy; {datetime.now().year}</p>
            </div>
            """
        )

    def sendAdminPasswordReset(self, user):
        self._send(
            to=user.email,
            subject="Sua senha foi redefinida pelo administrador - Barber Booking",
            html=f"""
            <div style="background:#0a0a0a;padding:40px;font-family:sans-serif;">
              <h1 style="color:#ffd600;">✂️ Barber Booking</h1>
              <p style="color:#fff;">Olá, <strong>{user.nome}</strong>!</p>
              <div style="background:#1a1a1a;border:1px solid #ffd600;border-radius:8px;padding:16px;margin:20px 0;">
                <p style="color:#ffd600;font-weight:bold;margin:0 0 8px;">⚠️ Ação necessária</p>
                <p style="color:#ccc;margin:0;">Sua senha foi redefinida pelo administrador. Por favor, crie uma nova senha no seu próximo login.</p>
              </div>
              <p style="color:#888;font-size:12px;">Barber Booking &copy; {datetime.now().year}</p>
            </div>
            """
        )


notification_service = NotificationService()
