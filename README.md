# os-pixel-data
Collect data for your os repository readme.


# Getting Set Up Using [wip]

You'll need `docker-compose`.


    $ docker-compose -f deploy/docker-compose.yml up

## Once `redpanda`, `buz`, and the `console` are running you can:

### Track a README view

(already happening, just refresh the page)

![view](http://localhost:8080/pixel/io.silverton/buz/pixel/pageView/v1.0?msg=hello&subject=world&location=buzwax&page=os-pixel-data)

### Hit the pixel with an arbitrary payload:

Track [localhost:8080/pixel?msg=hello&subject=world&location=buzwax](http://localhost:8080/pixel?msg=hello&subject=world&location=buzwax)

### Hit a named, schematized pixel and redirect to a link:

Track and [redirect to bytewax.io](http://localhost:8080/pixel/io.silverton/buz/pixel/linkClick/v1.0?msg=hello&subject=world&link=thisone&location=buzwax&rto=https://bytewax.io/)


### Inspect the payloads:

using the [Redpanda Console](http://localhost:8082/topics)