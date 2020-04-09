var http = require('http');
var url = require('url')
var fs = require('fs');

const NumberCloudServer = 4;
var returnPod = [];


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

function read_list(_number) {
    // default number is directed to cloud server
    pod_selected = NumberCloudServer;
    if(_number<10){
        // we choose the first container
        pod_selected = 0;
    } else if(_number<20){
        pod_selected = 1;
    } else if(_number<30){
        pod_selected = 2;
    } else if(_number<40){
        pod_selected = 3;
    }

    jsonReader('list.json', (err, pods) => {
        if (err) throw false;
        console.log("pod list read sucess");
        availablePods = pods[5].availableNumber;
        console.log(availablePods);
        // if the _number isn't smaller than Pods
        // the request than should be redirect to the cloud server
        if(pod_selected>=availablePods){
            pod_selected = NumberCloudServer;
            }
        // get the server's infos
        console.log("get the infos");
        returnPod[0] = pods[pod_selected].ip_address;
        returnPod[1] = pods[pod_selected].port;
        console.log(returnPod[0]);
        console.log(returnPod[1]);
        });
    return returnPod;
}

http.createServer(function (req, res) {
    // read request number
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    var q = url.parse(req.url, true).query;
    var number = Number(q.number);

    // read the latest list
    returnPodInfo = read_list(number);

    ip_address = returnPodInfo[0];
    port = returnPodInfo[1];
    res.writeHead(302, {
        'Location' : "http://"+ip_address+":"+port
    });
    res.end();
}).listen(9999); 