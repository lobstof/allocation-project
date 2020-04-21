const http = require('http');
const url = require('url');

const SERVICEPORT = 2000;
const HOST = "localhost"

var fs = require('fs');

var pod_list = [
    {
        "name": "netflix-1",
        "contentProvider": "Netflix",
        "status": "false",
        "ip_address": "1.1.1.1",
        "port": "8000",
        "request_number": 0
    },
    {
        "name": "netflix-2",
        "contentProvider": "Netflix",
        "status": "false",
        "ip_address": "1.1.1.1",
        "port": "8000",
        "request_number": 0
    },
    {
        "name": "netflix-3",
        "contentProvider": "Netflix",
        "status": "false",
        "ip_address": "1.1.1.1",
        "port": "8000",
        "request_number": 0
    },
    {
        "name": "netflix-4",
        "contentProvider": "Netflix",
        "status": "false",
        "ip_address": "1.1.1.1",
        "port": "8000",
        "request_number": 0
    },
    {
        "name": "netflix-cloud",
        "contentProvider": "Netflix",
        "status": "false",
        "ip_address": "1.1.1.1",
        "port": "8000",
        "request_number": 0
    },
    {
        "name": "calculater",
        "availableNumber": 0,
        "total_request_number": 0

    }]
    ;

var data = JSON.stringify(pod_list);


// This function is prepared for the second version
function build_list() {
    fs.writeFile('./list.json', data, function (err) {
        if (err) {
            console.log('There has been an error saving your configuration data.');
            console.log(err.message);
            return;
        }
        console.log('list build successfully.')
    });
}

function jsonReader(filePath, cb) {
    fs.readFile(filePath, (err, fileData) => {
        if (err) {
            return cb && cb(err)
        }
        try {
            const object = JSON.parse(fileData)
            return cb && cb(null, object)
        } catch (err) {
            return cb && cb(err)
        }
    })
}

function update_list(_name, _ip_address, _port, _status) {
    // console.log(_status)

    jsonReader('list.json', (err, pods) => {
        if (err) throw false;
        // console.log("pods read sucess1");
        i = 0;
        while (i < 5) {
            if (pods[i].name == _name) {
                pods[i].port = _port;
                pods[i].ip_address = _ip_address;
                pods[i].status = _status;
                if(i == 4){
                    // the cloud server isn't included at availabelServer calculator
                    break;
                }
                if(_status == "true"){
                    // we are adding the pod
                    pods[5].availableNumber = i+1;
                    console.log("we are adding the pod availableNumber:" + pods[5].availableNumber)
                } else {
                    // we are deleting the pod
                    pods[5].availableNumber = i;
                    console.log("we are deleting the pod availableNumber:" + pods[5].availableNumber)
                }
                break;
            }
            i++;
        }
        // console.log("pods read sucess2");


        fs.writeFile('./list.json', JSON.stringify(pods), function (err) {
            if (err) {
                // console.log('There has been an error saving your configuration data.');
                // console.log(err.message);
                return;
            }
            // console.log('list updated successfully.')
        });
        return true;
    });
}

const server = http.createServer((req, res) => {

        var q = url.parse(req.url, true).query;
        var _name = q.name;
        var _ip_address = q.ip_address;
        var _port = q.port;
        var _status = q.status;

        if(q.initial == "true"){
            // initialization the container list 
            build_list();
            // todo : verify the parm value returned of build_list()
            // if == true -> res.statusCode = 200
            // if == tfalse -> 412 (mission failed)
            res.statusCode = 200;
            res.setHeader('Content-Type', 'text/plain');
            res.end();
            console.log("end of initializing list");
        } else if(q.check == "true"){
            jsonReader('list.json', (err, pods) => {
                pods
                res.writeHead(200, {
                    'Content-Type': 'json'
                });
                res.write(JSON.stringify(pods))
                res.end();
                console.log("end of check list");
            });
        } else {
            // todo : verify the parms aren't void 
            update_list(_name, _ip_address, _port, _status);
            // todo : verify the parm value returned of update_list()
            // if == true -> res.statusCode = 200
            // if == tfalse -> 412 (mission failed)
            res.statusCode = 200;
            res.setHeader('Content-Type', 'text/plain');
            res.end();
            console.log("end of updating list");
        }
});

server.listen(SERVICEPORT, () => {
    console.log(`Server running at ${SERVICEPORT}`);
});