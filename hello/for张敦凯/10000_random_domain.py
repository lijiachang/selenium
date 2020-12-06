import random
import string


dummy_domain_lst = ['www.' + ''.join(random.sample(string.ascii_letters.lower() + string.digits, 5)) + '.test.com' for _ in range(10000)]

print(dummy_domain_lst)