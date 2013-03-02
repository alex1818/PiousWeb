class Extra(object):
    def onLoad(self, data, views, popup):
        if popup:
            data = self.imagePopup(data, "http://192.168.1.2/thepiousweb/really2.png")
        else:
            data = self.constantPopup(data)
            #data = self.popup(data, self.content[views % len(self.content)].replace("\n", ""))
        return data

    def constantPopup(self, data):
        data += """
          <script>
            window.top.onload = function() {
              TINY.box.show({
                html:'You are being watched over by God.<br />If you're feeling sufficiently pious, click to restart.',
                animate:false,
                close:false,
                mask:false,
                boxid:'god',
                autohide:10,
                top:20,
                left:20,
                fixed:true
              });
            };
          </script>
        """
        return data

    def imagePopup(self, data, uri):
        data += """
          <script>
            window.top.onload = function() {
              TINY.box.show({
                image:'%s',
                animate:true,
                fixed: true,
                close: true
              });
            };
          </script>
        """ % (uri)
        return data

    def popup(self, data, html):
        data += """
          <script>
            window.top.onload = function() {
              TINY.box.show({
                  html:'%s',
                  fixed:true,
                  boxid:'popup',
                  close: true
                });
            };
          </script>
        """ % (html)
        return data

    def greenBox(self, data, views):
        data += """
          <script>
            window.top.onload = function() {
              TINY.box.show({
                  html:'You have viewed this %d times',
                  animate:false,
                  close:false,
                  mask:false,
                  boxid:'success',
                  autohide:2,
                  top:14,
                  left:17
                });
            };
          </script>
          """ % (views)
        return data

