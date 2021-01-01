import yaftp

yaftp.YAFTPServer(
    address=("127.0.0.1", 2121),
    local_dir="tests/server_data",
    auth={
        "USER": "PASSWORD",
        "OFEY": "404",
        "ANONYMOUS": ""   # Blank means login without password
    }
).serve()