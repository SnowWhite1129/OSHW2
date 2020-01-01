The decription of all scripts:

1. client.sh
	Usage: ./client.sh <User name of your client instance> <public ip of your client instance> <public key path of your client instance>
	Description:
		This script will copy "demo_client" directory to your client instance home directory and start your client instance. The "demo_client" 
		directory contains some sample videos (01.mp4 - 05.mp4), stream.py (program that sends videos to your server), demo.sh and demo_tmux.sh.

2. demo.sh
	Usage: ./demo.sh <server IP> <server port>
	Description:
		This script will start a tmux session that contains 5 panes. These 5 panes represent 5 clients that will run stream.py and send videos to your server.

3. accuracy.sh
	Usage: ./accuracy.sh <your student id> <path of your license plate detection results>
	Description:
		This script will create a directory named after your student id and create an "output" directory in it. 
		Also, it will copy "answer" directory to <student id> directory and move all of your license plate detection results(e.g. 01.txt, 02.txt, etc) 
		from the path you typed to <student id>/output. At last, it will compare answers we provided with your results and calculate accuracy.

4. send.sh
	Usage: ./send.sh <User name of your destination instance> <public ip of your destination instance> <public key path of your destination instance>
	Description:
		If your license plate detection results are not on your local machine, you can use this script to send answer and accuracy.sh to the instance
		where your results are saved.

The process of demo:

1. Open a terminal and execute client.sh.
2. Change directory to demo_client on your client instance.
3. Open the other terminal and start your server instance.
4. Type "time <Run your server program>" on your server instance and prepare to execute demo.sh on your client instance.
5. Hit Enter on your server first and hit Enter on you client instance.
6. If your results are not on your local machine, please run send.sh first.
7. Execute accuracy.sh on the instance where your results are saved.

Note:
1. When you execute accuracy.sh, make sure that accuracy.sh and answer directory are in the same directory.

