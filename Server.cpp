#include <bits/stdc++.h>
// #include <stdio.h>
// #include <iostream>
// #include <string.h>

#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 8080

int main(int argc, char const *argv[])
{
	int sock;
	char s[1024];

	sockaddr_in serv_addr;
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	while( ( sock = socket( AF_INET, SOCK_STREAM, 0 ) ) < 0) continue;
	printf("Successfully created socket\n");

	if (inet_pton( AF_INET, "127.0.0.1", &serv_addr.sin_addr ) <= 0)
	{ printf("Invalid address/ Address not supported\n"); return 0; }

	while( !connect( sock, (sockaddr *)&serv_addr, sizeof( serv_addr ) ) ) continue;
	printf("Succesfully connected to server\n");

	char buff[1024] = {0};
	while(1)
	{
		printf("SENDING: ");
		fgets(s, 1024, stdin);

		if(strlen(s) == 2 && s[0] == 'q') break;

		send( sock, s, strlen(s) - 1, 0 );
		int numRead = recv( sock, buff, 1024, 0 );

		std::cout << "RECEIVED: ";
		printf("%s\n", buff);
	}

	shutdown( sock, SHUT_RDWR );

	return 0;
}
