-- control_server.js
This is a light http server based on the Node_project. 
It is running on the port 3002 for the list_update request. 
Once it receive the update request, it will parse the paramaters in the url and put them into the JSON list. 







Issues
1. I've met a problem weired that I can't figure out yet.
Each time when the server receive a right request but with a bad number parameter, it will respose code 422 back to inform the client that the parameter isn't correct. It is good. However, when the client start a right request with a right number parameter, the webpage will be corrupted. 

-->"The site at http://localhost:9999/?number=5 has experienced a network protocol violation that cannot be repaired."

And we need to restart the request again to resolve this problem. 

2. the defalut Node is multithreading. For example, when 
            
            build_list();
            res.statusCode = 200;
            res.setHeader('Content-Type', 'text/plain');
            res.end();
            console.log("end of initializing list");

the console will print "end of initializing list" (the last command) before the function build_list() finish. 
For now, everything is ok, it didn't make any troubles. However, I think this is a point at risk which we need to put in mind.