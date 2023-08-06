import pickle

path = './test/torch-1.9.1-cp37-cp37m-manylinux1_x86_64.pkl'  # path='/root/……/aus_openface.pkl'   pkl文件所在路径

f = open(path, 'rb')
data = pickle.load(f)

print(data.head)
print(len(data))
