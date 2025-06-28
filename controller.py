# controller.py
status = "ON"  # مقدار پیش‌فرض

def get_status():
    return status

def set_status(new_status):
    global status
    if new_status in ["ON", "OFF"]:
        status = new_status
        return True
    return False
