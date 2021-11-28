import time
import hashlib
secret=input(" Enter Secret: ").strip()
matrix = list()
temp = list(secret)
row = list()
for i in range(0, len(temp), 2):
    temp2 = secret[i] + secret[i + 1]
    row.append(temp2)
    if (len(row) == 8):
        matrix.append(row)
        row = []
print(time.time())
otp = int(time.time())//100
print(int(time.time())%60)
row = (otp // 3) % 8
column = (otp // 5) % 8
otp = matrix[row][column] + str(otp)
print(otp)
otp = int(hashlib.sha512(otp.strip().encode('utf-8')).hexdigest(), 16) % 1000000
print(otp)
print(" OTP : ",otp)

