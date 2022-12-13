from django.core.mail import send_mail, mail_admins


def send_order_message(email, order_id):
    """When an order created, this function send email to customer (to user email)
    and to admin (settings.ADMINS)"""
    content = {'subject': 'order created',
               'message': f'order id {order_id} has been created',
               'from_email': None,
               'recipient_list': [email]}
    send_mail(**content)
    mail_admins(content['subject'], content['message'])


def false_positions(positions):
    """It checks the quantity of the goods in the order and in_stock.
    Adds good to the list if the good is not enough.Return list"""
    res = []
    for position in positions:
        if position.quantity > position.good.instock:
            print(position.quantity, position.good.instock)
            res.append(position.good.id)
    return res
