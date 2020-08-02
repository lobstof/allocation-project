# Log introduction

## state log
The list is the record of changement of allocation state. For example, we start with 1 then 11, 1, 11 etc...

## request_running.log
Each client simulation process generated several records at this file with the request video number and request's destination host. 

## ratio_list_record.json
This is the record list of request ratio
[[ratio_to_cloud_youtube1,ratio_to_cloud_netflix1,ratio_to_cloud_total1],[ratio_to_cloud_youtube2,ratio_to_cloud_netflix2,ratio_to_cloud_total2],[ratio_to_cloud_youtube3,ratio_to_cloud_netflix3,ratio_to_cloud_total3],[ratio_to_cloud_youtube4,ratio_to_cloud_netflix4,ratio_to_cloud_total4]...]

## k8s_running.log
present each action taken during the simulation