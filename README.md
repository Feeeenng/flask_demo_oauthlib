
这是自己基于实践操作完成的第三方登录

包括 QQ，新浪，微信 等


所用到的包:
python-weixin
flask-oauthlib


构建docker

docker built -t test_oauth .

运行一个docker

docker run -p 80:80 -d -it test_oauth 