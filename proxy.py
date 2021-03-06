#!/usr/bin/python
"""A basic transparent HTTP proxy"""

__author__ = "Erik Johansson"
__email__  = "erik@ejohansson.se"
__license__= """
Copyright (c) 2012 Erik Johansson <erik@ejohansson.se>
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

"""

from twisted.web import http
from twisted.internet import reactor, protocol
from twisted.python import log
import re
import sys
import os
import random
from datetime import datetime, timedelta

from watermark import watermark 

websiteCounts = {}
websiteLastCount = {}

imageCount = [0]

for f in os.listdir("tmp"):
    try:
        imageCount[0] = max(imageCount[0], int(f))
    except:
        pass

imageCount[0] = imageCount[0] + 1

log.startLogging(sys.stdout)

class ProxyClient(http.HTTPClient):
    """ The proxy client connects to the real server, fetches the resource and
    sends it back to the original client, possibly in a slightly different
    form.
    """

    def __init__(self, method, uri, postData, headers, originalRequest):
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.contentLength = None

    def sendRequest(self):
        log.msg("Sending request: %s %s" % (self.method, self.uri))
        self.sendCommand(self.method, self.uri)

    def sendHeaders(self):
        for key, values in self.headers:
            if key.lower() == 'connection':
                values = ['close']
            elif key.lower() == 'keep-alive':
                next

            for value in values:
                self.sendHeader(key, value)
        self.endHeaders()

    def sendPostData(self):
        log.msg("Sending POST data")
        self.transport.write(self.postData)

    def connectionMade(self):
        log.msg("HTTP connection made")
        self.sendRequest()
        self.sendHeaders()
        if self.method == 'POST':
            self.sendPostData()

    def handleStatus(self, version, code, message):
        log.msg("Got server response: %s %s %s" % (version, code, message))
        self.originalRequest.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        if key.lower() == 'content-length':
            self.contentLength = value
        else:
            self.originalRequest.responseHeaders.addRawHeader(key, value)

    def handleResponse(self, data):
        data = self.originalRequest.processResponse(data)

        if self.contentLength != None:
            self.originalRequest.setHeader('Content-Length', len(data))

        self.originalRequest.write(data)

        self.originalRequest.finish()
        self.transport.loseConnection()

class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.protocol = ProxyClient
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest

    def buildProtocol(self, addr):
        return self.protocol(self.method, self.uri, self.postData,
                             self.headers, self.originalRequest)

    def clientConnectionFailed(self, connector, reason):
        log.err("Server connection failed: %s" % reason)
        self.originalRequest.setResponseCode(504)
        self.originalRequest.finish()

class ProxyRequest(http.Request):
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor

    def process(self):
        host = self.getHeader('host')
        if not host:
            log.err("No host header given")
            self.setResponseCode(400)
            self.finish()
            return

        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)

        self.setHost(host, port)

        self.content.seek(0, 0)
        postData = self.content.read()
        factory = ProxyClientFactory(self.method, self.uri, postData,
                                     self.requestHeaders.getAllRawHeaders(),
                                     self)
        self.reactor.connectTCP(host, port, factory)

    def processResponse(self, data):
        contentType = self.headers.get("content-type", "")
        log.msg("CONTENT TYPE:", contentType)

        if "text/html" in contentType:
            gcount = -1
            popup = False

            # apparently the client tuple line goes a little haywire sometime
            try:
                clientTuple = tuple([tuple(self.requestHeaders.getRawHeaders(x)) for x in ("accept-language", "accept-encoding", "accept", "user-agent")])
                clientHash = hash(clientTuple)
                if clientHash not in websiteLastCount or datetime.now() - timedelta(seconds=5) > websiteLastCount[clientHash]:
                    websiteCounts[clientHash] = websiteCounts.get(clientHash, 0) + 1
                    websiteLastCount[clientHash] = datetime.now()
                    gcount = websiteCounts[clientHash]
                    popup = True
            except:
                pass

            for scriptFile in sorted(os.listdir(os.path.join("scripts", "enabled"))):
                path, extension = os.path.splitext(scriptFile)
                log.msg("SCRIPT", scriptFile, extension, ".")
                if extension == ".py" and path != "__init__":
                    mod = __import__("scripts.enabled.%s" % path, fromlist=['Extra'])
                    extra = getattr(mod, "Extra")
                    klass = extra()
                    data = klass.onLoad(data, gcount, popup)
                elif extension == ".html":
                    script = open(os.path.join("scripts", "enabled", scriptFile), "r")
                    data += script.read()
                    script.close()
                elif extension == ".js":
                    script = open(os.path.join("scripts", "enabled", scriptFile), "r")
                    data += "<script>" + script.read() + "</script>"
                    script.close()
                elif extension == ".css":
                    script = open(os.path.join("scripts", "enabled", scriptFile), "r")
                    data += "<style media='screen' type='text/css'>" + script.read() + "</style>"
                    script.close()

        # half the time, hence the random choice
        if self.code != 304 and "image" in contentType and random.choice([True, False]):
            if not os.path.exists("tmp"):
                os.mkdir("tmp")

            count = globals()["imageCount"][0]
            fileName = os.path.join("tmp", "%06d" % (count))
            globals()["imageCount"][0] = count + 1
            f = open(fileName, "w")
            f.write(data)
            f.close()

            watermark.watermarkApply(fileName)

            f = open(fileName, "r")
            data = f.read()
            f.close()

        return data

class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest
 
class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy

reactor.listenTCP(3128, ProxyFactory())
reactor.run()
