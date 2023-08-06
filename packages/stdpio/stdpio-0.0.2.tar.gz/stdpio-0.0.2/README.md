# stdp.io client library

A library to interact with the stdp.io REST API

## authenticating

```

#init
stdp = stdpio(username="username", password="password", model_dir="/tmp/")

```

## fetching your Akida models

```

#get models
models = stdp.my_models()

# fetch all the model files & knowns
for model in models:
	# download the model file from stdp.io
    stdp.fetch_model_file(model)
    # print the labels and trained neurons for the model
    print(stdp.fetch_known(model))

```