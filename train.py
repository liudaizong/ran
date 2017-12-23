from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torchvision
from torchvision import transforms, datasets, models
import os
import cv2
from model.residual_attention_network import ResidualAttentionModel

# Image Preprocessing 
transform = transforms.Compose([
    transforms.Scale(224),
    transforms.ToTensor()])

# CIFAR-10 Dataset
train_dataset = datasets.CIFAR10(root='./data/',
                               train=True, 
                               transform=transform,
                               download=True)

test_dataset = datasets.CIFAR10(root='./data/',
                              train=False, 
                              transform=transforms.ToTensor())

# Data Loader (Input Pipeline)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=20, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=20, 
                                          shuffle=False)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

model = ResidualAttentionModel()
print(model)

lr = 0.001
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# Training 
for epoch in range(100):
    for i, (images, labels) in enumerate(train_loader):
        images = Variable(images)
        # print(images.data)
        labels = Variable(labels)
        
        # Forward + Backward + Optimize
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        print("hello")
        if (i+1) % 100 == 0:
            print ("Epoch [%d/%d], Iter [%d/%d] Loss: %.4f" %(epoch+1, 80, i+1, 500, loss.data[0]))

    # Decaying Learning Rate
    if (epoch+1) % 20 == 0:
        lr /= 3
        optimizer = torch.optim.Adam(model.parameters(), lr=lr) 

# Save the Model
torch.save(model.state_dict(), 'model.pkl')

# Test
correct = 0
total = 0
#
class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))

for images, labels in test_loader:
    images = Variable(images)
    outputs = model(images)
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum()
    #
    c = (predicted == labels).squeeze()
    for i in range(4):
        label = labels[i]
        class_correct[label] += c[i]
        class_total[label] += 1

print('Accuracy of the model on the test images: %d %%' % (100 * correct / total))

# class_correct = list(0. for i in range(10))
# class_total = list(0. for i in range(10))
# for data in testloader:
#     images, labels = data
#     outputs = model(Variable(images.cuda()))
#     _, predicted = torch.max(outputs.data, 1)
#     c = (predicted == labels).squeeze()
#     for i in range(4):
#         label = labels[i]
#         class_correct[label] += c[i]
#         class_total[label] += 1


for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))

