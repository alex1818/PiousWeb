class Extra(object):

    content = [
        """<img src="http://192.168.1.2/thepiousweb/ThePiousWeb.png" />
        <br />
        <br />
        <table cellpadding=20>
          <tr>
            <td><img src="http://192.168.1.2/thepiousweb/tablets.jpg" /></td>
            <td><p>And I said to Moses, "Come up to me on the mountain and stay here, and I will give you the tablets of stone, with the law and commands I have written for their instruction." (Exodus 32:16)</p>

            <p>The tablets were the work of God [that&#39;s me]; the writing was the writing of God [me again], engraved on the tablets. (Exodus 24:12)</p>

            <p>Thou shalt subscribe to the commandments, mobile or otherwise.</p>
            </td>
          </tr>
        </table>
        """,

            ]

    def onLoad(self, data, views, popup):
        if popup:
            data = self.popup(data, self.content[0].replace("\n", ""))
            data = self.popup(data, self.content[views % len(self.content)].replace("\n", ""))
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

