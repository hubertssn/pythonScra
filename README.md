# pythonScraper

### Launch API listener:
```
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```



### Terminate process to restart:
```
sudo lsof -i :5000
```
```
sudo kill <PID>
```
