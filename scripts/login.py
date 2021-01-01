import yaftp

c = yaftp.YAFTP(
    address=("127.0.0.1", 2121),
    user="USER",
    passwd="PASSWORD"
)

c.login()


# DO STH
# c.quit()