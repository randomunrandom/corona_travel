# Corna travel Open API

To access open API in web browser download this folder and run command

```
docker run --name ASD_swagger -d -p 8080:8080 -v ${PWD}/Task9/swagger.json:/swagger.yaml -e SWAGGER_FILE=/swagger.yaml swaggerapi/swagger-editor
```
