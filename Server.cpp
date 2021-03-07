// Client side C/C++ program to demonstrate Socket programming
// #include <stdio.h>
// #include <iostream>
// #include <sys/socket.h>
// #include <arpa/inet.h>
// #include <unistd.h>
// #include <string.h>

#include <bits/stdc++.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 8080

int main(int argc, char const *argv[])
{
	int sock = socket( AF_INET, SOCK_STREAM, 0 );
	if(sock < 0) { std::cout << "Creation failed" << std::endl; return 0; }

	sockaddr_in serv_addr;
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	// Convert IPv4 and IPv6 addresses from text to binary form
	if (inet_pton( AF_INET, "127.0.0.1", &serv_addr.sin_addr ) <= 0)
	{ std::cout << "\nInvalid address/ Address not supported" << std::endl; return 0; }

	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{ std::cout << "\nConnection Failed" << std::endl; return -1; }

	std::string s = "";
	char buff[1024] = {0};
	while(1)
	{
		std::cout << "SENDING: ";
		std::cin >> s;

		if(s.size() == 1 && s[0] == 'q') break;

		send( sock, s.c_str(), s.size(), 0 );
		int numRead = read( sock, buff, 1024 );

		std::cout << "RECEIVING ";
		for(int i = 0; i < numRead;) std::cout << buff[i++];
		std::cout << std::endl;
	}

	return 0;
}
