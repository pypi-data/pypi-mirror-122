import torch 
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as dsets
import torch.nn.functional as F
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys
from torch.utils.data import Dataset, DataLoader
from os import listdir
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import r2_score
from joblib import dump, load
from StatsArbData import ObtainData
torch.manual_seed(0)

class LoadData(Dataset):
    def __init__(self, X, y):
        self.x = torch.tensor(X).float()
        self.y = torch.tensor(y).long()
        self.len = self.x.shape[0]

    def __getitem__(self,index):
        return self.x[index],self.y[index]

    def __len__(self):
        return self.len

class DNN_1(nn.Module):
    def __init__(self, D_in, H1, H2, H3, D_out=2):
        super(DNN_1, self).__init__()
        self.drop1 = nn.Dropout(p = 0.1)
        self.drop2 = nn.Dropout(p = 0.5)
        self.channel1_l1 = nn.Linear(D_in, H1)
        self.channel1_l2 = nn.Linear(H1, H2)
        self.channel1_l3 = nn.Linear(H2, H3)
        
        self.channel2_l1 = nn.Linear(D_in, H1)
        self.channel2_l2 = nn.Linear(H1, H2)
        self.channel2_l3 = nn.Linear(H2, H3)
        
        self.out = nn.Linear(H3, D_out)

    def forward(self, x):
        x = torch.max(self.drop1(self.channel1_l1(x)), self.drop1(self.channel2_l1(x)))
        x = torch.max(self.drop2(self.channel1_l2(x)), self.drop2(self.channel2_l2(x)))
        x = torch.max(self.drop2(self.channel1_l3(x)), self.drop2(self.channel2_l3(x)))
        x = F.softmax(self.out(x))
        return x

class DNN_2(nn.Module):
    def __init__(self, D_in, H1, H2, H3, D_out=2):
        super(DNN_2, self).__init__()
        self.drop1 = nn.Dropout(p = 0.5)
        self.drop2 = nn.Dropout(p = 0.25)
        
        self.linear1_1 = nn.Linear(D_in, H1)
        torch.nn.init.kaiming_uniform_(self.linear1_1.weight, nonlinearity = "leaky_relu")
        self.linear2_1 = nn.Linear(H1, H2)
        torch.nn.init.kaiming_uniform_(self.linear2_1.weight, nonlinearity = "leaky_relu")
        self.linear3_1 = nn.Linear(H2, H3)
        torch.nn.init.kaiming_uniform_(self.linear3_1.weight, nonlinearity = "leaky_relu")
        self.linear1_2 = nn.Linear(D_in, H1)
        torch.nn.init.kaiming_uniform_(self.linear1_2.weight, nonlinearity = "leaky_relu")
        self.linear2_2 = nn.Linear(H1, H2)
        torch.nn.init.kaiming_uniform_(self.linear2_2.weight, nonlinearity = "leaky_relu")
        self.linear3_2 = nn.Linear(H2, H3)
        torch.nn.init.kaiming_uniform_(self.linear3_2.weight, nonlinearity = "leaky_relu")
        
        self.bn1 = nn.BatchNorm1d(H1)
        self.bn2 = nn.BatchNorm1d(H2)
        self.bn3 = nn.BatchNorm1d(H3)
        
        self.out = nn.Linear(H3, D_out)

    def forward(self, x):
        x = torch.max(self.bn1(self.drop1(self.linear1_1(x))), self.bn1(self.drop1(self.linear1_2(x))))
        x = torch.max(self.bn2(self.drop2(self.linear2_1(x))), self.bn2(self.drop2(self.linear2_2(x))))
        x = torch.max(self.bn3(self.linear3_1(x)), self.bn3(self.linear3_2(x)))
        x = F.softmax(self.out(x))
        return x


class ML_Models:
  def __init__(self, X_training, X_testing, y_training, y_testing):
      torch.manual_seed(0)
      self.deep_nn_1 = DNN_1(31, 31, 10, 5, 2)
      self.deep_nn_2 = DNN_2(31, 31, 10, 5, 2)
      self.random_forest = RandomForestClassifier(n_estimators = 1000, max_depth=20, max_features = "sqrt", random_state=0)
      self.gb_trees = GradientBoostingClassifier(n_estimators = 100, max_depth = 3, learning_rate = 0.1, min_samples_split = 15, random_state = 0)
      self.training = LoadData(X_training, y_training)
      self.testing = LoadData(X_testing, y_testing)
      self.X_training = X_training
      self.X_testing = X_testing 
      self.y_training = y_training
      self.y_testing = y_testing

  def train_dnn(self, model, criterion, train_loader, validation_loader, optimizer, paper_model=False, epochs=100, show_training_info = True):
      training_info = {'training_loss':[], 'validation_accuracy': []}
      MIN = -1
      COUNTER = 0
      temp = []
      for epoch in range(epochs):
          for i, (x, y) in enumerate(train_loader):
              optimizer.zero_grad()
              y_hat = model(x)
              if paper_model:
                  lambda1 = 0.00001
                  all_params = torch.cat([b.view(-1) for b in model.parameters()])
                  l1_regularization = lambda1 * torch.norm(all_params, 1)
                  loss = criterion(y_hat,y) + l1_regularization
              else:
                  loss = criterion(y_hat,y)
              loss.backward()
              optimizer.step()
              training_info['training_loss'].append(loss.data.item())
            
          if paper_model:
              if epoch < 400 or loss.data.item() < MIN:
                  MIN = loss.data.item()
                  COUNTER = 0
              else:
                  COUNTER += 1
                
          correct = 0
          accuracy = 0
          for x, y in validation_loader:
              z = model(x)
              _, y_hat = torch.max(z,1)
              correct = (y_hat == y).sum().item()
              accuracy += correct/x.shape[0]
          training_info['validation_accuracy'].append(accuracy/len(validation_loader))
          
          if show_training_info:
              print("LOSS:",training_info['training_loss'][-1],"ACCURCY:",training_info['validation_accuracy'][-1])
              print("current epoch",epoch+1,", ", 100*(epoch+1)/epochs, "% completed")

          if COUNTER == 5:
              print("FINISHED!!!")
              break
            
      return training_info

  def train_models(self, plot_graphs = False):
      # Define loss function and get training and testing datasets
      criterion = nn.CrossEntropyLoss()

      # Training DNN's paper model
      torch.manual_seed(0)
      train_loader = DataLoader(dataset = self.training, batch_size=2000, shuffle = True)
      validation_loader = DataLoader(dataset = self.testing, batch_size=5000)
      optimizer = torch.optim.Adadelta(self.deep_nn_1.parameters())


      path_1 = "dnn1.pth"
      try:
          self.deep_nn_1.load_state_dict(torch.load(path_1))
          self.deep_nn_1.eval()
          print("DNN 1 Model loaded")
      except:
          print("Training DNN Model 1...")
          dnn_1_info = self.train_dnn(self.deep_nn_1, criterion, train_loader, validation_loader, optimizer, paper_model = True, epochs = 500)
          if plot_graphs:
              steps = int(len(dnn_1_info["training_loss"])/len(dnn_1_info["validation_accuracy"]))
              plt.plot(dnn_1_info["training_loss"][::steps], color = "red")
              plt.plot(dnn_1_info["validation_accuracy"], color = "blue")
              plt.show()
          
          torch.save(self.deep_nn_1.state_dict(), path_1)
          print("DNN - Model 1 Accuracy: ", dnn_1_info["validation_accuracy"][-1])

      # Training DNN's our proposed model
      torch.manual_seed(0)
      train_loader = DataLoader(dataset = self.training, batch_size=2000, shuffle = True)
      validation_loader = DataLoader(dataset = self.testing, batch_size=5000)
      optimizer = torch.optim.Adam(self.deep_nn_2.parameters(), lr=1e-4)

      path_2 = "dnn2.pth"

      try:
          self.deep_nn_2.load_state_dict(torch.load(path_2))
          self.deep_nn_2.eval()
          print("DNN 2 Model loaded")
      except:
          print("Training DNN Model 2...")
          dnn_2_info = self.train_dnn(self.deep_nn_2, criterion, train_loader, validation_loader, optimizer, paper_model = False, epochs = 400)
          if plot_graphs:
              steps = int(len(dnn_2_info["training_loss"])/len(dnn_2_info["validation_accuracy"]))
              plt.plot(dnn_2_info["training_loss"][::steps], color = "red")
              plt.plot(dnn_2_info["validation_accuracy"], color = "blue")
              plt.show()

          torch.save(self.deep_nn_2.state_dict(), path_2)
          print("DNN- Model 2 Accuracy: ", dnn_2_info["validation_accuracy"][-1])
      
      

      # Training Random Forest
      try:
          self.random_forest = load("random_forest.joblib")
          print("Random Forest model loaded")
      except:
          self.random_forest.fit(self.X_training, self.y_training)
          dump(self.random_forest, "random_forest.joblib")
      print("Random Forest Accuracy:", self.random_forest.score(self.X_testing, self.y_testing))

      # Training Gradient Boosted Trees
      try:
          self.gb_trees = load("gb_tree.joblib")
          print("Gradient Boosted Trees model loaded")
      except:
          self.gb_trees.fit(self.X_training, self.y_training)
          dump(self.gb_trees, "gb_tree.joblib")
      print("Gradient Boosted Trees Accuracy:", self.gb_trees.score(self.X_testing, self.y_testing))
      print("TRAINING IS DONE!")

      return self.deep_nn_1, self.deep_nn_2, self.random_forest, self.gb_trees

  def import_DNN_1(self):
    return self.deep_nn_1
  
  def import_DNN_2(self):
    return self.deep_nn_2

  def import_rf(self):
    return self.random_forest
  
  def import_gbt(self):
    return self.gb_trees

class Models:
  def __init__(self, trading_year):
    self.dataset = ObtainData(trading_year = trading_year)
    self.X_training, self.y_training, self.X_testing, self.y_testing = self.dataset.getSplitData()
    self.models = ML_Models(self.X_training, self.X_testing, self.y_training, self.y_testing)	

  def getModels(self):
    self.dnn1, self.dnn2, self.rf, self.gbt = self.models.train_models(plot_graphs=False)
    return self.dnn1, self.dnn2, self.rf, self.gbt 
