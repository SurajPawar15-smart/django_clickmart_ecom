from django.core.mail import send_mail
from django.conf import settings

# def send_order_notification(order):
#     send_mail(
#         subject=f'Order #{order.id} is received',
#         message=f"""
#             Hi {order.user.first_name},

#             Your order #{order.id} has been placed successfully.

#             Total: {order.grand_total}

#             Thank you for shopping with us.
#         """,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[order.user.email],
#         fail_silently=False
#     )

def send_order_notification(order):
    """
    Sends a simple order confirmation email to the customer.
    Basic transactional email (using send_mail).
    """
    if not order.user.email:
        return  # Fail silently (common practice)

    subject = f"🧾 Order Confirmation - {order.id} is received"
    message = f"""
        Hello {order.user.first_name},\n\n
        Your order has been received successfully.\n\n
        Thank you for your order {order.id}.\n\n
        Total Amount: {order.grand_total} \n\n
        We appreciate your business!
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = [order.user.email]
    to = [order.user.email]

    send_mail(
        subject,
        message,
        from_email,
        to,
        fail_silently=False,
    )

# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings

# def send_order_notification(order):
#     subject = f"✅ Order #{order.id} Confirmed!"
#     from_email = settings.EMAIL_HOST_USER
#     to = [order.user.email]

#     text_content = f"""
#     Hi {order.user.first_name},

#     Your order #{order.id} has been placed successfully.
#     Total Amount: ₹{order.grand_total}

#     Thank you for shopping with us!
#     """

#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 background-color: #f4f6f8;
#                 padding: 20px;
#             }}
#             .container {{
#                 max-width: 600px;
#                 background-color: #ffffff;
#                 margin: auto;
#                 padding: 30px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#             }}
#             .header {{
#                 text-align: center;
#                 color: #2c3e50;
#             }}
#             .order-id {{
#                 font-size: 18px;
#                 color: #27ae60;
#                 font-weight: bold;
#             }}
#             .details {{
#                 margin-top: 20px;
#                 font-size: 16px;
#                 color: #333;
#             }}
#             .total {{
#                 font-size: 20px;
#                 color: #e67e22;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 margin-top: 30px;
#                 text-align: center;
#                 font-size: 14px;
#                 color: #888;
#             }}
#             .btn {{
#                 display: inline-block;
#                 margin-top: 20px;
#                 padding: 12px 20px;
#                 background-color: #3498db;
#                 color: white;
#                 text-decoration: none;
#                 border-radius: 6px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h2 class="header">🎉 Order Confirmed!</h2>

#             <p>Hello <strong>{order.user.first_name}</strong>,</p>

#             <p class="details">
#                 Thank you for your purchase! Your order
#                 <span class="order-id">#{order.id}</span>
#                 has been placed successfully.
#             </p>

#             <p class="total">
#                 💰 Total Amount: ₹{order.grand_total}
#             </p>

#             <a href="#" class="btn">View Order</a>

#             <div class="footer">
#                 <p>Thank you for shopping with us ❤️</p>
#                 <p>&copy; 2025 ClickMart</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """

#     email = EmailMultiAlternatives(subject, text_content, from_email, to)
#     email.attach_alternative(html_content, "text/html")
#     email.send()
