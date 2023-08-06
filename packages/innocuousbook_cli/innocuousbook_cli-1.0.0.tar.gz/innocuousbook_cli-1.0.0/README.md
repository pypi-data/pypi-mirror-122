# innocuousbook_cli

## Build CLI 

1. run script file
```bash
sh build.sh
```

## Install CLI

1. Edit permission
```bash
chmod +x innocuousbook
```

2. Install
```
sudo install ./innocuousbook /usr/bin/
```

## Environment Variables

- INNOCUOUSBOOK_TOKEN (user's token)
- INNOCUOUSBOOK_HOST (server host, default https://dashboard.innocuous.ai)
> At Cloud IDE will auto set environment variables

## CLI Command

- [innocuousbook version](#version)
- [innocuousbook generate](#generate)
- [innocuousbook list](#list)
- [innocuousbook upload](#upload)
- [innocuousbook trial](#trial)

### <span id="version"> version </span>

show cli and server version
```bash
innocuousbook version
```

result
```bash
[2021-10-01 01:24:35][INFO    ] CLI version: 1.0.0
[2021-10-01 01:24:35][INFO    ] Server version: beta-1.0.0
```

### <span id="generate"> generate </span>

generate demo recipe file
```bash
innocuousbook generate
```
> output file: demo_recipe.json

### <span id="list"> list </span>

list all user's file (model function dataset requirements)
```bash
innocuousbook list [model, function, dataset, requirements]
```

> -o table (output table format, default)  
-o json (output json format)

list all model in json format
```bash
innocuousbook list model -o json
```

### <span id="upload"> upload </span>

Upload file to fine manager (model function dataset)
```bash
innocuousbook upload [model, function, dataset] -n <NAME> -p <FOLDER/FILE>
```

Upload model
```bash
innocuousbook upload model -n myModel -p /home/ubuntu/myModel/
```

Upload function
```bash
innocuousbook upload function -n myFunctionl -p /home/ubuntu/myFunctionl/
```

Upload requirements
```bash
innocuousbook upload requirements -n myRequirements -p /home/ubuntu/requirements.txt
```

Upload dataset
```bash
innocuousbook upload dataset -p /home/ubuntu/myDatasetzip
```

### <span id="trial"> trial </span>

Create experiment
```bash
innocuousbook trial -r <RECIPE_FILE_PATH>
```