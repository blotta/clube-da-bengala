# Clube da Bengala


## Venv

### Create

```powershell
py -3 -v venv venv
.\venv\Scripts\activate
pip install Flask
```


### Running
```powershell
.\venv\Scripts\activate
```

## Config

```powershell
# powershell
$env:FLASK_APP = "clubedabengala"
$env:FLASK_ENV = "development"
```

## Rebuild database Schema

```shell
flask init-db
```

## Run
```shell
flask run
```
