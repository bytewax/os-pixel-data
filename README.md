# os-pixel-data
Collect data for your os repository readme.


# Getting Set Up Using [wip]

You'll need `docker-compose`.


    $ docker-compose -f deploy/docker-compose.yml up

## Once `redpanda`, `buz`, and the `console` are running you can:

### Track a README view

()(already happening, just refresh the page)

![view][localhost:8080/pixel/io.silverton/buz/pixel/pageView/v1.0?msg=hello&subject=world&location=buzwax]

### Hit a named, schematized pixel when a thing is clicked:

[localhost:8080/pixel/io.silverton/buz/pixel/linkClick/v1.0?msg=hello&subject=world&location=buzwax](localhost:8080/pixel/io.silverton/buz/pixel/linkClick/v1.0?msg=hello&subject=world&location=buzwax)

### Hit a named, schematized pixel and redirect to a link:

[localhost:8080/pixel/io.silverton/buz/pixel/linkClick/v1.0?msg=hello&subject=world&location=buzwax&rto=https://bytewax.io/](localhost:8080/pixel/io.silverton/buz/pixel/linkClick/v1.0?msg=hello&subject=world&location=buzwax&rto=https://bytewax.io/)
