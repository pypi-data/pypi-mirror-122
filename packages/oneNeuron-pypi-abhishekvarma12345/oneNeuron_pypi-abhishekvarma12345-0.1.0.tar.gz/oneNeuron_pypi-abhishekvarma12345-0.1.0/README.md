# oneNeuron_pypi
oneNeuron_pypi

## How to use this
1. In the main file create DataFrame for any of the logic gate
2. import Perceptron from oneNeuron.perceptron API 
3. import prepare_data,save_model and save_plot from utils.all_utils API
4. There are loggong modules already present in the API's. So, paste the below code as it is in the start of main file
```python
logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir, "running_logs.log"),level=logging.INFO, format=logging_str
,filemode='a')
``` 
5. The above logging code creates logs directory and do the logging in running_logs.log file
6. Then train the model accordingly and include logging wherever needed in the main program
```python
from oneNeuron.perceptron import Perceptron
## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X,y)
```

# References -
[Official Python Docs](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)