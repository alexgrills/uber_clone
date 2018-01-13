import database_service


def notify():
    pass

def start_driving(email):
    database_service.set_to_driving(email)
    return True