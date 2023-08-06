import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import joblib
import os

plt.style.use('fivethirtyeight')

def prepare_data(df_name):
  """Function prepare independent and dependent data and also pandas dataframe.
  Args:
      df_name (Dictionary): Dictionary object
  Returns:
      X [independent variable]: Pandas series object
      y [dependent variable]: Pandas series object
      df [data frame]: Pandas dataframe object
  """
  df = pd.DataFrame(df_name)

  X = df.drop("y", axis=1)
  y = df["y"]

  return X, y, df

def save_model(model, filename):
  """This saves trained model.
  Args:
      model (python object): Trained model
      filename (str): file name for mdoel
  """
  model_dir = "models"
  os.makedirs(model_dir, exist_ok=True)
  save_path = os.path.join(model_dir, filename)
  joblib.dump(model, save_path)

def save_plot(df_name, filename, model):
  """Function for save plots
  Args:
      df_name (Dictionary): Dictionary object
      filename (str): File name for prepared plot
      model (python object): Trained model
  """
  def _create_base_plot(df):
    df.plot(kind='scatter', x="x1", y="x2", c="y", s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10,8)

  def _plot_decision_regions(X, y, model, resolution=0.2):
    colors = ["red", "blue", "lightgreen", "cyan", "gray"]
    cmap = ListedColormap(colors[: len(np.unique(y))]) # take colours for unique y values

    X = X.values
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1 # from first column "x1"
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1 # from second column "x2"
    
    # Get all values for x1 and x2 between min and max
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    
    Z = model.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    plt.plot()
  
  X, y, df = prepare_data(df_name)
  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True)
  save_path = os.path.join(plot_dir, filename)
  plt.savefig(save_path)