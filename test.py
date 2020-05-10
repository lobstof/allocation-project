
import json
# 列表写入文件
# 测试list
risk_list =  [61,45,78,35,78,54]
# 将数据写入文件
file = open('risk.json', 'w')
for i in risk_list:
    json_i = json.dumps(i)
    file.write(json_i+'\n')
file.close()

def list_to_json_file(data_list):
     data_list = data_list
     file = open('ratio_record.json', 'w')
     for i in data_list:
          json_i = json.dumps(i)
          file.write(json_i+'\n')
     file.close()

# 从文件中读取数据
risk_result = []
with open('risk.json','r') as f:
    # 读取数据并分割。 最后一个为空，所以去除
    risk_new_list = f.read().split('\n')[:-1]
    for x in risk_new_list:
        json_x = json.loads(x)
        risk_result.append(json_x)
f.close()
print("原始数据是：", risk_list)
print("结果数据是：", risk_result)