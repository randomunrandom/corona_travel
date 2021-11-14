# 🦠 Corona Travel

Our goal is to allow users to travel online from home via any device of their liking. They'll start by opening an app or a link and choosing a desired destination. After choosing a location, users can choose to view destination in 3D, look at some 3D photos or videos or learn some facts about the place.

## Task 9
```sh
docker run --name ASD_swagger -d -p 8080:8080 -v ${PWD}/Task9/swagger.json:/swagger.yaml -e SWAGGER_FILE=/swagger.yaml swaggerapi/swagger-editor
```

