def check_time_sync(user_val, correct_val):
    return int(user_val) == int(correct_val)

def check_sequence(user_op, user_val, correct_op, correct_val):
    return user_op == correct_op and int(user_val) == int(correct_val)

def check_inventory(user_val, correct_val):
    return int(user_val) == int(correct_val)
