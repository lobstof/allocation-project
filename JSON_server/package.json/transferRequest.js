var http = require('http');
var url = require('url')
var fs = require('fs');

const NumberCloudServer = 4;
// define a pods buffer
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
    if(_number<=10){
        // we choose the first container
        pod_selected = 0;
    } else if(_number<=20){
        pod_selected = 1;
    } else if(_number<=30){
        pod_selected = 2;
    } else if(_number<=40){
        pod_selected = 3;
    }

    jsonReader('list.json', (err, pods) => {
        if (err) throw false;
        // console.log("pod list read sucess");
        availablePods = pods[5].availableNumber;
        // console.log("podSelected"+pod_selected)
        // console.log(availablePods);
        // if the _number isn't smaller than Pods
        // the request than should be redirect to the cloud server
        if(pod_selected>availablePods){
            pod_selected = NumberCloudServer;
            }
        // get the server's infos
        // console.log("get the infos");
        returnPod[0] = pods[pod_selected].ip_address;
        returnPod[1] = pods[pod_selected].port;
        console.log(pod_selected);
        console.log(returnPod[0]);
        console.log(returnPod[1]);

        // access record
        pods[pod_selected].request_number = pods[pod_selected].request_number + 1;
        pods[NumberCloudServer+1].total_request_number = pods[NumberCloudServer+1].total_request_number +1;
        
        // record request
        fs.writeFile('./list.json', JSON.stringify(pods), function (err) {
            if (err) {
                // console.log('There has been an error saving your configuration data.');
                // console.log(err.message);
                return;
            }
            // console.log('list updated successfully.')
        });

        });
    // console.log("end of reading list");
    return returnPod;
}


http.createServer(function (req, res) {
    // read request number
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    var q = url.parse(req.url, true).query;
    var number = Number(q.number);
    // console.log("number = " + number);
    // make sure that client has given the right number positif
    if(isNaN(number) || number<1){
        res.writeHead(422, {'Content-Type': 'text/plain'});
        res.end("Can't find the resource, please give a positif number of video")
        // console.log("Error, number missed")
    } else {
        // read the latest list
        returnPodInfo = read_list(number);
        // console.log("returnPodInfo = " +returnPodInfo)
        ip_address = returnPodInfo[0];
        port = returnPodInfo[1];
        res.writeHead(302, {
            'Location' : "http://"+ip_address+":"+port
        });
        res.end();
        // console.log("End of Service")
    }
}).listen(9999); 