from django.core.mail import send_mail, mail_admins


def send_order_message(email, order_id):
    #отправка уведомления о создании заказа покупателю и админу
    content = {'subject': 'order created',
               'message': f'order id {order_id} has been created',
               'from_email': None,
               'recipient_list': [email]}
    send_mail(**content)
    mail_admins(content['subject'], content['message'])


def false_positions(positions):
    #проверка количества товара при формировании заказа
    res = []
    for position in positions:
        if position.quantity > position.good.instock:
            print(position.quantity, position.good.instock)
            res.append(position.good.id)
    return res
