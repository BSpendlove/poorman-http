# poorman-http
Just a learning project for me to build a http client in Python to learn more about Python and not just using import statements :-)

It's a really poor example and you shouldn't read the code... This project isn't meant to be used in production and its not fast... probably one of the slowest http clients you'll ever see

## NOTES:

### How does a HTTP request actually work from a network level?

1. Client types in a URL
2. DNS resolution for that URL, A records (ipv4) or AAAA records (ipv6) returns the IPv4/6 address to contact, common http port is 80, https = 443
3. Now we have the host, we can attempt to create a socket, sockets allow us to communicate to remote devices, python has socket implemented natively in the module called "sockets". I don't want to write sockets... :-) but they essentially allow us to ingest data from some kind of input (network) and handle the transport protocol stack (TCP in our case), opening a port on the client machine so that when data returns back, we know which application to pass the traffic back to... again I want to sleep at least a few times a week so I'd rather not implement sockets from scratch
4. Now we need to implement the HTTP protocol, if its HTTPS then we need some layer of TLS management but I will just worry about HTTP for now... HTTP Operations, building the initial HTTP request, different HTTP standards... HTTP is a very back and fourth protocol... I speak and request something, you send me back a response

Let's read HTTP RFC... Yay, latest one is HTTP/1.1 so I'll ignore the others and only care about this... Here are some quick notes from my RFC reading: (RFC7231)

- "Each Hypertext Transfer Protocol (HTTP) message is either a request or a response"... I got something right at least on my last few sentences...
- Target of HTTP request is called a resource, maybe I need a HTTPRequest and HTTPResponse class...
- Target URI must be in the format of RFC7230 Section 5.3...
```
request-target = origin-form
    / absolute-form
    / authority-form
    / asterisk-form
```
wtf is this lol... Origin form is the most common form, client must send only the absolute path  with queries (`?` character)... Ok so like http://blahblah.com/?something=hello... My path is `/` and I have optional parameters `?`... Exclude `?` if no parameters are apart of the HTTPRequest when the client builds it... Ok got it

- Representation header fields provide metadata on the representation of the data... eg:
```
   +-------------------+-----------------+
   | Header Field Name | Defined in...   |
   +-------------------+-----------------+
   | Content-Type      | Section 3.1.1.5 |
   | Content-Encoding  | Section 3.1.2.2 |
   | Content-Language  | Section 3.1.3.2 |
   | Content-Location  | Section 3.1.4.2 |
   +-------------------+-----------------+
```
Ok like application/json for example if I want to load it using `json` module...

- Media types (RFC2046) used in Content-Type and Accept... These are things like `text/plain`... Omg I regret this already, gonna be so much reading...
- Charset is used to indicate character encoding... ? UTF-8? idk...
- Finally found out what MIME stands for... Multipurpose Internet Mail Extensions... It all started with that guy sending his wife an email about how much they love them right? I think that was one reason the internet took off... or maybe why routers were invented I forgot...
- Ok enough reading, lets look at urllib3 implementation of HTTP client... I am interested more in after the socket is created, how we build the initial HTTP Request with the various headers in the HTTP message itself... Oh right... urllib implements http which is apart of the python language... (https://github.com/python/cpython/blob/3.11/Lib/http/client.py#L790)

