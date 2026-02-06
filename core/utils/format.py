

def format_user_registration(data):
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Demande d'inscription reçue</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f9;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #10425D, #047bae);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .content h2 {{
                color: #2c5aa0;
                margin-bottom: 20px;
            }}
            .content p {{
                font-size: 16px;
                margin-bottom: 15px;
            }}
            .footer {{
                background-color: #34495e;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 KmrCare</h1>
                <p>Un Rendez-vous, une solution</p>
            </div>
            <div class="content">
                <h2>Demande d'inscription reçue</h2>
                <p>Bonjour {data['first_name']} {data['last_name']},</p>
                <p>Merci d'avoir soumis votre demande d'inscription. Nous l'examinerons dans les plus brefs délais.</p>
            </div>
            <div class="footer">
                Cet email est automatique, merci de ne pas y répondre.
            </div>
        </div>
    </body>
    </html>
    """.strip()


def format_registration_email(data):
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Nouvelle demande d'inscription</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f9;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #10425D, #047bae);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .content h2 {{
                color: #2c5aa0;
                margin-bottom: 20px;
            }}
            .content h3 {{
                color: #10425D;
                margin-top: 25px;
                margin-bottom: 10px;
            }}
            ul {{
                list-style: none;
                padding-left: 0;
            }}
            li {{
                padding: 5px 0;
                font-size: 14px;
            }}
            strong {{
                color: #2c5aa0;
            }}
            .footer {{
                background-color: #34495e;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 KmrCare</h1>
                <p>Un Rendez-vous, une solution</p>
            </div>
            <div class="content">
                <h2>📋 Nouvelle demande d'inscription</h2>
                <h3>👤 Utilisateur</h3>
                <ul>
                    <li><strong>Prénom :</strong> {data['first_name']}</li>
                    <li><strong>Nom :</strong> {data['last_name']}</li>
                    <li><strong>Email :</strong> {data['email']}</li>
                    <li><strong>Nom d'utilisateur :</strong> {data['username']}</li>
                </ul>
                <h3>🏥 Dispensaire</h3>
                <ul>
                    <li><strong>Nom :</strong> {data['dispensary_name']}</li>
                    <li><strong>Spécialités :</strong> {data['dispensary_specialities']}</li>
                    <li><strong>Quartier :</strong> {data['dispensary_quarter']}</li>
                    <li><strong>Localisation :</strong> {data['dispensary_localisation']}</li>
                    <li><strong>Téléphone :</strong> {data.get('dispensary_phone') or 'Non renseigné'}</li>
                    <li><strong>Email :</strong> {data.get('dispensary_email') or 'Non renseigné'}</li>
                    <li><strong>Horaires :</strong> {data['dispensary_opening']} - {data['dispensary_ending']}</li>
                </ul>
            </div>
            <div class="footer">
                Cet email est automatique, merci de ne pas y répondre.
            </div>
        </div>
    </body>
    </html>
    """.strip()


def format_registration_accepted():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Inscription acceptée</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f9;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #10425D, #047bae);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .content h2 {{
                color: #2c5aa0;
                margin-bottom: 20px;
            }}
            .content p {{
                font-size: 16px;
                margin-bottom: 15px;
            }}
            .footer {{
                background-color: #34495e;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 KmrCare</h1>
                <p>Un Rendez-vous, une solution</p>
            </div>
            <div class="content">
                <h2>✅ Votre demande d'inscription a été acceptée !</h2>
                <p>Vous pouvez maintenant vous connecter à votre compte.</p>
                <p>Merci de votre patience et à bientôt !</p>
            </div>
            <div class="footer">
                Cet email est automatique, merci de ne pas y répondre.
            </div>
        </div>
    </body>
    </html>
    """.strip()


def format_registration_rejected():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Inscription rejetée</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f9;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #10425D, #047bae);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .content h2 {{
                color: #2c5aa0;
                margin-bottom: 20px;
            }}
            .content p {{
                font-size: 16px;
                margin-bottom: 15px;
            }}
            .footer {{
                background-color: #34495e;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 KmrCare</h1>
                <p>Un Rendez-vous, une solution</p>
            </div>
            <div class="content">
                <h2>❌ Votre demande d'inscription a été rejetée</h2>
                <p>Nous sommes désolés, mais votre demande n'a pas été acceptée.</p>
                <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
            </div>
            <div class="footer">
                Cet email est automatique, merci de ne pas y répondre.
            </div>
        </div>
    </body>
    </html>
    """.strip()

    

def format_user_appointment_request(data):
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    border: 1px solid #ccc;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>📅 Demande de rendez-vous reçue</h2>
            <p>Bonjour {data['patient_name']},</p>
            <p>Votre demande de rendez-vous pour le <strong>{data['appointment_date']}</strong> à <b>{data['appointment_hour']}</b> a été reçue.</p>
            <p>Nous vous contacterons bientôt pour confirmer le statut de votre rendez-vous.</p>
        </body>
    </html>
    """.strip()
    
    
def format_appointment_request(data):
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    border: 1px solid #ccc;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>📅 Nouvelle demande de rendez-vous</h2>
            <p>Bonjour,</p>
            <p>Un nouveau rendez-vous a été demandé par <strong>{data['patient_name']}</strong>.</p>
            <ul>
                <li><strong>Date :</strong> {data['appointment_date']}</li>
                <li><strong>Heure :</strong> {data['appointment_hour']}</li>
                <li><strong>Raison :</strong> {data['reason']}</li>
            </ul>
        </body>
    </html>
    """.strip()
    
    
def format_appointment_confirmed(data):
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    border: 1px solid #ccc;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>✅ Votre rendez-vous a été confirmé !</h2>
            <p>Bonjour,</p>
            <p>Nous sommes heureux de vous informer que votre rendez-vous pour le <strong>{data['appointment_date']}</strong> à <b>{data['appointment_hour']}</b> a été confirmé avec succès.</p>
            <p>Merci de votre confiance. Nous vous attendons à l'heure convenue.</p>
        </body>
    </html>
    """.strip()

def format_appointment_rejected(data):
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    border: 1px solid #ccc;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>❌ Votre rendez-vous a été rejeté</h2>
            <p>Bonjour,</p>
            <p>Nous sommes désolés de vous informer que votre rendez-vous pour le <strong>{data['appointment_date']}</strong> à <b>{data['appointment_hour']}</b> a été rejeté.</p>
            <p>Si vous avez des questions ou souhaitez reprogrammer, n'hésitez pas à nous contacter.</p>
        </body>
    </html>
    """.strip()


def format_appointment_cancelled(data):
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    border: 1px solid #ccc;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>❌ Votre rendez-vous a été annulé</h2>
            <p>Bonjour,</p>
            <p>Nous vous informons que votre rendez-vous pour le <strong>{data['appointment_date']}</strong> à <b>{data['appointment_hour']}</b> a été annulé.</p>
            <p>Si vous avez des questions ou souhaitez reprogrammer, n'hésitez pas à nous contacter.</p>
        </body>
    </html>
    """.strip()