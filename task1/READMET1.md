Task1 Description:

This code was written on a windows machine with python 3.11.5 installed. The reason this was run
on windows was because it was necessary to test the code using a browser and postman, which I could 
not do on the eceubuntu server.

To start the server on a windows machine with python 3 installed, run the following command in this directory:

    python webserver.py

If this is being run on a linux machine (eg. eceubuntu), you can also run the following command:

    python3 webserver.py

To send a request to the server, use the following url.  Replace the "/example/file.html" path with your path
to an HTML file:

    http://localhost:10000/example/file.html

If you want to use the HTML file that we included, and you place it in the same directory as this server, you would use the url:

    http://localhost:10000/HelloWorld.html

Once the server is running, test the server using a Web Browser or Postman as the client. If you test with Chrome first, it will hold on to the connection to the socket because it is a persistent connection.  Therefore, if you test with chrome first, make sure you close Chrome before testing with Postman.
