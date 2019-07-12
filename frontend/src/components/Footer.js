import React from "react";

class Footer extends React.Component {
  render() {
    console.log("Footer.render");

        return (
            <div class="footer container">
              <div class="row">
                <div class="col">
                  Made by Christina Branson
                  <br/>
                  <a href="https://darksky.net/poweredby/" target="_blank">Powered By DarkSky</a>
                  <br/>
                  View source on <a href="https://github.com/christinabranson/weather-app" target="_blank">Github</a>.
                </div>
              </div>
            </div>
        );

  }
}
export default Footer;