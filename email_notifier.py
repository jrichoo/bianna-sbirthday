"""
Email Notification System for Birthday Party RSVPs
Sends email notifications when someone fills up the RSVP form
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, email, password):
        """
        Initialize email notifier
        
        Args:
            smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
            smtp_port: SMTP port (e.g., 587 for TLS)
            email: Your email address
            password: Your email password or app-specific password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_rsvp_notification(self, rsvp_data, party_data):
        """
        Send email notification when someone RSVPs
        
        Args:
            rsvp_data: Dictionary containing RSVP information
            party_data: Dictionary containing party information
        """
        subject = f"🎉 New RSVP for {party_data['child_name']}'s Birthday Party!"
        
        # Create HTML email body
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f8f9fa;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        padding: 30px;
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #FF6B9D;
                        font-size: 28px;
                        margin-bottom: 10px;
                    }}
                    .info-box {{
                        background: #FFE5F0;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .info-row {{
                        margin-bottom: 10px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #666;
                    }}
                    .value {{
                        color: #333;
                    }}
                    .status {{
                        display: inline-block;
                        padding: 8px 15px;
                        border-radius: 20px;
                        color: white;
                        font-weight: bold;
                    }}
                    .status-yes {{
                        background: linear-gradient(135deg, #6BCB77, #4D96FF);
                    }}
                    .status-no {{
                        background: linear-gradient(135deg, #FF6B9D, #FF8FAB);
                    }}
                    .message-box {{
                        background: #E5F3FF;
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 20px;
                        font-style: italic;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        color: #999;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 New RSVP Received!</h1>
                        <p>Someone just responded to {party_data['child_name']}'s party invitation</p>
                    </div>
                    
                    <div class="info-box">
                        <div class="info-row">
                            <span class="label">👶 Child's Name:</span>
                            <span class="value">{rsvp_data['child_name']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">👨‍👩‍👧 Parent's Name:</span>
                            <span class="value">{rsvp_data['parent_name']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">📧 Email:</span>
                            <span class="value">{rsvp_data['email']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">📱 Phone:</span>
                            <span class="value">{rsvp_data['phone']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Status:</span>
                            <span class="status status-{rsvp_data['attendance_status']}">
                                {'✅ Coming!' if rsvp_data['attendance_status'] == 'yes' else '❌ Cannot Attend' if rsvp_data['attendance_status'] == 'no' else '❓ Maybe'}
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="label">👶 Number of Kids:</span>
                            <span class="value">{rsvp_data.get('number_of_kids', 1)}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">👨‍👩‍👧 Number of Adults:</span>
                            <span class="value">{rsvp_data.get('number_of_adults', 1)}</span>
                        </div>
                        {f'''
                        <div class="info-row">
                            <span class="label">🚫 Food Allergies:</span>
                            <span class="value">{rsvp_data.get('food_allergies', 'None')}</span>
                        </div>
                        ''' if rsvp_data.get('food_allergies') else ''}
                    </div>
                    
                    {f'''
                    <div class="message-box">
                        <strong>💌 Birthday Message:</strong><br>
                        "{rsvp_data.get('birthday_message', '')}"
                    </div>
                    ''' if rsvp_data.get('birthday_message') else ''}
                    
                    <div class="footer">
                        <p>RSVP received on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p>View all RSVPs in your admin dashboard</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send email
        self._send_email(self.email, subject, html_body)
    
    def send_confirmation_to_guest(self, rsvp_data, party_data):
        """
        Send confirmation email to the guest who submitted RSVP
        
        Args:
            rsvp_data: Dictionary containing RSVP information
            party_data: Dictionary containing party information
        """
        subject = f"🎉 RSVP Confirmation - {party_data['child_name']}'s Birthday Party"
        
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f8f9fa;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        padding: 30px;
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #FF6B9D;
                        font-size: 28px;
                    }}
                    .party-details {{
                        background: linear-gradient(135deg, #FFE5F0, #E5F3FF);
                        padding: 25px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .detail-row {{
                        margin-bottom: 12px;
                        font-size: 16px;
                    }}
                    .emoji {{
                        margin-right: 8px;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 2px solid #FFE5F0;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Thank You for Your RSVP! 🎉</h1>
                        <p>Hi {rsvp_data['parent_name']}!</p>
                    </div>
                    
                    <p>We're {'thrilled' if rsvp_data['attendance_status'] == 'yes' else 'sorry'} 
                    {'that you can join us' if rsvp_data['attendance_status'] == 'yes' else 'you cannot make it'} 
                    for {party_data['child_name']}'s {party_data['age']}th birthday party!</p>
                    
                    {f'''
                    <div class="party-details">
                        <h3 style="color: #FF6B9D; margin-bottom: 15px;">Party Details:</h3>
                        <div class="detail-row">
                            <span class="emoji">📅</span>
                            <strong>Date:</strong> {party_data['party_date']}
                        </div>
                        <div class="detail-row">
                            <span class="emoji">🕐</span>
                            <strong>Time:</strong> {party_data['party_time_start']} - {party_data['party_time_end']}
                        </div>
                        <div class="detail-row">
                            <span class="emoji">📍</span>
                            <strong>Location:</strong> {party_data['venue_name']}<br>
                            <span style="margin-left: 30px;">{party_data['venue_address']}</span>
                        </div>
                    </div>
                    ''' if rsvp_data['attendance_status'] == 'yes' else ''}
                    
                    <div class="footer">
                        <p>If you need to update your RSVP, please contact us.</p>
                        <p style="margin-top: 15px;">See you at the party! 🎈</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send confirmation to guest
        self._send_email(rsvp_data['email'], subject, html_body)
    
    def _send_email(self, to_email, subject, html_body):
        """
        Internal method to send email
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.email
            message['To'] = to_email
            message['Subject'] = subject
            
            # Attach HTML body
            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(message)
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


# Configuration examples for popular email providers
EMAIL_CONFIGS = {
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'note': 'Use App Password instead of regular password. Enable 2FA and create app password at: https://myaccount.google.com/apppasswords'
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587
    },
    'yahoo': {
        'smtp_server': 'smtp.mail.yahoo.com',
        'smtp_port': 587
    },
    'icloud': {
        'smtp_server': 'smtp.mail.me.com',
        'smtp_port': 587,
        'note': 'Use app-specific password from appleid.apple.com'
    }
}


# Example usage
if __name__ == '__main__':
    # Initialize email notifier (REPLACE WITH YOUR CREDENTIALS)
    notifier = EmailNotifier(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        email='your_email@gmail.com',  # Replace with your email
        password='your_app_password'    # Replace with your app password
    )
    
    # Example party data
    party_data = {
        'child_name': 'Emma',
        'age': 7,
        'party_date': 'December 25, 2026',
        'party_time_start': '3:00 PM',
        'party_time_end': '6:00 PM',
        'venue_name': 'Happy Kids Party Place',
        'venue_address': '123 Rainbow Street, Funtown, State 12345'
    }
    
    # Example RSVP data
    rsvp_data = {
        'child_name': 'Sarah',
        'parent_name': 'Jennifer Smith',
        'email': 'jennifer@email.com',
        'phone': '(555) 123-4567',
        'attendance_status': 'yes',
        'number_of_kids': 1,
        'number_of_adults': 2,
        'food_allergies': 'None',
        'birthday_message': 'Happy Birthday Emma! Can\'t wait to celebrate with you!'
    }
    
    # Send notifications
    notifier.send_rsvp_notification(rsvp_data, party_data)
    notifier.send_confirmation_to_guest(rsvp_data, party_data)
