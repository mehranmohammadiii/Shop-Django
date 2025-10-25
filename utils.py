from kavenegar import *
def create_random_code(count):
    import random
    return random.randint(10**(count-1),10**count-1)

def send_sms(mobile,massage):
    pass

    # try:
    #     api = KavenegarAPI('31486952452B476175594437716F36736939425465386D353345504E44616C3945334665503451376155773D')
    #     params = {
    #         'sender': '',#optional
    #         'receptor': mobile,#multiple mobile number, split by comma
    #         'message': massage,
    #     } 
    #     response = api.sms_send(params)
    #     return response
    # except APIException as e: 
    #     print(e)
    # except HTTPException as e: 
    #     print(e)