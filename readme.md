

```#AdmiN@123Sonar```
```sqp_bb1bb2d46020236d0eee7d70d995797dd648b760```

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=maven-project01 \
  -Dsonar.host.url=http://192.168.1.139:30000/ \
  -Dsonar.login=sqp_bb1bb2d46020236d0eee7d70d995797dd648b760
