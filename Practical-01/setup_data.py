import os

os.makedirs("data", exist_ok=True)

with open("data/sample.txt", "w", encoding="utf-8") as f:
    f.write("user_id: 101\nusername: alex_dev\nstatus: active\ndepartment: \ntimeout_seconds: -30\n")

with open("data/sample.csv", "w", encoding="utf-8") as f:
    f.write("id,name,age,salary\n1,Alice Johnson,29,75000\n2,Bob Miller,-5,50000\n3,Charlie Brown,,90000\n4,David Smith,150,62000\n5,Eve Davis,34,-1500\n")

with open("data/sample.html", "w", encoding="utf-8") as f:
    f.write("<html><body><table><tr><th>id</th><th>name</th><th>age</th><th>salary</th></tr><tr><td>1</td><td>Frank</td><td>45</td><td>82000</td></tr><tr><td>2</td><td>Grace</td><td></td><td>95000</td></tr><tr><td>3</td><td>Hank</td><td>-10</td><td>54000</td></tr></table></body></html>")

with open("data/sample.xml", "w", encoding="utf-8") as f:
    f.write("<users><user><id>1</id><name>Iris</name><age>28</age><salary>65000</salary></user><user><id>2</id><name>Jack</name><age>200</age><salary>45000</salary></user><user><id>3</id><name>Kara</name><age>27</age><salary></salary></user></users>")

with open("data/sample.json", "w", encoding="utf-8") as f:
    f.write('[{"id": 1, "name": "Liam", "age": 52, "salary": 110000}, {"id": 2, "name": "Mia", "age": null, "salary": 72000}, {"id": 3, "name": "Noah", "age": -3, "salary": -5000}]')

print("All sample files generated inside data/ folder.")