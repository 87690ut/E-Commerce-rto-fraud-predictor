import pandas as pd
import random

data = []
for _ in range(50000):
    order_value = random.randint(500, 50000)
    city_tier = random.choice(['Rural', 'Urban', 'Metro City'])
    payment_type = random.choice(['COD', 'COD', 'Credit Card', 'Debit Card', 'UPI', 'Net Banking'])
    return_count = random.randint(0,10)
    is_verified_mobile = random.choice([True, False])

    is_rto = 0
    