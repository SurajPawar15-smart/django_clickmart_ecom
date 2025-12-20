from django.core.mail import send_mail
from django.conf import settings


def send_order_notification(order):
    user_name = order.user.first_name or "Customer"

    subject = f"Order #{order.id} Received Successfully"

    message = f"""
Hi {user_name},

Your order #{order.id} has been placed successfully.

Order Summary:
- Subtotal: {order.subtotal}
- Tax: {order.tax_amount}
- Total: {order.grand_total}

Thank you for shopping with us!
"""

    html_message = f"""
    <html>
        <body>
            <h2>Thank you for your order, {user_name}!</h2>
            <p>Your order <strong>#{order.id}</strong> has been placed successfully.</p>
            <hr>
            <p><strong>Order Summary</strong></p>
            <ul>
                <li>Subtotal: ₹{order.subtotal}</li>
                <li>Tax: ₹{order.tax_amount}</li>
                <li><strong>Total: ₹{order.grand_total}</strong></li>
            </ul>
            <p>We appreciate your business 🙏</p>
        </body>
    </html>
    """

    send_mail(
        subject=subject,
        message=message.strip(),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        html_message=html_message,
        fail_silently=False,
    )
