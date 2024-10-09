from app import current_user
def data_():
    data = {
    'payment':current_user.payment,
    'pay_data': current_user.do,
    'comp_name': current_user.comp,
    'email': current_user.username,
    'tarif': current_user.tarif
    }
    return data