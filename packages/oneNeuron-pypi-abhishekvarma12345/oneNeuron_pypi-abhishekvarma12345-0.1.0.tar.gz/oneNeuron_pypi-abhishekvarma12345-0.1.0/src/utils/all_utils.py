import os
import matplotlib.pyplot as plt
import numpy as np
import joblib # used for saving model as binary file
from matplotlib.colors import ListedColormap
import logging

plt.style.use("fivethirtyeight") #style for the graphs


def prepare_data(df):
  """It is used to seperate dependent and Independent features 

   Args:
    df (pd.DataFrame): Its the pandas DataFrame

   Returns:
    tuple: It returns the tuple consist of dependent and Independent features
  """
  logging.info("Preparing the data by segregating dependent and independent variables")
  X = df.drop("y",axis=1)
  y = df["y"]
  return X,y

def save_model(model, filename):
    """This creates models directory and saves the model with specified filename

     Args:
      model (python object): trained model to
      filename (str): path to save the trained model
    """
    logging.info("saving the trained model")
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True) # only create if model dir doesn't exist
    filePath = os.path.join(model_dir,filename) # model/filename
    joblib.dump(model,filePath)
    logging.info(f"saved the trained model at {filePath}")

def save_plot(df, filename, model):
  """This creates plots directory and saves the plot with specified filename

    Args:
        df (pd.DataFrame): Its a DataFrame object
        filename (str): filename of the plot
        model (model): trained model
  """
  def _create_base_plot(df):
    logging.info("Creating the base plot")
    df.plot(kind="scatter", x="x1", y="x2", c='y', s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get the current figure
    figure.set_size_inches(10,8)

  def _plot_decision_regions(X, y, classifier, resolution=0.02):
    logging.info("Plotting decision regions")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[:len(np.unique(y))])
    X = X.values # as array
    x1_min, x1_max = min(X[:,0]) - 1,  max(X[:,0]) + 1
    x2_min, x2_max = min(X[:,1]) - 1,  max(X[:,1]) + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(),xx1.max())
    plt.ylim(xx2.min(),xx2.max())
    plt.plot()
  
  X,y = prepare_data(df)

  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # only create if plot dir doesn't exist
  plotPath = os.path.join(plot_dir,filename) # model/filename
  plt.savefig(plotPath)
  logging.info(f"saving the plots at {plotPath}")